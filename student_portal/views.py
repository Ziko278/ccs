import json
from datetime import date, datetime, timedelta
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import default_storage
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
from finance.models import InvoiceModel, FeePaymentModel, FinanceSettingModel, SchoolBankDetail, StudentDiscountModel, \
    InvoiceItemModel, StudentFundingModel
from inventory.models import SaleModel
from school_setting.models import SchoolGeneralInfoModel, SchoolAcademicInfoModel, SchoolSettingModel
from student.models import StudentsModel
from academic.models import ClassSectionInfoModel, LessonNoteModel
from .forms import FeeUploadForm
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
        student = self.request.user.profile.student
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


class FeeInvoiceListView(ListView):
    model = InvoiceModel
    template_name = 'student_portal/fee/fee_list.html'
    context_object_name = 'invoices'

    def get_queryset(self):
        student = self.request.user.profile.student

        return InvoiceModel.objects.filter(
            student=student
        ).order_by('-session__start_year', '-term__order')


class AccountDetailView(TemplateView):
    model = InvoiceModel
    template_name = 'student_portal/fee/account_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['funding_account'] = SchoolSettingModel.objects.first()
        context['school_account_list'] = SchoolBankDetail.objects.all()
        return context


class FeeInvoiceDetailView(DetailView):
    model = InvoiceModel
    template_name = 'student_portal/fee/fee_invoice_detail.html'
    context_object_name = 'invoice'

    def get_queryset(self):
        # Ensure parent can only see invoices for their selected ward
        student = self.request.user.profile.student
        return InvoiceModel.objects.filter(student=student)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['invoice_items'] = self.object.items.all()
        context['invoice_discounts'] = StudentDiscountModel.objects.filter(
            invoice_item__invoice=self.object
        ).select_related('discount_application__discount')
        return context


class FeeUploadView(FormView):
    form_class = FeeUploadForm
    template_name = 'student_portal/fee/fee_upload.html'
    success_url = reverse_lazy('parent_fee_history')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        student = self.request.user.profile.student

        kwargs['student'] = student
        kwargs['upload_type'] = self.request.GET.get('type', 'fee')
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        transaction_type = self.request.GET.get('type', 'fee')
        context['transaction_type'] = transaction_type

        if transaction_type == 'wallet':
            try:
                context['funding_account'] = SchoolSettingModel.objects.first()
            except SchoolSettingModel.DoesNotExist:
                context['funding_account'] = None
            context['bank_details'] = None
        else:
            context['bank_details'] = SchoolBankDetail.objects.all()
            context['funding_account'] = None

        return context

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        target_invoice = cleaned_data.get('target_invoice')
        proof_file = self.request.FILES.get('proof_of_payment')
        payment_type = self.request.POST.get('payment_type', 'quick')  # 'quick' or 'itemized'
        student = self.request.user.profile.student

        if target_invoice:
            # --- Create FeePaymentModel for invoice payment ---
            try:
                if target_invoice.student != student:
                    messages.error(self.request, "Selected invoice does not belong to the current student.")
                    return self.form_invalid(form)

                # Save proof file
                proof_file_name = None
                if proof_file:
                    file_name = f"parent_proofs/{student.registration_number}_{target_invoice.invoice_number}_{proof_file.name}"
                    proof_file_name = default_storage.save(file_name, proof_file)

                # Get or create a default bank account for parent uploads
                bank_account = SchoolBankDetail.objects.first()
                if not bank_account:
                    messages.error(self.request, "No bank account configured. Please contact administration.")
                    return self.form_invalid(form)

                # Build notes with payment allocation details
                notes_parts = [
                    f"Parent Upload via Portal.",
                    f"Proof File: {proof_file_name or 'Not Saved'}.",
                    f"Student: {student.__str__()}",
                    f"Payment Type: {payment_type.title()}",
                    f"note: parent upload"
                ]
                
                # Handle itemized payment
                if payment_type == 'itemized':
                    item_allocations = {}
                    total_allocated = Decimal('0.00')

                    for key, value in self.request.POST.items():
                        if key.startswith('item_') and value:
                            try:
                                item_id = int(key.split('_')[1])
                                amount_for_item = Decimal(value)

                                if amount_for_item > 0:
                                    item = get_object_or_404(InvoiceItemModel, pk=item_id, invoice=target_invoice)

                                    # Don't allow overpayment on a single item
                                    payable_amount = min(amount_for_item, item.balance)

                                    if payable_amount != amount_for_item:
                                        messages.warning(
                                            self.request,
                                            f"Amount for '{item.description}' adjusted from ₦{amount_for_item:,.2f} to ₦{payable_amount:,.2f} (item balance)"
                                        )

                                    item_allocations[item_id] = {
                                        'description': item.description,
                                        'amount': float(payable_amount)
                                    }
                                    total_allocated += payable_amount

                            except (ValueError, TypeError, InvoiceItemModel.DoesNotExist):
                                continue

                    # Validate that allocated amounts match the total payment
                    if total_allocated != cleaned_data['amount']:
                        messages.error(
                            self.request,
                            f"Item allocations (₦{total_allocated:,.2f}) must equal the total amount paid (₦{cleaned_data['amount']:,.2f})"
                        )
                        return self.form_invalid(form)

                    if not item_allocations:
                        messages.error(self.request, "Please select at least one fee item to pay.")
                        return self.form_invalid(form)

                    # Store item allocations as JSON in notes
                    import json
                    notes_parts.append(f"Item Allocations: {json.dumps(item_allocations, indent=2)}")

                notes = "\n".join(notes_parts)

                FeePaymentModel.objects.create(
                    invoice=target_invoice,
                    amount=cleaned_data['amount'],
                    payment_mode=cleaned_data['method'],
                    bank_account=bank_account,
                    date=timezone.now().date(),
                    reference=cleaned_data.get('teller_number', ''),
                    status=FeePaymentModel.PaymentStatus.PENDING,
                    notes=notes,
                )

                if payment_type == 'itemized':
                    messages.success(
                        self.request,
                        f"Payment proof of ₦{cleaned_data['amount']:,.2f} for {len(item_allocations)} fee item(s) submitted. Pending review."
                    )
                else:
                    messages.success(self.request, "Payment proof for invoice submitted. Pending review.")

            except Exception as e:
                messages.error(self.request, f"Error saving invoice payment proof: {e}")
                if proof_file_name and default_storage.exists(proof_file_name):
                    default_storage.delete(proof_file_name)
                return self.form_invalid(form)

        else:
            # --- Create StudentFundingModel (Wallet) ---
            try:
                funding = StudentFundingModel(
                    student=student,
                    amount=cleaned_data['amount'],
                    method=cleaned_data['method'],
                    teller_number=cleaned_data.get('teller_number', ''),
                    proof_of_payment=proof_file,
                    status='pending',
                    mode='online',
                )
                try:
                    setting = SchoolSettingModel.objects.first()
                    if setting:
                        funding.session = setting.session
                        funding.term = setting.term
                except Exception:
                    pass

                funding.save()
                messages.success(self.request, "Wallet funding proof submitted. Pending review.")

            except Exception as e:
                messages.error(self.request, f"Error saving wallet funding proof: {e}")
                return self.form_invalid(form)

        return redirect(self.success_url)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            field_label = "__all__" if field == "__all__" else form.fields.get(field).label if form.fields.get(
                field) else field.replace('_', ' ').title()
            for error in errors:
                messages.error(self.request, f"{field_label}: {error}")
        return self.render_to_response(self.get_context_data(form=form))


