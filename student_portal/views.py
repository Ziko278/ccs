from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin, messages
from django.http import HttpResponse
from num2words import num2words
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from communication.models import RecentActivityModel
from finance.forms import FeePaymentForm
from finance.models import OnlinePaymentModel, OutstandingFeeModel, FeePaymentSummaryModel, generate_payment_id
from finance.templatetags.fee_custom_filters import get_fee_discount, get_fee_penalty
from finance.utility import select_payment_method
from school_setting.models import SchoolGeneralInfoModel, SchoolAcademicInfoModel

from student.models import StudentsModel
from student_portal.view.result_view import *


def setup_test():
    if 1:
        return True
    return False


class StudentDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'student_portal/dashboard.html'

    def dispatch(self, *args, **kwargs):
        if setup_test():
            return super(StudentDashboardView, self).dispatch(*args, **kwargs)
        else:
            pass
            # return redirect(reverse('site_info_create'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['student'] = self.request.user.profile.student
        return context


class StudentClassMateView(LoginRequiredMixin, TemplateView):
    template_name = 'student_portal/classmate.html'

    def dispatch(self, *args, **kwargs):
        if setup_test():
            return super(StudentClassMateView, self).dispatch(*args, **kwargs)
        else:
            pass
            # return redirect(reverse('site_info_create'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.request.user.profile.student
        context['student'] = student
        context['classmate_list'] = StudentsModel.objects.filter(student_class=student.student_class, class_section=student.class_section).order_by('surname')
        context['class_section_info'] = ClassSectionInfoModel.objects.filter(student_class=student.student_class, section=student.class_section).first()
        return context


class StudentFeeView(SuccessMessageMixin, TemplateView):
    template_name = 'student_portal/fee/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        student = self.request.user.profile.student
        if school_setting.separate_school_section:
            academic_setting = SchoolAcademicInfoModel.objects.filter(type=student.type).first()
            termly_fee_list = FeeMasterModel.objects.filter(type=student.type,
                                                            fee__fee_occurrence='termly', student_class=student.student_class, class_section=student.class_section)
            if student.is_new:
                one_time_fee_list = FeeMasterModel.objects.filter(type=student.type, student_class=student.student_class, class_section=student.class_section).exclude(
                    fee__fee_occurrence='termly')
            else:
                one_time_fee_list = FeeMasterModel.objects.filter(type=student.type,
                                                                  student_class=student.student_class,
                                                                  class_section=student.class_section).exclude(
                    fee__fee_occurrence='termly').exclude(is_new=True)
            payment_method = OnlinePaymentModel.objects.filter(type=student.type, status='active')

        else:
            academic_setting = SchoolAcademicInfoModel.objects.first()
            termly_fee_list = FeeMasterModel.objects.filter(fee__fee_occurrence='termly', student_class=student.student_class, class_section=student.class_section)
            if student.is_new:
                one_time_fee_list = FeeMasterModel.objects.filter(student_class=student.student_class, class_section=student.class_section).exclude(fee__fee_occurrence='termly')
            else:
                one_time_fee_list = FeeMasterModel.objects.filter(student_class=student.student_class, class_section=student.class_section).exclude(fee__fee_occurrence='termly').exclude(is_new=True)
            payment_method = OnlinePaymentModel.objects.filter(status='active')

        context['academic_setting'] = academic_setting
        context['student'] = student
        context['termly_fee_list'] = termly_fee_list
        context['one_time_fee_list'] = one_time_fee_list
        context['payment_method_list'] = payment_method

        return context


def select_fee_method(request):
    if request.method == 'POST':
        student = StudentsModel.objects.get(pk=request.POST.get('student'))
        fee = FeeMasterModel.objects.get(pk=request.POST.get('fee'))
        session = request.POST.get('session')
        term = request.POST.get('term')
        amount = request.POST.get('amount')
        amount_in_word = num2words(amount)
        method = request.POST.get('payment_method')

        return select_payment_method(request, student, fee, amount, amount_in_word, method, session, term)


