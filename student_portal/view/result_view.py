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
                           TextBasedResultModel, TextResultCategoryModel, TextResultModel, ResultSettingModel,
                           MidResultGradeModel)
from academic.models import AcademicSettingModel, ClassSectionInfoModel, SubjectsModel


# ============================================================================
# NEW: HELPER FUNCTION FOR FEE RESTRICTION CHECK
# ============================================================================
def check_student_fee_restriction(student, academic_setting, result_setting):
    """
    Check if a student meets the fee requirements to view results.

    Args:
        student: StudentsModel instance
        academic_setting: SchoolAcademicInfoModel instance with session and term
        result_setting: ResultSettingModel instance

    Returns:
        tuple: (allowed: bool, message: str)
            - allowed: True if student can view results, False otherwise
            - message: Error message to display if not allowed, empty string if allowed
    """
    # If no restriction is set, allow access
    if not result_setting.fee_restriction_type or result_setting.fee_restriction_type == 'none':
        return True, ""

    # Get student's invoice for the current term
    invoice = InvoiceModel.objects.filter(
        student=student,
        session=academic_setting.session,
        term=academic_setting.term
    ).first()

    # If no invoice exists, allow access (no fees to pay)
    if not invoice:
        return True, ""

    # Calculate amounts based on scope (specific fee or all fees)
    if result_setting.fee_restriction_scope:
        # Specific fee selected - check only that fee
        items = invoice.items.filter(
            fee_master__fee=result_setting.fee_restriction_scope
        )

        if not items.exists():
            # Student doesn't have this specific fee, allow access
            return True, ""

        total_amount = sum(item.amount for item in items)
        amount_paid = sum(item.effective_amount_paid for item in items)
        balance = sum(item.balance for item in items)
        fee_name = result_setting.fee_restriction_scope.name
    else:
        # All fees - use invoice totals
        total_amount = invoice.total_amount
        amount_paid = invoice.effective_amount_paid
        balance = invoice.balance
        fee_name = "total fees"

    # If total amount is zero, allow access
    if total_amount == 0:
        return True, ""

    # Check based on restriction type
    if result_setting.fee_restriction_type == 'percentage':
        # Calculate percentage paid
        percentage_paid = (amount_paid / total_amount) * 100
        required_percentage = result_setting.fee_payment

        if percentage_paid < required_percentage:
            message = (
                f'You must pay at least {required_percentage:.0f}% of your {fee_name} '
                f'to access results. Currently paid: {percentage_paid:.1f}%'
            )
            return False, message

    elif result_setting.fee_restriction_type == 'fixed_balance':
        # Check if balance exceeds maximum allowed
        max_balance = Decimal(str(result_setting.fee_payment))

        if balance > max_balance:
            message = (
                f'Your {fee_name} balance (₦{balance:,.2f}) exceeds the maximum allowed '
                f'balance of ₦{max_balance:,.2f} to access results. '
                f'Please make a payment to view your results.'
            )
            return False, message

    # If we reach here, student meets the requirements
    return True, ""


# ============================================================================
# UPDATED: CURRENT TERM RESULT VIEW
# ============================================================================
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

    # NEW: Use the updated fee restriction check
    allowed, restriction_message = check_student_fee_restriction(student, academic_setting, result_setting)
    if not allowed:
        messages.warning(request, restriction_message)
        return redirect(reverse('student_dashboard'))

    # Check if results are published
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
        field_list = ResultFieldModel.objects.filter(student_class=student_class, class_section=class_section,
                                                     type=student.type).order_by('order')
        grade_list = ResultGradeModel.objects.filter(student_class=student_class, class_section=class_section,
                                                     type=student.type).order_by('order')
        mid_grade_list = MidResultGradeModel.objects.filter(student_class=student_class,
                                                            class_section=class_section,
                                                            type=request.user.profile.type).order_by('order')
        behaviour_category_list = ResultBehaviourCategoryModel.objects.filter(type=student.type).order_by('name')
    else:
        field_list = ResultFieldModel.objects.filter(student_class=student_class, class_section=class_section).order_by(
            'order')
        grade_list = ResultGradeModel.objects.filter(student_class=student_class, class_section=class_section).order_by(
            'order')
        behaviour_category_list = ResultBehaviourCategoryModel.objects.all().order_by('name')
        mid_grade_list = MidResultGradeModel.objects.filter(student_class=student_class,
                                                            class_section=class_section).order_by('order')

    class_detail = ClassSectionInfoModel.objects.filter(student_class=student_class, section=class_section).first()
    subject_list = student.subject_group.subjects.all() if student.subject_group else (
        class_detail.subjects.all() if class_detail else [])

    midterm_max = 0
    for field in field_list:
        if field.mid_term:
            midterm_max += field.max_mark

    context = {}
    if student_class and (student_class.result_type == 'text' or student_class.result_type == 'mix'):
        text_result = TextBasedResultModel.objects.filter(term=term, session=session, student=student).first()
        if school_setting.separate_school_section:
            result_category_list = TextResultCategoryModel.objects.filter(term=term, session=session, type=student.type,
                                                                          student_class=student_class,
                                                                          class_section=class_section).order_by('order')
            result_field_list = TextResultModel.objects.filter(type=student.type, student_class=student_class,
                                                               class_section=class_section).order_by('order')
        else:
            result_category_list = TextResultCategoryModel.objects.filter(term=term, session=session,
                                                                          student_class=student_class,
                                                                          class_section=class_section).order_by('order')
            result_field_list = TextResultModel.objects.filter(student_class=student_class,
                                                               class_section=class_section).order_by('order')

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
        'mid_grade_list': mid_grade_list,
        'behaviour_category_list': behaviour_category_list,
        'behaviour_result': behaviour_result,
        'class_minimum': class_minimum,
        'result_type': result_type,
        'midterm_max': midterm_max,
    })
    return render(request, 'student_portal/result/main_result_template.html', context=context)