class FeeUploadHistoryView(ListView):
    # --- ADD THIS LINE BACK ---
    model = StudentFundingModel # Provide a base model for ListView
    # --- END ADDITION ---
    template_name = 'student_portal/fee/fee_history.html'
    # context_object_name = 'uploads' # We are using custom context names below
    # paginate_by = 10 # Pagination across two lists is complex, handle manually if needed

    def get_context_data(self, **kwargs):
        # This calls ParentPortalMixin.get_context_data and ListView.get_context_data
        context = super().get_context_data(**kwargs)
        student = self.request.user.profile.student

        # Fetch wallet funding uploads
        wallet_uploads = StudentFundingModel.objects.filter(
            student=student,
            mode='online'
            # Add parent filter if model has it
            # parent=self.parent_obj,
        ).order_by('-created_at')

        # Fetch invoice payment uploads initiated by parent
        invoice_uploads = FeePaymentModel.objects.filter(
            invoice__student=student,
            status=FeePaymentModel.PaymentStatus.PENDING, # Show pending ones
            notes__icontains=f"parent upload" # Identify by note
            # Add parent filter if model has it
            # parent=self.parent_obj
        ).select_related('invoice').order_by('-created_at')

        context['wallet_uploads'] = wallet_uploads
        context['invoice_uploads'] = invoice_uploads

        # Remove the default queryset if ListView added it under 'object_list' or 'studentfundingmodel_list'
        context.pop('object_list', None)
        context.pop('studentfundingmodel_list', None)

        return context


# --- Shop ---
class ShopHistoryView(ListView):
    model = SaleModel
    template_name = 'parent_portal/shop_history.html'
    context_object_name = 'sales'
    paginate_by = 15

    def get_queryset(self):
        student = self.request.user.profile.student
        return SaleModel.objects.filter(
            customer=student
        ).order_by('-sale_date')

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

