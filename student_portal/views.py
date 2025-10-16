import json
from datetime import date, datetime, timedelta
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import Q, Sum, Avg, F, DecimalField, Value, Count
from django.db.models.functions import TruncMonth, Coalesce, Concat
from django.forms import modelformset_factory
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.utils import timezone
from django.utils.timezone import now
from django.views import View
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DetailView, FormView
from num2words import num2words
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# CORRECTED IMPORTS to work with the new project structure
from finance.models import InvoiceModel, FeePaymentModel, FinanceSettingModel
from school_setting.models import SchoolGeneralInfoModel, SchoolAcademicInfoModel
from student.models import StudentsModel
from academic.models import ClassSectionInfoModel, LessonNoteModel
from .view.result_view import *


def setup_test():
    # This function remains as you provided it.
    if 1:
        return True
    return False


class StudentDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'student_portal/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            # CORRECTED: Uses a safer direct lookup.
            context['student'] = StudentsModel.objects.get(user=self.request.user)
        except StudentsModel.DoesNotExist:
            context['student'] = None
        return context


class StudentClassMateView(LoginRequiredMixin, TemplateView):
    template_name = 'student_portal/classmate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            student = StudentsModel.objects.get(user=self.request.user)
            context['student'] = student
            if student and student.student_class and student.class_section:
                context['classmate_list'] = StudentsModel.objects.filter(
                    student_class=student.student_class,
                    class_section=student.class_section
                ).order_by('surname', 'last_name')
                context['class_section_info'] = ClassSectionInfoModel.objects.filter(
                    student_class=student.student_class,
                    section=student.class_section
                ).first()
            else:
                context['classmate_list'] = []
                context['class_section_info'] = None
        except StudentsModel.DoesNotExist:
            context['student'] = None
            context['classmate_list'] = []
            context['class_section_info'] = None
        return context


# ===================================================================
# RECREATED FEE VIEWS (Updated for Invoice System)
# ===================================================================

class StudentFeeDashboardView(LoginRequiredMixin, TemplateView):
    """
    RECREATED & RENAMED: This is the updated version of your `StudentFeeDashboardView`.
    It serves as the central hub for student finance, using the new Invoice system.
    """
    template_name = 'student_portal/fee/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = get_object_or_404(StudentsModel, user=self.request.user)
        school_setting = SchoolGeneralInfoModel.objects.first()

        if school_setting.separate_school_section:
            academic_setting = SchoolAcademicInfoModel.objects.filter(type=student.type).first()
        else:
            academic_setting = SchoolAcademicInfoModel.objects.first()

        context['academic_setting'] = academic_setting
        context['student'] = student

        # Get the invoice for the current term using the new InvoiceModel
        current_invoice = InvoiceModel.objects.filter(
            student=student,
            session=academic_setting.session,
            term=academic_setting.term
        ).first()

        # Calculate total outstanding fees from all previous unpaid invoices
        outstanding_invoices = InvoiceModel.objects.filter(
            student=student,
            status__in=[InvoiceModel.Status.UNPAID, InvoiceModel.Status.PARTIALLY_PAID]
        ).exclude(pk=current_invoice.pk if current_invoice else None)

        outstanding_fee_total = sum(inv.balance for inv in outstanding_invoices)

        # Set context variables from the new InvoiceModel's properties
        current_fee = current_invoice.total_amount if current_invoice else Decimal('0.00')
        fee_paid = current_invoice.amount_paid if current_invoice else Decimal('0.00')
        fee_balance = current_invoice.balance if current_invoice else Decimal('0.00')

        context['current_invoice'] = current_invoice
        context['outstanding_invoices'] = outstanding_invoices
        context['current_fee'] = current_fee
        context['fee_paid'] = fee_paid
        context['fee_balance'] = fee_balance
        context['outstanding_fee'] = outstanding_fee_total
        context['total_fee'] = fee_balance + outstanding_fee_total

        if current_fee > 0:
            context['percentage_paid'] = round((fee_paid / current_fee) * 100)
        else:
            context['percentage_paid'] = 100 if fee_paid > 0 else 0

        return context


class StudentFeeView(StudentFeeDashboardView):
    """
    RECREATED: In the new system, this view is now an alias for the main dashboard.
    It will render the same dashboard template.
    """
    template_name = 'student_portal/fee/dashboard.html'


class StudentFeePaymentCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    RECREATED: This view now handles uploading a payment teller for the CURRENT TERM'S INVOICE.
    It creates a FeePayment record with a 'pending' status for admin approval.
    """
    model = FeePaymentModel
    # Using a simplified form; you might want a more specific one
    fields = ['amount', 'payment_mode', 'date', 'reference', 'notes']
    template_name = 'student_portal/fee/create.html'
    success_message = "Your payment teller has been uploaded successfully and is awaiting confirmation."

    def get_success_url(self):
        return reverse('student_fee_dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = get_object_or_404(StudentsModel, user=self.request.user)
        academic_setting = SchoolAcademicInfoModel.objects.first()  # Simplified for this example
        current_invoice = InvoiceModel.objects.filter(
            student=student,
            session=academic_setting.session,
            term=academic_setting.term
        ).first()
        context['student'] = student
        context['invoice'] = current_invoice
        return context

    def form_valid(self, form):
        student = get_object_or_404(StudentsModel, user=self.request.user)
        academic_setting = SchoolAcademicInfoModel.objects.first()
        invoice = get_object_or_404(InvoiceModel, student=student, session=academic_setting.session,
                                    term=academic_setting.term)

        payment = form.save(commit=False)
        payment.invoice = invoice
        payment.status = FeePaymentModel.PaymentStatus.PENDING  # Always pending for admin review
        payment.save()

        return super().form_valid(form)


@login_required
def student_fee_payment_list_view(request):
    """
    RECREATED: This view lists all historical payments (both pending and confirmed)
    for the logged-in student.
    """
    student = get_object_or_404(StudentsModel, user=request.user)
    payment_list = FeePaymentModel.objects.filter(invoice__student=student).order_by('-date')
    context = {
        'student': student,
        'payment_list': payment_list
    }
    return render(request, 'student_portal/fee/payment_list.html', context)


class StudentFeeDetailView(LoginRequiredMixin, DetailView):
    """
    RECREATED: This view shows the details of a single payment transaction.
    """
    model = FeePaymentModel
    template_name = 'student_portal/fee/detail.html'
    context_object_name = "payment"

    def get_queryset(self):
        # Ensure students can only view their own payment details
        student = get_object_or_404(StudentsModel, user=self.request.user)
        return FeePaymentModel.objects.filter(invoice__student=student)


# The views below are now obsolete in the new invoice-based system.
# They are included by name as requested, but their functionality is either
# handled by the views above or is no longer applicable.

@login_required
def select_fee_method(request):
    """
    RECREATED: This view's original purpose is obsolete.
    It now redirects to the main fee dashboard.
    """
    messages.info(request, "Please use the dashboard to manage your fees.")
    return redirect('student_fee_dashboard')


@login_required
def student_bulk_payment_create_view(request):
    """
    RECREATED: The concept of "bulk payment" is now handled by making a single
    payment against an invoice. This view redirects to the standard payment upload page.
    """
    messages.info(request, "To pay for multiple fees, please upload a single teller for your current term's invoice.")
    return redirect('student_fee_create')


@login_required
def student_create_fee__payment_summary(request, payment_pk, student_pk):
    """
    RECREATED: The old FeePaymentSummaryModel is no longer used. The new FeePaymentModel
    serves as the complete record. This view now redirects to the payment detail page.
    """
    return redirect('student_fee_detail', pk=payment_pk)


# ===================================================================
# UNCHANGED VIEWS (Lesson Note and Result Views)
# ===================================================================

# NOTE: The result-related views from your 'student_portal/view/result_view.py' file
# should be placed here. I am including the lesson note views you provided.

class StudentLessonNoteListView(LoginRequiredMixin, ListView):
    model = LessonNoteModel
    template_name = 'student_portal/lesson_note/index.html'
    context_object_name = "lesson_note_list"

    def get_queryset(self):
        try:
            student = StudentsModel.objects.get(user=self.request.user)
            if student.student_class and student.class_section:
                class_info = ClassSectionInfoModel.objects.filter(
                    student_class=student.student_class, section=student.class_section
                ).first()
                if class_info:
                    return LessonNoteModel.objects.filter(
                        grant_access=True,
                        status='approved',
                        student_class=class_info
                    )
        except StudentsModel.DoesNotExist:
            return LessonNoteModel.objects.none()
        return LessonNoteModel.objects.none()


class StudentLessonNoteDetailView(LoginRequiredMixin, DetailView):
    model = LessonNoteModel
    template_name = 'student_portal/lesson_note/detail.html'
    context_object_name = "lesson_note"