# ============================================================================
# EXISTING: RESULT SELECT VIEW (No changes needed)
# ============================================================================
class ResultSelectView(LoginRequiredMixin, TemplateView):
    template_name = 'student_portal/result/select.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = get_object_or_404(StudentsModel, user=self.request.user)
        sessions_with_results = ResultModel.objects.filter(student=student).values_list('session', flat=True).distinct()
        context['student_session_list'] = SessionModel.objects.filter(pk__in=sessions_with_results).order_by(
            '-start_year')
        context['term_list'] = TermModel.objects.all().order_by('order')
        return context


# ============================================================================
# UPDATED: ARCHIVED RESULT VIEW
# ============================================================================
@login_required
def student_result_archive_sheet_view(request, pk):
    student = get_object_or_404(StudentsModel, pk=pk)
    session_pk = request.GET.get('session_pk')
    term_pk = request.GET.get('term_pk')

    if not session_pk or not term_pk:
        messages.error(request, "Session and Term must be selected to view archived results.")
        return redirect('student_result_select')

    session = get_object_or_404(SessionModel, pk=session_pk)
    term = get_object_or_404(TermModel, pk=term_pk)

    school_setting = SchoolGeneralInfoModel.objects.first()

    # Get result setting for fee restriction check
    if school_setting.separate_school_section:
        result_setting = ResultSettingModel.objects.filter(type=student.type).first()
        academic_setting = SchoolAcademicInfoModel.objects.filter(type=student.type).first()
    else:
        result_setting = ResultSettingModel.objects.first()
        academic_setting = SchoolAcademicInfoModel.objects.first()

    # NEW: Check fee restriction for archived results too
    # Create a temporary academic_setting object for the selected term
    class TempAcademicSetting:
        def __init__(self, session, term):
            self.session = session
            self.term = term

    temp_academic_setting = TempAcademicSetting(session, term)

    if result_setting:
        allowed, restriction_message = check_student_fee_restriction(student, temp_academic_setting, result_setting)
        if not allowed:
            messages.warning(request, f"Archive Access Restricted: {restriction_message}")
            return redirect('student_result_select')

    result = ResultModel.objects.filter(term=term, session=session, student=student).first()

    if not result:
        messages.warning(request, f"No result found for {student} in {term.name}, {session} session.")
        return redirect('student_result_select')

    student_class = result.student_class
    class_section = result.class_section

    behaviour_result = ResultBehaviourComputeModel.objects.filter(term=term, session=session, student=student).first()
    result_stat = ResultStatisticModel.objects.filter(term=term, session=session, student_class=student_class,
                                                      class_section=class_section).first()
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
        field_list = ResultFieldModel.objects.filter(student_class=student_class, class_section=class_section,
                                                     type=student.type).order_by('order')
        grade_list = ResultGradeModel.objects.filter(type=student.type).order_by('order')
        behaviour_category_list = ResultBehaviourCategoryModel.objects.filter(type=student.type).order_by('name')
    else:
        field_list = ResultFieldModel.objects.filter(student_class=student_class, class_section=class_section).order_by(
            'order')
        grade_list = ResultGradeModel.objects.all().order_by('order')
        behaviour_category_list = ResultBehaviourCategoryModel.objects.all().order_by('name')

    subject_list = SubjectsModel.objects.filter(
        pk__in=result.result.keys()) if result and result.result else SubjectsModel.objects.none()

    academic_setting_context = {'term': term, 'session': session}

    context = {
        'student': student,
        'academic_setting': academic_setting_context,
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