class StudentFeeDashboardView(LoginRequiredMixin, SuccessMessageMixin, TemplateView):
    template_name = 'student_portal/fee/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        student = self.request.user.profile.student
        student_class = student.student_class
        class_section = student.class_section
        if school_setting.separate_school_section:
            academic_setting = SchoolAcademicInfoModel.objects.filter(type=self.request.user.profile.type).first()
            fee_setting = FinanceSettingModel.objects.filter(type=self.request.user.profile.type).first()
            if student_class and class_section:
                termly_fee_list = FeeMasterModel.objects.filter(type=self.request.user.profile.type,
                                                                fee__fee_occurrence='termly',
                                                                student_class__in=[student_class.id],
                                                                class_section__in=[class_section.id])
                one_time_fee_list = FeeMasterModel.objects.filter(type=self.request.user.profile.type,
                                                                student_class__in=[student_class.id],
                                                                class_section__in=[class_section.id]).exclude(fee__fee_occurrence='termly').filter(
							        Q(fee__payment_term='any term') | Q(fee__payment_term=academic_setting.term))
            else:
                termly_fee_list = []
                one_time_fee_list = []
        else:
            academic_setting = SchoolAcademicInfoModel.objects.first()
            fee_setting = FinanceSettingModel.objects.first()
            if student_class and class_section:
                termly_fee_list = FeeMasterModel.objects.filter(fee__fee_occurrence='termly',
                                                                student_class__in=[student_class.id],
                                                                class_section__in=[class_section.id])
                one_time_fee_list = FeeMasterModel.objects.filter(student_class__in=[student_class.id],
                                                                class_section__in=[class_section.id]).exclude(fee__fee_occurrence='termly').filter(
                                                                Q(fee__payment_term='any term') | Q(fee__payment_term=academic_setting.term))

            else:
                termly_fee_list = []
                one_time_fee_list = []
        outstanding_payment_list = OutstandingFeeModel.objects.filter(student=student, status='active')
        current_fee, fee_paid, fee_discount, fee_penalty, fee_balance, outstanding_fee = 0, 0, 0, 0, 0, 0
        for fee_master in termly_fee_list:
            if fee_master.same_termly_price:
                amount = fee_master.amount
            else:
                if academic_setting.term == '1st term':
                    amount = fee_master.first_term_amount
                elif academic_setting.term == '2nd term':
                    amount = fee_master.second_term_amount
                elif academic_setting.term == '3rd term':
                    amount = fee_master.third_term_amount
            current_fee += amount
            fee_paid += get_amount_paid(fee_master, student.id)
            fee_discount += get_fee_discount(fee_master, student.id)
            fee_penalty += get_fee_penalty(fee_master, student.id)
            fee_balance += get_fee_balance(fee_master, student.id)

        for fee_master in one_time_fee_list:
            if fee_master.fee.payment_term == 'any term':
                amount = fee_master.amount
            elif fee_master.fee.payment_term == academic_setting.term:
                amount = fee_master.amount
            else:
                amount = 0

            current_fee += amount
            fee_paid += get_amount_paid(fee_master, student.id)
            fee_discount += get_fee_discount(fee_master, student.id)
            fee_penalty += get_fee_penalty(fee_master, student.id)
            fee_balance += get_fee_balance(fee_master, student.id)

        for fee in outstanding_payment_list:
            if fee.balance:
                outstanding_fee += fee.balance

        context['academic_setting'] = academic_setting
        context['fee_setting'] = fee_setting
        context['student'] = student
        context['current_fee'] = current_fee
        context['fee_paid'] = fee_paid
        context['fee_discount'] = fee_discount
        context['fee_penalty'] = fee_penalty
        context['fee_balance'] = fee_balance
        context['outstanding_fee'] = outstanding_fee
        context['total_fee'] = outstanding_fee + fee_balance
        if current_fee:
            context['percentage_paid'] = round(((current_fee - fee_balance)/current_fee) * 100)
        else:
            context['percentage_paid'] = 0

        return context


class StudentFeePaymentCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = FeePaymentModel
    form_class = FeePaymentForm
    success_message = 'Fee Payment Teller Uploaded, Wait for confirmation'
    template_name = 'student_portal/fee/create.html'

    def get_success_url(self):
        return reverse('student_fee_payment_summary_create', kwargs={'payment_pk': self.object.pk,
                                                             'student_pk': self.object.student.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        student = self.request.user.profile.student
        student_class = student.student_class
        class_section = student.class_section
        if school_setting.separate_school_section:
            academic_setting = SchoolAcademicInfoModel.objects.filter(type=self.request.user.profile.type).first()
            fee_setting = FinanceSettingModel.objects.filter(type=self.request.user.profile.type).first()
            if student_class and class_section:
                termly_fee_list = FeeMasterModel.objects.filter(type=self.request.user.profile.type,
                                                                fee__fee_occurrence='termly',
                                                                student_class__in=[student_class.id],
                                                                class_section__in=[class_section.id])
                one_time_fee_list = FeeMasterModel.objects.filter(type=self.request.user.profile.type,
                                                                student_class__in=[student_class.id],
                                                                class_section__in=[class_section.id]).exclude(fee__fee_occurrence='termly').filter(
							        Q(fee__payment_term='any term') | Q(fee__payment_term=academic_setting.term))
            else:
                termly_fee_list = []
                one_time_fee_list = []
        else:
            academic_setting = SchoolAcademicInfoModel.objects.first()
            fee_setting = FinanceSettingModel.objects.first()
            if student_class and class_section:
                termly_fee_list = FeeMasterModel.objects.filter(fee__fee_occurrence='termly',
                                                                student_class__in=[student_class.id],
                                                                class_section__in=[class_section.id])
                one_time_fee_list = FeeMasterModel.objects.filter(student_class__in=[student_class.id],
                                                                class_section__in=[class_section.id]).exclude(fee__fee_occurrence='termly').filter(
                                                                Q(fee__payment_term='any term') | Q(fee__payment_term=academic_setting.term))

            else:
                termly_fee_list = []
                one_time_fee_list = []
        current_payment_list = FeePaymentModel.objects.filter(student=student, session=academic_setting.session)
        all_payment_list = FeePaymentModel.objects.filter(student=student)
        outstanding_payment_list = OutstandingFeeModel.objects.filter(student=student, status='active')
        current_fee, fee_paid, fee_discount, fee_penalty, fee_balance, outstanding_fee = 0, 0, 0, 0, 0, 0
        for fee_master in termly_fee_list:
            if fee_master.same_termly_price:
                amount = fee_master.amount
            else:
                if academic_setting.term == '1st term':
                    amount = fee_master.first_term_amount
                elif academic_setting.term == '2nd term':
                    amount = fee_master.second_term_amount
                elif academic_setting.term == '3rd term':
                    amount = fee_master.third_term_amount
            current_fee += amount
            fee_paid += get_amount_paid(fee_master, student.id)
            fee_discount += get_fee_discount(fee_master, student.id)
            fee_penalty += get_fee_penalty(fee_master, student.id)
            fee_balance += get_fee_balance(fee_master, student.id)

        for fee_master in one_time_fee_list:
            if fee_master.fee.payment_term == 'any term':
                amount = fee_master.amount
            elif fee_master.fee.payment_term == academic_setting.term:
                amount = fee_master.amount
            else:
                amount = 0

            current_fee += amount
            fee_paid += get_amount_paid(fee_master, student.id)
            fee_discount += get_fee_discount(fee_master, student.id)
            fee_penalty += get_fee_penalty(fee_master, student.id)
            fee_balance += get_fee_balance(fee_master, student.id)

        for fee in outstanding_payment_list:
            if fee.balance:
                outstanding_fee += fee.balance

        context['academic_setting'] = academic_setting
        context['fee_setting'] = fee_setting
        context['student'] = student
        context['termly_fee_list'] = termly_fee_list
        context['one_time_fee_list'] = one_time_fee_list
        context['current_payment_list'] = current_payment_list
        context['all_payment_list'] = all_payment_list
        context['outstanding_payment_list'] = outstanding_payment_list
        context['current_fee'] = current_fee
        context['fee_paid'] = fee_paid
        context['fee_discount'] = fee_discount
        context['fee_penalty'] = fee_penalty
        context['fee_balance'] = fee_balance
        context['outstanding_fee'] = outstanding_fee
        context['total_fee'] = outstanding_fee + fee_balance
        if current_fee:
            context['percentage_paid'] = round(((current_fee - fee_balance)/current_fee) * 100)
        else:
            context['percentage_paid'] = 0

        return context


def student_create_fee__payment_summary(request, payment_pk, student_pk):
    payment = FeePaymentModel.objects.get(pk=payment_pk)
    fee_payment_summary = FeePaymentSummaryModel.objects.filter(fees__in=[payment.pk])
    if not fee_payment_summary:
        fee_payment_summary = FeePaymentSummaryModel.objects.create(
            student=payment.student, session=payment.session, term=payment.term, date=payment.date,
            online_payment_method=payment.online_payment_method, vat=payment.vat,  amount=payment.amount,
            type=payment.type, payment_proof=payment.payment_proof, status=payment.status, user=request.user,
            reference=generate_payment_id(payment.type))
        fee_payment_summary.save()
        fee_payment_summary.fees.add(payment)
        fee_payment_summary.save()
        student = fee_payment_summary.student
        payment_purpose = payment.fee.fee.name
        session = payment.session
        term = payment.term
        category = 'fee_payment'
        subject = "<b>{} {}</b> paid <b>N{}</b> for <b>{}</b>".format(student.surname.title(),
                                                                      student.last_name.title(), payment.amount,
                                                                      payment_purpose)
        activity = RecentActivityModel.objects.create(category=category, subject=subject,
                                                      reference_id=fee_payment_summary.id, type=student.type,
                                                      session=session, term=term)

        try:
            mail_subject = f'NEW TELLER OF ₦{payment.amount} UPLOADED BY STUDENT: {fee_payment_summary.student.__str__()}'
            message = f"""
            {fee_payment_summary.student.__str__()} just uploaded fee payment teller
            for the sum of {num2words(payment.amount)} naira (₦{payment.amount})
            been payment for {fee_payment_summary.fee_list()}
            """
            send_mail(mail_subject, message, 'odekeziko@gmail.com', ['accounts@whitecloudschool.sch.ng'],
                      fail_silently=True)
        except Exception:
            pass

    return redirect(reverse('student_fee_payments'))


@login_required
def student_fee_payment_list_view(request):
    session_id = request.GET.get('session', None)
    student = request.user.profile.student
    term = request.GET.get('term', None)
    if session_id:
        session = SessionModel.objects.get(id=session_id)
    else:
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            academic_setting = SchoolAcademicInfoModel.objects.filter(type=student.type).first()
        else:
            academic_setting = SchoolAcademicInfoModel.objects.first()
        session = academic_setting.session
        term = academic_setting.term

    session_list = SessionModel.objects.all()

    fee_payment_list = FeePaymentSummaryModel.objects.filter(student=student, session=session, term=term).order_by('-id')
    context = {
        'fee_payment_list': fee_payment_list,
        'session': session,
        'term': term,
        'session_list': session_list
    }
    return render(request, 'student_portal/fee/payment.html', context)


@login_required
def student_bulk_payment_create_view(request):
    if request.method == 'POST':
        fee_list = request.POST.getlist('fee[]')
        amount_list = request.POST.getlist('amount[]')
        payment_mode_list = request.POST.getlist('payment_mode[]')
        student_pk = request.POST.get('student')
        type = request.POST.get('type')
        vat = request.POST.get('vat')
        payment_date = request.POST.get('date')
        payment_proof = request.FILES.get('payment_proof')

        online_payment_method = request.POST.get('online_payment_method')
        school_setting = SchoolGeneralInfoModel.objects.first()
        student = get_object_or_404(StudentsModel, pk=student_pk)

        if school_setting.separate_school_section:
            academic_setting = SchoolAcademicInfoModel.objects.filter(type=type).first()
            fee_setting = FinanceSettingModel.objects.filter(type=type).first()
        else:
            academic_setting = SchoolAcademicInfoModel.objects.first()
            fee_setting = FinanceSettingModel.objects.first()
        session = academic_setting.session
        term = academic_setting.term

        total_amount = 0
        for num in range(len(amount_list)):
            total_amount += float(amount_list[num])

        reference = generate_payment_id(type)

        # Check if a FeePaymentSummaryModel already exists for the student, session, term, and reference
        fee_payment_summary = FeePaymentSummaryModel.objects.filter(student=student, session=session, term=term, reference=reference).first()

        if not fee_payment_summary:
            fee_payment_summary = FeePaymentSummaryModel.objects.create(
                student=student, session=session, term=term, online_payment_method=online_payment_method,
                vat=vat, date=payment_date, amount=total_amount, type=type,
                payment_proof=payment_proof, status='pending', user=request.user, reference=reference)
            fee_payment_summary.save()

        if fee_payment_summary.id:
            payment_purpose = ''
            for num in range(len(fee_list)):
                payment_mode = payment_mode_list[num]
                if payment_mode == 'online':
                    if fee_setting.use_2fa_online:
                        status = 'pending'
                    else:
                        status = 'confirmed'
                else:
                    status = 'pending'

                fee_id = fee_list[num]
                fee = FeeMasterModel.objects.get(pk=fee_id)
                if num == 1:
                    payment_purpose += fee.fee.name
                elif num > 1 and num == (len(fee_list) - 1):
                    payment_purpose += " & {} others".format(len(fee_list) - 1)
                amount = amount_list[num]
                fee_payment = FeePaymentModel.objects.create(
                    fee=fee, student=student, session=session, term=term,
                    online_payment_method=online_payment_method, payment_mode=payment_mode,
                    vat=vat, date=payment_date, amount=amount, payment_proof=payment_proof,
                    status=status, user=request.user, type=type)
                fee_payment.save()
                fee_payment_summary.fees.add(fee_payment)

            category = 'fee_payment'
            subject = "<b>{} {}</b> uploaded teller of <b>N{}</b> for <b>{}</b>".format(student.surname.title(),
                                                                          student.last_name.title(), total_amount,
                                                                          payment_purpose)
            activity = RecentActivityModel.objects.create(category=category, subject=subject,
                                                          reference_id=fee_payment_summary.id, type=student.type,
                                                          session=session, term=term)

            activity.save()

            try:
                mail_subject = f'NEW TELLER OF ₦{total_amount} UPLOAD BY {student.__str__()}'
                message = f"""
                {student.__str__().title()} just uploaded fee payment teller
                for the sum of {num2words(total_amount)} naira (₦{total_amount})
                been payment for {fee_payment_summary.fee_list()}
                """
                send_mail(mail_subject, message, 'odekeziko@gmail.com', ['accounts@whitecloudschool.sch.ng'],
                          fail_silently=True)
            except Exception:
                pass

            messages.success(request, 'Fee Payment Uploaded, Wait for Confirmation')
            return redirect(reverse('student_fee_payments'))
        else:
            messages.error(request, 'Error Processing Payments, Try Later')

    messages.error(request, 'method not supported, try again')
    return redirect(reverse('fee_select_student'))


class StudentFeeDetailView(LoginRequiredMixin, DetailView):
    model = FeePaymentSummaryModel
    fields = '__all__'
    template_name = 'student_portal/fee/detail.html'
    context_object_name = "fee_payment"


class StudentLessonNoteListView(LoginRequiredMixin, ListView):
    model = LessonNoteModel
    fields = '__all__'
    template_name = 'student_portal/lesson_note/index.html'
    context_object_name = "lesson_note_list"

    def get_queryset(self):
        student = self.request.user.profile.student
        return LessonNoteModel.objects.filter(grant_access=True, status='approved', student_class__student_class=student.student_class, student_class__section=student.class_section)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class StudentLessonNoteDetailView(LoginRequiredMixin, DetailView):
    model = LessonNoteModel
    fields = '__all__'
    template_name = 'student_portal/lesson_note/detail.html'
    context_object_name = "lesson_note"

