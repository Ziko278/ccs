from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from decimal import Decimal

# CORRECTED IMPORTS to use the new invoice-based finance models and correct app structure
from finance.models import InvoiceModel
from school_setting.models import SchoolGeneralInfoModel, SchoolAcademicInfoModel, SessionModel, TermModel
from student.models import StudentsModel
from result.models import (ResultModel, ResultBehaviourCategoryModel, ResultBehaviourComputeModel,
                           ResultStatisticModel, ResultRemarkModel, ResultFieldModel, ResultGradeModel,
                           TextBasedResultModel, TextResultCategoryModel, TextResultModel, ResultSettingModel)
from academic.models import AcademicSettingModel, ClassSectionInfoModel, SubjectsModel


def student_fee_percentage_paid(student, academic_setting):
    """
    REWRITTEN: This helper function now calculates the percentage of fees paid
    for the current term based on the new InvoiceModel.
    """
    invoice = InvoiceModel.objects.filter(
        student=student,
        session=academic_setting.session,
        term=academic_setting.term
    ).first()

    if not invoice or not invoice.total_amount or invoice.total_amount == 0:
        # If no invoice exists for the term, or the total is zero,
        # we assume they have paid 100% to avoid incorrectly blocking access.
        return 100

    # Calculate percentage based on the invoice's properties
    percentage_paid = (invoice.amount_paid / invoice.total_amount) * 100
    return round(percentage_paid)


@login_required
def current_term_result(request, pk):
    student = get_object_or_404(StudentsModel, pk=pk)
    result_type = request.GET.get('type', None)
    school_setting = SchoolGeneralInfoModel.objects.first()

    if school_setting.separate_school_section:
        result_setting = ResultSettingModel.objects.filter(type=student.type).first()
        academic_setting = SchoolAcademicInfoModel.objects.filter(type=student.type).first()
        academic_info = AcademicSettingModel.objects.filter(type=student.type).first()
    else:
        result_setting = ResultSettingModel.objects.first()
        academic_setting = SchoolAcademicInfoModel.objects.first()
        academic_info = AcademicSettingModel.objects.first()

    if not all([result_setting, academic_setting, academic_info]):
        messages.error(request, "School settings are not fully configured. Please contact administration.")
        return redirect(reverse('student_dashboard'))

    session = academic_setting.session
    term = academic_setting.term

    # CORRECTED: Use the new invoice-based fee check
    if result_setting.fee_payment and result_setting.fee_payment > 0:
        fee_paid_percentage = student_fee_percentage_paid(student, academic_setting)
        if fee_paid_percentage < result_setting.fee_payment:
            message = f'You must pay at least {result_setting.fee_payment}% of the current term fees to access results.'
            messages.warning(request, message)
            return redirect(reverse('student_dashboard'))

    if result_setting.result_status != 'published':
        messages.warning(request, 'Results for the current term have not been published yet.')
        return redirect(reverse('student_dashboard'))

    student_class = student.student_class
    class_section = student.class_section
    result = ResultModel.objects.filter(term=term, session=session, student=student).first()
    behaviour_result = ResultBehaviourComputeModel.objects.filter(term=term, session=session, student=student).first()
    result_stat = ResultStatisticModel.objects.filter(term=term, session=session, student_class=student_class,
                                                      class_section=class_section).first()
    result_remark = ResultRemarkModel.objects.filter(term=term, session=session, student=student).first()

    total_score = 0
    number_of_course = 0
    total_lowest = 0
    average = 0
    class_minimum = 0

    if result and result.result:
        number_of_course = len(result.result)
        for key, value in result.result.items():
            total_score += value.get('total', 0)
            if result_stat and result_stat.result_statistic and key in result_stat.result_statistic:
                stat_data = result_stat.result_statistic[key]
                value['highest_in_class'] = stat_data.get('highest_in_class', '')
                value['lowest_in_class'] = stat_data.get('lowest_in_class', '')
                value['average_score'] = stat_data.get('average_score', '')
                total_lowest += stat_data.get('lowest_in_class', 0)

    if number_of_course > 0:
        average = round((total_score / (100 * number_of_course)) * 100)
        class_minimum = round((total_lowest / (100 * number_of_course)) * 100)

    if school_setting.separate_school_section:
        field_list = ResultFieldModel.objects.filter(student_class=student_class, class_section=class_section, type=student.type).order_by('order')
        grade_list = ResultGradeModel.objects.filter(student_class=student_class, class_section=class_section, type=student.type).order_by('order')
        behaviour_category_list = ResultBehaviourCategoryModel.objects.filter(type=student.type).order_by('name')
    else:
        field_list = ResultFieldModel.objects.filter(student_class=student_class, class_section=class_section).order_by('order')
        grade_list = ResultGradeModel.objects.filter(student_class=student_class, class_section=class_section).order_by('order')
        behaviour_category_list = ResultBehaviourCategoryModel.objects.all().order_by('name')

    class_detail = ClassSectionInfoModel.objects.filter(student_class=student_class, section=class_section).first()
    subject_list = student.subject_group.subjects.all() if student.subject_group else (class_detail.subjects.all() if class_detail else [])

    midterm_max = 0
    for field in field_list:
        if field.mid_term:
            midterm_max += field.max_mark

    context = {}
    if student_class and (student_class.result_type == 'text' or student_class.result_type == 'mix'):
        text_result = TextBasedResultModel.objects.filter(term=term, session=session, student=student).first()
        if school_setting.separate_school_section:
            result_category_list = TextResultCategoryModel.objects.filter(term=term, session=session, type=student.type, student_class=student_class, class_section=class_section).order_by('order')
            result_field_list = TextResultModel.objects.filter(type=student.type, student_class=student_class, class_section=class_section).order_by('order')
        else:
            result_category_list = TextResultCategoryModel.objects.filter(term=term, session=session, student_class=student_class, class_section=class_section).order_by('order')
            result_field_list = TextResultModel.objects.filter(student_class=student_class, class_section=class_section).order_by('order')

        context.update({
            'result_list': text_result,
            'result_category_list': result_category_list,
            'result_field_list': result_field_list,
        })

    context.update({
        'student': student,
        'academic_setting': academic_setting,
        'academic_info': academic_info,
        'result': result,
        'total_score': total_score,
        'number_of_course': number_of_course,
        'average_score': average,
        'result_remark': result_remark,
        'general_setting': school_setting,
        'subject_list': subject_list,
        'field_list': field_list,
        'grade_list': grade_list,
        'behaviour_category_list': behaviour_category_list,
        'behaviour_result': behaviour_result,
        'class_minimum': class_minimum,
        'result_type': result_type,
        'midterm_max': midterm_max,
    })
    return render(request, 'student_portal/result/main_result_template.html', context=context)


class ResultSelectView(LoginRequiredMixin, TemplateView):
    template_name = 'student_portal/result/select.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = get_object_or_404(StudentsModel, user=self.request.user)
        sessions_with_results = ResultModel.objects.filter(student=student).values_list('session', flat=True).distinct()
        context['student_session_list'] = SessionModel.objects.filter(pk__in=sessions_with_results).order_by('-start_year')
        context['term_list'] = TermModel.objects.all().order_by('order')
        return context


@login_required
def student_result_archive_sheet_view(request, pk):
    student = get_object_or_404(StudentsModel, pk=pk)
    session_pk = request.GET.get('session_pk')
    term_pk = request.GET.get('term_pk')

    if not session_pk or not term_pk:
        messages.error(request, "Session and Term must be selected to view archived results.")
        return redirect('result_select')

    session = get_object_or_404(SessionModel, pk=session_pk)
    term = get_object_or_404(TermModel, pk=term_pk)

    academic_setting = {'term': term, 'session': session}
    result = ResultModel.objects.filter(term=term, session=session, student=student).first()

    if not result:
        messages.warning(request, f"No result found for {student} in {term.name}, {session} session.")
        return redirect('result_select')

    student_class = result.student_class
    class_section = result.class_section
    school_setting = SchoolGeneralInfoModel.objects.first()

    behaviour_result = ResultBehaviourComputeModel.objects.filter(term=term, session=session, student=student).first()
    result_stat = ResultStatisticModel.objects.filter(term=term, session=session, student_class=student_class, class_section=class_section).first()
    result_remark = ResultRemarkModel.objects.filter(term=term, session=session, student=student).first()

    total_score = 0
    number_of_course = 0
    total_lowest = 0
    average = 0
    class_minimum = 0

    if result.result:
        number_of_course = len(result.result)
        for key, value in result.result.items():
            total_score += value.get('total', 0)
            if result_stat and result_stat.result_statistic and key in result_stat.result_statistic:
                stat_data = result_stat.result_statistic[key]
                value['highest_in_class'] = stat_data.get('highest_in_class', '')
                value['lowest_in_class'] = stat_data.get('lowest_in_class', '')
                value['average_score'] = stat_data.get('average_score', '')
                total_lowest += stat_data.get('lowest_in_class', 0)

    if number_of_course > 0:
        average = round((total_score / (100 * number_of_course)) * 100)
        class_minimum = round((total_lowest / (100 * number_of_course)) * 100)

    if school_setting.separate_school_section:
        field_list = ResultFieldModel.objects.filter(student_class=student_class, class_section=class_section, type=student.type).order_by('order')
        grade_list = ResultGradeModel.objects.filter(type=student.type).order_by('order')
        behaviour_category_list = ResultBehaviourCategoryModel.objects.filter(type=student.type).order_by('name')
    else:
        field_list = ResultFieldModel.objects.filter(student_class=student_class, class_section=class_section).order_by('order')
        grade_list = ResultGradeModel.objects.all().order_by('order')
        behaviour_category_list = ResultBehaviourCategoryModel.objects.all().order_by('name')

    subject_list = SubjectsModel.objects.filter(pk__in=result.result.keys()) if result and result.result else SubjectsModel.objects.none()

    context = {
        'student': student,
        'academic_setting': academic_setting,
        'result': result,
        'total_score': total_score,
        'number_of_course': number_of_course,
        'average_score': average,
        'result_remark': result_remark,
        'general_setting': school_setting,
        'subject_list': subject_list,
        'field_list': field_list,
        'grade_list': grade_list,
        'behaviour_category_list': behaviour_category_list,
        'behaviour_result': behaviour_result,
        'class_minimum': class_minimum
    }
    return render(request, 'student_portal/result/main_result_template.html', context=context)

