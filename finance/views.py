from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.messages.views import SuccessMessageMixin, messages
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from cryptography.fernet import Fernet
import requests
from communication.models import RecentActivityModel
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from datetime import date, datetime, timedelta
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from school_setting.models import SchoolGeneralInfoModel
from django.core import serializers
from finance.templatetags.fee_custom_filters import *
from finance.urls import *
from num2words import num2words
from finance.models import *
from finance.forms import *
from django.db.models import Q


class FeeCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = FeeModel
    permission_required = 'finance.add_feemodel'
    form_class = FeeForm
    success_message = 'Fee Added Successfully'
    template_name = 'finance/fee/index.html'

    def get_success_url(self):
        return reverse('fee_index')
        # return reverse('fee_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            context['fee_list'] = FeeModel.objects.filter(type=self.request.user.profile.type).order_by('name')
        else:
            context['fee_list'] = FeeModel.objects.all().order_by('name')
        return context


class FeeListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = FeeModel
    permission_required = 'finance.view_feemodel'
    fields = '__all__'
    template_name = 'finance/fee/index.html'
    context_object_name = "fee_list"

    def get_queryset(self):
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            return FeeModel.objects.filter(type=self.request.user.profile.type)
        else:
            return FeeModel.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            context['fee_list'] = FeeModel.objects.filter(type=self.request.user.profile.type).order_by('name')
        else:
            context['fee_list'] = FeeModel.objects.all().order_by('name')
        context['form'] = FeeForm

        return context


class FeeDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = FeeModel
    permission_required = 'finance.view_feemodel'
    fields = '__all__'
    template_name = 'finance/fee/detail.html'
    context_object_name = "fee"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = FeeForm
        return context


class FeeUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = FeeModel
    permission_required = 'finance.change_feemodel'
    form_class = FeeEditForm
    success_message = 'Fee Updated Successfully'
    template_name = 'finance/fee/edit.html'

    def get_success_url(self):
        return reverse('fee_index')
        # return reverse('fee_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fee'] = self.object

        return context


class FeeDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = FeeModel
    permission_required = 'finance.delete_feemodel'
    success_message = 'Fee Deleted Successfully'
    fields = '__all__'
    template_name = 'finance/fee/delete.html'
    context_object_name = "fee"

    def get_success_url(self):
        return reverse("fee_index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class FeeGroupCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = FeeGroupModel
    permission_required = 'finance.add_feegroupmodel'
    form_class = FeeGroupForm
    success_message = 'Fee Group Added Successfully'
    template_name = 'finance/fee_group/index.html'

    def get_success_url(self):
        return reverse('fee_group_index')
        # return reverse('fee_group_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            context['fee_group_list'] = FeeGroupModel.objects.filter(type=self.request.user.profile.type).order_by('name')
        else:
            context['fee_group_list'] = FeeGroupModel.objects.all().order_by('name')
        return context


class FeeGroupListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = FeeGroupModel
    permission_required = 'finance.view_feegroupmodel'
    fields = '__all__'
    template_name = 'finance/fee_group/index.html'
    context_object_name = "fee_group_list"

    def get_queryset(self):
        return FeeGroupModel.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            context['fee_group_list'] = FeeGroupModel.objects.filter(type=self.request.user.profile.type).order_by(
                'name')
        else:
            context['fee_group_list'] = FeeGroupModel.objects.all().order_by('name')
        context['form'] = FeeGroupForm

        return context


class FeeGroupDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = FeeGroupModel
    permission_required = 'finance.view_feegroupmodel'
    fields = '__all__'
    template_name = 'finance/fee_group/detail.html'
    context_object_name = "fee_group"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = FeeGroupForm
        return context


class FeeGroupUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = FeeGroupModel
    permission_required = 'finance.change_feegroupmodel'
    form_class = FeeGroupEditForm
    success_message = 'Fee Group Updated Successfully'
    template_name = 'finance/fee_group/index.html'

    def get_success_url(self):
        return reverse('fee_group_index')
        # return reverse('fee_group_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fee_group_list'] = FeeGroupModel.objects.all()

        return context


class FeeGroupDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = FeeGroupModel
    permission_required = 'finance.delete_feegroupmodel'
    success_message = 'Fee Group Deleted Successfully'
    fields = '__all__'
    template_name = 'finance/fee_group/delete.html'
    context_object_name = "fee_group"

    def get_success_url(self):
        return reverse("fee_group_index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class FeeMasterCreateView(SuccessMessageMixin, CreateView):
    model = FeeMasterModel
    form_class = FeeMasterForm
    success_message = 'Fee Master Added Successfully'
    template_name = 'finance/fee_master/create.html'

    def get_success_url(self):
        return reverse('fee_master_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            context['fee_list'] = FeeModel.objects.filter(type=self.request.user.profile.type).order_by('name')
        else:
            context['fee_list'] = FeeModel.objects.all().order_by('name')
        return context

    def get_form_kwargs(self):
        kwargs = super(FeeMasterCreateView, self).get_form_kwargs()
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            kwargs.update({'type': self.request.user.profile.type})
        kwargs.update({'type': self.request.user.profile.type})
        return kwargs


class FeeMasterListView(ListView):
    model = FeeMasterModel
    fields = '__all__'
    template_name = 'finance/fee_master/index.html'
    context_object_name = "fee_master_list"

    def get_queryset(self):
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            return FeeMasterModel.objects.filter(type=self.request.user.profile.type).order_by('fee__name')
        else:
            return FeeMasterModel.objects.all().order_by('fee__name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class FeeMasterDetailView(DetailView):
    model = FeeMasterModel
    fields = '__all__'
    template_name = 'finance/fee_master/detail.html'
    context_object_name = "fee_master"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class FeeMasterUpdateView(SuccessMessageMixin, UpdateView):
    model = FeeMasterModel
    form_class = FeeMasterEditForm
    success_message = 'Fee Master Updated Successfully'
    template_name = 'finance/fee_master/edit.html'

    def get_success_url(self):
        return reverse('fee_master_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            context['fee_list'] = FeeModel.objects.filter(type=self.request.user.profile.type).order_by('name')
            context['student_class_list'] = ClassesModel.objects.all().order_by('name')
            context['class_section_list'] = ClassSectionModel.objects.all().order_by('name')
        else:
            context['fee_list'] = FeeModel.objects.filter(type=self.request.user.profile.type).order_by('name')
            context['student_class_list'] = ClassesModel.objects.filter(type=self.request.user.profile.type).order_by('name')
            context['class_section_list'] = ClassSectionModel.objects.all().order_by('name')
        context['group'] = self.object
        return context

    def get_form_kwargs(self):
        kwargs = super(FeeMasterUpdateView, self).get_form_kwargs()
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            kwargs.update({'type': self.request.user.profile.type})
        kwargs.update({'type': self.request.user.profile.type})
        return kwargs


class FeeMasterDeleteView(SuccessMessageMixin, DeleteView):
    model = FeeMasterModel
    success_message = 'Fee Master Deleted Successfully'
    fields = '__all__'
    template_name = 'finance/fee_master/delete.html'
    context_object_name = "fee_master"

    def get_success_url(self):
        return reverse("fee_master_index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class FeeDiscountCreateView(SuccessMessageMixin, CreateView):
    model = FeeDiscountModel
    form_class = FeeDiscountForm
    success_message = 'Fee Discount Added Successfully'
    template_name = 'finance/fee_discount/index.html'

    def get_success_url(self):
        return reverse('fee_discount_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            context['fee_discount_list'] = FeeDiscountModel.objects.filter(
                type=self.request.user.profile.type).order_by('fee_master__fee__name')
        else:
            context['fee_discount_list'] = FeeDiscountModel.objects.all().order_by('fee_master__fee__name')
        return context

    def get_form_kwargs(self):
        kwargs = super(FeeDiscountCreateView, self).get_form_kwargs()
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            kwargs.update({'type': self.request.user.profile.type})
        kwargs.update({'type': self.request.user.profile.type})
        return kwargs


class FeeDiscountListView(ListView):
    model = FeeDiscountModel
    fields = '__all__'
    template_name = 'finance/fee_discount/index.html'
    context_object_name = "fee_discount_list"

    def get_queryset(self):
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            return FeeDiscountModel.objects.filter(
                type=self.request.user.profile.type).order_by('fee_master__fee__name')
        else:
            return FeeDiscountModel.objects.all().order_by('fee_master__fee__name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        school_setting = SchoolGeneralInfoModel.objects.first()
        form_kwargs = {}
        if school_setting.separate_school_section:
            form_kwargs['type'] = self.request.user.profile.type
        context['form'] = FeeDiscountForm(**form_kwargs)

        return context


class FeeDiscountDetailView(DetailView):
    model = FeeDiscountModel
    fields = '__all__'
    template_name = 'finance/fee_discount/detail.html'
    context_object_name = "fee_discount"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class FeeDiscountUpdateView(SuccessMessageMixin, UpdateView):
    model = FeeDiscountModel
    form_class = FeeDiscountEditForm
    success_message = 'Fee Discount Updated Successfully'
    template_name = 'finance/fee_discount/edit.html'

    def get_success_url(self):
        return reverse('fee_discount_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fee_discount'] = self.object

        return context


class FeeDiscountDeleteView(SuccessMessageMixin, DeleteView):
    model = FeeDiscountModel
    success_message = 'Fee Discount Deleted Successfully'
    fields = '__all__'
    template_name = 'finance/fee_discount/delete.html'
    context_object_name = "fee_discount"

    def get_success_url(self):
        return reverse("fee_discount_index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class FeeDiscountGroupCreateView(SuccessMessageMixin, CreateView):
    model = FeeDiscountGroupModel
    form_class = FeeDiscountGroupForm
    success_message = 'Fee Discount Group Added Successfully'
    template_name = 'finance/fee_discount_group/index.html'

    def get_success_url(self):
        return reverse('fee_discount_group_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            context['fee_discount_group_list'] = FeeDiscountGroupModel.objects.filter(
                type=self.request.user.profile.type)
        else:
            context['fee_discount_group_list'] = FeeDiscountGroupModel.objects.all()

    def get_form_kwargs(self):
        kwargs = super(FeeDiscountGroupCreateView, self).get_form_kwargs()
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            kwargs.update({'type': self.request.user.profile.type})
        kwargs.update({'type': self.request.user.profile.type})
        return kwargs


class FeeDiscountGroupListView(ListView):
    model = FeeDiscountGroupModel
    fields = '__all__'
    template_name = 'finance/fee_discount_group/index.html'
    context_object_name = "fee_discount_group_list"

    def get_queryset(self):
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            return FeeDiscountGroupModel.objects.filter(type=self.request.user.profile.type)
        else:
            return FeeDiscountGroupModel.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        school_setting = SchoolGeneralInfoModel.objects.first()
        form_kwargs = {}
        if school_setting.separate_school_section:
            form_kwargs['type'] = self.request.user.profile.type
        context['form'] = FeeDiscountGroupForm(**form_kwargs)

        return context


class FeeDiscountGroupDetailView(DetailView):
    model = FeeDiscountGroupModel
    fields = '__all__'
    template_name = 'finance/fee_discount_group/detail.html'
    context_object_name = "fee_discount_group"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            context['class_list'] = ClassesModel.objects.filter(type=self.request.user.profile.type).order_by('name')
            student_list = StudentsModel.objects.filter(type=self.request.user.profile.type, status='active')
        else:
            context['class_list'] = ClassesModel.objects.all().order_by('name')
            student_list = StudentsModel.objects.filter(status='active')
        context['student_list'] = serializers.serialize("json", student_list)
        return context


class FeeDiscountGroupUpdateView(SuccessMessageMixin, UpdateView):
    model = FeeDiscountGroupModel
    form_class = FeeDiscountGroupEditForm
    success_message = 'Fee Discount Group Updated Successfully'
    template_name = 'finance/fee_discount_group/edit.html'

    def get_success_url(self):
        return reverse('fee_discount_group_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fee_discount_group'] = self.object

        return context


class FeeDiscountGroupAddBeneficiaryView(SuccessMessageMixin, UpdateView):
    model = FeeDiscountGroupModel
    form_class = FeeDiscountGroupAddBenefactorForm
    success_message = 'Fee Discount Group Updated Successfully'
    template_name = 'finance/fee_discount_group/detail.html'

    def get_success_url(self):
        return reverse('fee_discount_group_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fee_discount_group'] = self.object

        return context


def discount_add_benefactor_view(request, discount_pk, student_pk):
    discount_group = FeeDiscountGroupModel.objects.get(pk=discount_pk)
    student = StudentsModel.objects.get(pk=student_pk)
    if student in discount_group.students.all():
        messages.error(request, 'Student Already in Discount Group')
        return redirect(reverse('fee_discount_group_detail', kwargs={'pk': discount_group.pk}))
    if request.method == 'POST':
        discount_group.students.add(student)
        discount_group.save()
        messages.success(request,
                         "student {} {} added to scholarship group  successfully".format(student.surname.title(),
                                                                                        student.last_name.title()))
        return redirect(reverse('fee_discount_group_detail', kwargs={'pk': discount_group.pk}))

    context = {
        'student': student,
        'discount_group': discount_group
    }
    return render(request, 'finance/fee_discount_group/add_beneficiary.html', context)


def discount_remove_benefactor_view(request, discount_pk, student_pk):
    discount_group = FeeDiscountGroupModel.objects.get(pk=discount_pk)
    student = StudentsModel.objects.get(pk=student_pk)
    if student not in discount_group.students.all():
        messages.error(request, 'Student not in Discount Group')
        return redirect(reverse('fee_discount_group_detail', kwargs={'pk': discount_group.pk}))
    if request.method == 'POST':
        discount_group.students.remove(student)
        discount_group.save()
        messages.success(request,
                         "student {} {} has been removed from scholarship group successfully".format(student.surname.title(),
                                                                                        student.last_name.title()))
        return redirect(reverse('fee_discount_group_detail', kwargs={'pk': discount_group.pk}))

    context = {
        'student': student,
        'discount_group': discount_group
    }
    return render(request, 'finance/fee_discount_group/remove_beneficiary.html', context)


class FeeDiscountGroupDeleteView(SuccessMessageMixin, DeleteView):
    model = FeeDiscountGroupModel
    success_message = 'Fee Discount Group Deleted Successfully'
    fields = '__all__'
    template_name = 'finance/fee_discount_group/delete.html'
    context_object_name = "fee_discount_group"

    def get_success_url(self):
        return reverse("fee_discount_group_index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class FeePenaltyCreateView(SuccessMessageMixin, CreateView):
    model = FeePenaltyModel
    form_class = FeePenaltyForm
    success_message = 'Fee Penalty Added Successfully'
    template_name = 'finance/fee_penalty/index.html'

    def get_success_url(self):
        return reverse('fee_penalty_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            context['fee_penalty_list'] = FeePenaltyModel.objects.filter(
                type=self.request.user.profile.type).order_by('fee_master__fee__name')
        else:
            context['fee_penalty_list'] = FeePenaltyModel.objects.all().order_by('fee_master__fee__name')
        return context

    def get_form_kwargs(self):
        kwargs = super(FeePenaltyCreateView, self).get_form_kwargs()
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            kwargs.update({'type': self.request.user.profile.type})
        kwargs.update({'type': self.request.user.profile.type})
        return kwargs


class FeePenaltyListView(ListView):
    model = FeePenaltyModel
    fields = '__all__'
    template_name = 'finance/fee_penalty/index.html'
    context_object_name = "fee_penalty_list"

    def get_queryset(self):
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            return FeePenaltyModel.objects.filter(
                type=self.request.user.profile.type).order_by('fee_master__fee__name')
        else:
            return FeePenaltyModel.objects.all().order_by('fee_master__fee__name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        school_setting = SchoolGeneralInfoModel.objects.first()
        form_kwargs = {}
        if school_setting.separate_school_section:
            form_kwargs['type'] = self.request.user.profile.type
        context['form'] = FeePenaltyForm(**form_kwargs)

        return context


class FeePenaltyDetailView(DetailView):
    model = FeePenaltyModel
    fields = '__all__'
    template_name = 'finance/fee_penalty/detail.html'
    context_object_name = "fee_penalty"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class FeePenaltyUpdateView(SuccessMessageMixin, UpdateView):
    model = FeePenaltyModel
    form_class = FeePenaltyEditForm
    success_message = 'Fee Penalty Updated Successfully'
    template_name = 'finance/fee_penalty/edit.html'

    def get_success_url(self):
        return reverse('fee_penalty_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fee_penalty'] = self.object

        return context


class FeePenaltyDeleteView(SuccessMessageMixin, DeleteView):
    model = FeePenaltyModel
    success_message = 'Fee Penalty Deleted Successfully'
    fields = '__all__'
    template_name = 'finance/fee_penalty/delete.html'
    context_object_name = "fee_penalty"

    def get_success_url(self):
        return reverse("fee_penalty_index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class FeeReminderCreateView(SuccessMessageMixin, CreateView):
    model = FeeReminderModel
    form_class = FeeReminderForm
    success_message = 'Fee Reminder Added Successfully'
    template_name = 'finance/fee_reminder/index.html'

    def get_success_url(self):
        return reverse('fee_reminder_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fee_reminder_list'] = FeeReminderModel.objects.all()
        return context


class FeeReminderListView(ListView):
    model = FeeReminderModel
    fields = '__all__'
    template_name = 'finance/fee_reminder/index.html'
    context_object_name = "fee_reminder_list"

    def get_queryset(self):
        return FeeReminderModel.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fee_reminder_list'] = FeeReminderModel.objects.all()
        context['form'] = FeeReminderForm

        return context


class FeeReminderDetailView(DetailView):
    model = FeeReminderModel
    fields = '__all__'
    template_name = 'finance/fee_reminder/detail.html'
    context_object_name = "fee_reminder"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = FeeReminderForm
        return context


class FeeReminderUpdateView(SuccessMessageMixin, UpdateView):
    model = FeeReminderModel
    form_class = FeeReminderEditForm
    success_message = 'Fee Reminder Updated Successfully'
    template_name = 'finance/fee_reminder/index.html'

    def get_success_url(self):
        return reverse('fee_reminder_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fee_reminder_list'] = FeeReminderModel.objects.all()

        return context


class FeeReminderDeleteView(SuccessMessageMixin, DeleteView):
    model = FeeReminderModel
    success_message = 'Fee Reminder Deleted Successfully'
    fields = '__all__'
    template_name = 'finance/fee_reminder/delete.html'
    context_object_name = "fee_reminder"

    def get_success_url(self):
        return reverse("fee_reminder_index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class FeePaymentSelectStudentView(LoginRequiredMixin, SuccessMessageMixin, TemplateView):
    template_name = 'finance/fee_payment/select_student.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            context['class_list'] = ClassesModel.objects.filter(type=self.request.user.profile.type).order_by('name')
            student_list = StudentsModel.objects.filter(type=self.request.user.profile.type)
        else:
            context['class_list'] = ClassesModel.objects.all().order_by('name')
            student_list = StudentsModel.objects.all()
        context['student_list'] = serializers.serialize("json", student_list)
        return context


class FeePaymentCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = FeePaymentModel
    form_class = FeePaymentForm
    success_message = 'Fee Payment Successful'
    template_name = 'finance/fee_payment/create.html'

    def get_success_url(self):
        return reverse('fee_payment_summary_create', kwargs={'payment_pk': self.object.pk,
                                                             'student_pk': self.object.student.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        student_pk = self.kwargs.get('student_pk')
        student = get_object_or_404(StudentsModel, pk=student_pk)
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
                if student.is_new:
                    one_time_fee_list = FeeMasterModel.objects.filter(type=self.request.user.profile.type,
                                                                      student_class__in=[student_class.id],
                                                                      class_section__in=[class_section.id]).exclude(
                        fee__fee_occurrence='termly').filter(
                        Q(fee__payment_term='any term') | Q(fee__payment_term=academic_setting.term))

                else:
                    one_time_fee_list = FeeMasterModel.objects.filter(type=self.request.user.profile.type,
                                                                      student_class__in=[student_class.id],
                                                                      class_section__in=[class_section.id]).exclude(
                        fee__fee_occurrence='termly').exclude(is_new=True).filter(
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
                if student.is_new:
                    one_time_fee_list = FeeMasterModel.objects.filter(student_class__in=[student_class.id],
                                                                      class_section__in=[class_section.id]).exclude(
                        fee__fee_occurrence='termly').filter(
                        Q(fee__payment_term='any term') | Q(fee__payment_term=academic_setting.term))

                else:
                    one_time_fee_list = FeeMasterModel.objects.filter(student_class__in=[student_class.id],
                                                                      class_section__in=[class_section.id]).exclude(
                        fee__fee_occurrence='termly').exclude(is_new=True).filter(
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


def create_fee__payment_summary(request, payment_pk, student_pk):
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
            mail_subject = f'NEW TELLER OF ₦{payment.amount} UPLOAD BY ACCOUNTANT'
            message = f"""
            The Accountant just uploaded fee payment teller
            for the sum of {num2words(payment.amount)} naira (₦{payment.amount})
            being payment for {fee_payment_summary.fee_list()}
            by {fee_payment_summary.student.__str__()}
            """
            send_mail(mail_subject, message, 'odekeziko@gmail.com', ['accounts@whitecloudschool.sch.ng'],
                      fail_silently=True)
        except Exception:
            pass

    return redirect(reverse('fee_payment_create', kwargs={'student_pk': student_pk}))


def bulk_payment_create_view(request):
    if request.method == 'POST':
        fee_list = request.POST.getlist('fee[]')
        amount_list = request.POST.getlist('amount[]')
        payment_mode_list = request.POST.getlist('payment_mode[]')
        student_pk = request.POST.get('student')
        type = request.POST.get('type')
        vat = request.POST.get('vat')
        payment_date = request.POST.get('date')
        payment_proof = request.POST.get('payment_proof')

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
                    if fee_setting.use_2fa_manual:
                        status = 'pending'
                    else:
                        status = 'confirmed'
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
            subject = "<b>{} {}</b> paid <b>N{}</b> for <b>{}</b>".format(student.surname.title(),
                                                                          student.last_name.title(), total_amount,
                                                                          payment_purpose)
            activity = RecentActivityModel.objects.create(category=category, subject=subject,
                                                          reference_id=fee_payment_summary.id, type=student.type,
                                                          session=session, term=term)

            activity.save()

            try:
                mail_subject = f'NEW TELLER OF ₦{total_amount} UPLOADED BY ACCOUNTANT'
                message = f"""
                The Accountant just uploaded fee payment teller
                for the sum of {num2words(total_amount)} naira (₦{total_amount})
                been payment for {fee_payment_summary.fee_list()}
                by {fee_payment_summary.student.__str__()}
                """
                send_mail(mail_subject, message, 'odekeziko@gmail.com', ['accounts@whitecloudschool.sch.ng'],
                          fail_silently=True)
            except Exception:
                pass

            messages.success(request, 'Fee Payment Successful')
            return redirect(reverse('fee_payment_create', kwargs={'student_pk': student.pk}))
        else:
            messages.error(request, 'Error Processing Payments, Try Later')

    messages.error(request, 'method not supported, try again')
    return redirect(reverse('fee_select_student'))


def fee_payment_list_view(request):
    session_id = request.GET.get('session', None)
    session = SessionModel.objects.get(id=session_id)
    session_list = SessionModel.objects.all()
    term = request.GET.get('term', None)
    fee_payment_list = FeePaymentSummaryModel.objects.filter(session=session, term=term).order_by('-id')
    context = {
        'fee_payment_list': fee_payment_list,
        'session': session,
        'term': term,
        'session_list': session_list
    }
    return render(request, 'finance/fee_payment/index.html', context)


def confirm_bulk_fee_payment_view(request, pk):
    if request.method == 'POST' and request.user.is_superuser:
        fee_payment = FeePaymentSummaryModel.objects.get(pk=pk)
        if fee_payment.status == 'confirmed':
            messages.warning(request, 'Fee Already Confirmed')
        else:
            for payment in fee_payment.fees.all():
                payment.status = 'confirmed'
                payment.save()
            fee_payment.status = 'confirmed'
            fee_payment.save()

            messages.success(request, 'Fee Payment Confirmed Successfully')

            try:
                mail_subject = f'CONFIRMATION OF PAYMENT OF ₦{fee_payment.amount} FOR {fee_payment.student.__str__().upper()} '
                message = f"""
                The Accountant just Confirmed the payment of
                the sum of {num2words(fee_payment.amount)} naira (₦{fee_payment.amount})
                been payment for {fee_payment.fee_list()}
                by {fee_payment.student.__str__()}
                """
                send_mail(mail_subject, message, 'odekeziko@gmail.com', ['accounts@whitecloudschool.sch.ng'],
                          fail_silently=True)
            except Exception:
                pass

        return redirect(reverse('fee_payment_create', kwargs={'student_pk': fee_payment.student.pk}))
    messages.error(request, 'Invalid Request, Try Again')
    return redirect(reverse('fee_select_student'))


def confirm_fee_payment_view(request, pk):
    if request.method == 'POST' and request.user.is_superuser:
        fee_payment = FeePaymentModel.objects.get(pk=pk)
        if fee_payment.status == 'confirmed':
            messages.warning(request, 'Fee Already Confirmed')
        else:
            fee_payment.status = 'confirmed'
            fee_payment.save()
            payment_summary = FeePaymentSummaryModel.objects.filter(fees__in=[fee_payment.id]).first()
            all_confirmed = True
            for payment in payment_summary.fees.all():
                if payment.status == 'pending':
                    all_confirmed = False
                    break
            if all_confirmed:
                payment_summary.status = 'confirmed'
                payment_summary.save()

            messages.success(request, 'Fee Payment Confirmed Successfully')
            try:
                mail_subject = f'CONFIRMATION OF PAYMENT OF ₦{fee_payment.amount} FOR {fee_payment.student.__str__().upper()} '
                message = f"""
                The Accountant just Confirmed the payment of
                the sum of {num2words(fee_payment.amount)} naira (₦{fee_payment.amount})
                been payment for {fee_payment.fee_list()}
                by {fee_payment.student.__str__()}
                """
                send_mail(mail_subject, message, 'odekeziko@gmail.com', ['accounts@whitecloudschool.sch.ng'],
                          fail_silently=True)
            except Exception:
                pass

        return redirect(reverse('fee_payment_create', kwargs={'student_pk': fee_payment.student.pk}))
    messages.error(request, 'Invalid Request, Try Again')
    return redirect(reverse('fee_select_student'))


def revert_bulk_fee_payment_view(request, pk):
    if request.method == 'POST' and request.user.is_superuser:
        fee_payment = FeePaymentSummaryModel.objects.get(pk=pk)
        for payment in fee_payment.fees.all():
            payment.delete()
        fee_payment.delete()
        messages.success(request, 'Fee Payment Reverted Successfully')
        return redirect(reverse('fee_payment_create', kwargs={'student_pk': fee_payment.student.pk}))
    messages.error(request, 'Invalid Request, Try Again')
    return redirect(reverse('fee_select_student'))


def revert_fee_payment_view(request, pk):
    if request.method == 'POST' and request.user.is_superuser:
        fee_payment = FeePaymentModel.objects.get(pk=pk)
        payment_summary = FeePaymentSummaryModel.objects.filter(fees__in=[fee_payment.id]).first()
        fee_payment.delete()
        if payment_summary:
            if len(payment_summary.fees.all()) == 0:
                payment_summary.delete()
        messages.success(request, 'Fee Payment Reverted Successfully')
        return redirect(reverse('fee_payment_create', kwargs={'student_pk': fee_payment.student.pk}))
    messages.error(request, 'Invalid Request, Try Again')
    return redirect(reverse('fee_select_student'))


def fee_get_class_students(request):
    class_pk = request.GET.get('class_pk')
    section_pk = request.GET.get('section_pk')

    student_list = StudentsModel.objects.filter(student_class=class_pk, class_section=section_pk)
    result = ''
    for student in student_list:
        if student.middle_name:
            full_name = "{} {} {}".format(student.surname.title(), student.middle_name.title(), student.last_name.title())
        else:
            full_name = "{} {}".format(student.surname.title(), student.last_name.title())
        result += """<li class='list-group-item select_student d-flex justify-content-between align-items-center' student_id='{}'>
        {} </li>""".format(student.id, full_name)
    if result == '':
        result += """<li class='list-group-item  d-flex justify-content-between align-items-center bg-danger text-white'>
        No Student in Selected Class</li>"""
    return HttpResponse(result)


def fee_get_class_students_by_reg_number(request):
    reg_no = request.GET.get('reg_no')

    student_list = StudentsModel.objects.filter(registration_number__contains=reg_no)
    result = ''
    for student in student_list:
        if student.middle_name:
            full_name = "{} {} {}".format(student.surname.title(), student.middle_name.title(), student.last_name.title())
        else:
            full_name = "{} {}".format(student.surname.title(), student.last_name.title())
        result += """<li class='list-group-item select_student d-flex justify-content-between align-items-center' student_id={}>
        {} </li>""".format(student.id, full_name)
    if result == '':
        result += """<li class='list-group-item d-flex justify-content-between align-items-center bg-danger text-white'>
        No Student in with inputed Registration Number</li>"""
    return HttpResponse(result)


class FeePaymentListView(ListView):
    model = FeePaymentModel
    fields = '__all__'
    template_name = 'finance/fee_payment/index.html'
    context_object_name = "fee_payment_list"

    def get_queryset(self):
        return FeePaymentModel.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fee_payment_list'] = FeePaymentModel.objects.all()
        context['form'] = FeePaymentForm

        return context


class FeePaymentDetailView(DetailView):
    model = FeePaymentSummaryModel
    fields = '__all__'
    template_name = 'finance/fee_payment/detail.html'
    context_object_name = "fee_payment"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['amount_in_word'] = num2words(self.object.amount)
        context['general_setting'] = SchoolGeneralInfoModel.objects.first()
        return context


class FeePaymentUpdateView(SuccessMessageMixin, UpdateView):
    model = FeePaymentModel
    form_class = FeePaymentEditForm
    success_message = 'Fee Payment Updated Successfully'
    template_name = 'finance/fee_payment/index.html'

    def get_success_url(self):
        return reverse('fee_payment_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fee_payment_list'] = FeePaymentModel.objects.all()

        return context


class FeePaymentDeleteView(SuccessMessageMixin, DeleteView):
    model = FeePaymentModel
    success_message = 'Fee Payment Deleted Successfully'
    fields = '__all__'
    template_name = 'finance/fee_payment/delete.html'
    context_object_name = "fee_payment"

    def get_success_url(self):
        return reverse("fee_payment_index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class OnlinePaymentCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = OnlinePaymentModel
    permission_required = 'finance.add_feegroupmodel'
    form_class = OnlinePaymentForm
    success_message = 'Payment Method Added Successfully'
    template_name = 'finance/online_payment/index.html'

    def get_success_url(self):
        return reverse('online_payment_index')
        # return reverse('online_payment_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            context['online_payment_list'] = OnlinePaymentModel.objects.filter(type=self.request.user.profile.type).order_by('name')
        else:
            context['fee_group_list'] = OnlinePaymentModel.objects.all().order_by('name')
        return context


class OnlinePaymentListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = OnlinePaymentModel
    permission_required = 'finance.view_feegroupmodel'
    fields = '__all__'
    template_name = 'finance/online_payment/index.html'
    context_object_name = "online_payment_list"

    def get_queryset(self):
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            return OnlinePaymentModel.objects.filter(type=self.request.user.profile.type).order_by('name')
        else:
            return OnlinePaymentModel.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = OnlinePaymentForm

        return context


class OnlinePaymentDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = OnlinePaymentModel
    permission_required = 'finance.view_feegroupmodel'
    fields = '__all__'
    template_name = 'finance/online_payment/detail.html'
    context_object_name = "method"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        key = self.object.key
        fernet = Fernet(key)
        context['public_key'] = fernet.decrypt(self.object.public_key.encode()).decode()
        context['private_key'] = fernet.decrypt(self.object.private_key.encode()).decode()
        return context


class OnlinePaymentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = OnlinePaymentModel
    permission_required = 'finance.change_feegroupmodel'
    form_class = OnlinePaymentEditForm
    success_message = 'Online Payment Method Updated Successfully'
    template_name = 'finance/online_payment/index.html'

    def get_success_url(self):
        return reverse('online_payment_index')
        # return reverse('fee_group_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            context['online_payment_list'] = OnlinePaymentModel.objects.filter(
                type=self.request.user.profile.type).order_by('name')
        else:
            context['fee_group_list'] = OnlinePaymentModel.objects.all().order_by('name')

        return context


class OnlinePaymentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = OnlinePaymentModel
    permission_required = 'finance.delete_feegroupmodel'
    success_message = 'Online Payment Method Deleted Successfully'
    fields = '__all__'
    template_name = 'finance/online_payment/delete.html'
    context_object_name = "online_payment"

    def get_success_url(self):
        return reverse("online_payment_index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ExpenseCategoryCreateView(SuccessMessageMixin, CreateView):
    model = ExpenseCategoryModel
    form_class = ExpenseCategoryForm
    success_message = 'Expense Category Added Successfully'
    template_name = 'finance/expense_category/index.html'

    def get_success_url(self):
        return reverse('expense_category_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            context['expense_category_list'] = ExpenseCategoryModel.objects.filter(
                type=self.request.user.profile.type).order_by('name')
        else:
            context['expense_category_list'] = ExpenseCategoryModel.objects.all().order_by('name')
        return context


class ExpenseCategoryListView(ListView):
    model = ExpenseCategoryModel
    fields = '__all__'
    template_name = 'finance/expense_category/index.html'
    context_object_name = "expense_category_list"

    def get_queryset(self):
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            return ExpenseCategoryModel.objects.filter(type=self.request.user.profile.type).order_by('name')
        return ExpenseCategoryModel.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ExpenseCategoryForm

        return context


class ExpenseCategoryUpdateView(SuccessMessageMixin, UpdateView):
    model = ExpenseCategoryModel
    form_class = ExpenseCategoryEditForm
    success_message = 'Expense Category Updated Successfully'
    template_name = 'finance/expense_category/index.html'

    def get_success_url(self):
        return reverse('expense_category_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            context['expense_category_list'] = ExpenseCategoryModel.objects.filter(
                type=self.request.user.profile.type).order_by('name')
        else:
            context['expense_category_list'] = ExpenseCategoryModel.objects.all().order_by('name')

        return context


class ExpenseCategoryDeleteView(SuccessMessageMixin, DeleteView):
    model = ExpenseCategoryModel
    success_message = 'Expense Category Deleted Successfully'
    fields = '__all__'
    template_name = 'finance/expense_category/delete.html'
    context_object_name = "expense_category"

    def get_success_url(self):
        return reverse("expense_category_index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ExpenseTypeCreateView(SuccessMessageMixin, CreateView):
    model = ExpenseTypeModel
    form_class = ExpenseTypeForm
    success_message = 'Expense Type Added Successfully'
    template_name = 'finance/expense_type/index.html'

    def get_success_url(self):
        return reverse('expense_type_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            context['expense_category_list'] = ExpenseCategoryModel.objects.filter(
                type=self.request.user.profile.type).order_by('name')
            context['expense_type_list'] = ExpenseTypeModel.objects.filter(
                type=self.request.user.profile.type).order_by('name')
        else:
            context['expense_category_list'] = ExpenseCategoryModel.objects.all().order_by('name')
            context['expense_type_list'] = ExpenseTypeModel.objects.all().order_by('name')
        context = super().get_context_data(**kwargs)

        return context

    def get_form_kwargs(self):
        kwargs = super(ExpenseTypeCreateView, self).get_form_kwargs()
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            kwargs.update({'type': self.request.user.profile.type})
        kwargs.update({'type': self.request.user.profile.type})
        return kwargs


class ExpenseTypeListView(ListView):
    model = ExpenseTypeModel
    fields = '__all__'
    template_name = 'finance/expense_type/index.html'
    context_object_name = "expense_type_list"

    def get_queryset(self):
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            return ExpenseTypeModel.objects.filter(
                type=self.request.user.profile.type).order_by('name')
        else:
            return ExpenseTypeModel.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        form_kwargs = {}
        if school_setting.separate_school_section:
            context['expense_category_list'] = ExpenseCategoryModel.objects.filter(
                type=self.request.user.profile.type).order_by('name')
            form_kwargs['type'] = self.request.user.profile.type
        else:
            context['expense_category_list'] = ExpenseCategoryModel.objects.all().order_by('name')

        context['form'] = ExpenseTypeForm(**form_kwargs)

        return context


class ExpenseTypeUpdateView(SuccessMessageMixin, UpdateView):
    model = ExpenseTypeModel
    form_class = ExpenseTypeEditForm
    success_message = 'Expense Type Updated Successfully'
    template_name = 'finance/expense_type/index.html'

    def get_success_url(self):
        return reverse('expense_type_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            context['expense_category_list'] = ExpenseCategoryModel.objects.filter(
                type=self.request.user.profile.type).order_by('name')
            context['expense_type_list'] = ExpenseTypeModel.objects.filter(
                type=self.request.user.profile.type).order_by('name')
        else:
            context['expense_category_list'] = ExpenseCategoryModel.objects.all().order_by('name')
            context['expense_type_list'] = ExpenseTypeModel.objects.all().order_by('name')
        context = super().get_context_data(**kwargs)

        return context

    def get_form_kwargs(self):
        kwargs = super(ExpenseTypeUpdateView, self).get_form_kwargs()
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            kwargs.update({'type': self.request.user.profile.type})
        kwargs.update({'type': self.request.user.profile.type})
        return kwargs


class ExpenseTypeDeleteView(SuccessMessageMixin, DeleteView):
    model = ExpenseTypeModel
    success_message = 'Expense Type Deleted Successfully'
    fields = '__all__'
    template_name = 'finance/expense_type/delete.html'
    context_object_name = "expense_type"

    def get_success_url(self):
        return reverse("expense_type_index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ExpenseCreateView(SuccessMessageMixin, CreateView):
    model = ExpenseModel
    form_class = ExpenseForm
    success_message = 'Expense Added Successfully'
    template_name = 'finance/expense/create.html'

    def get_success_url(self):
        return reverse('expense_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            context['category_list'] = ExpenseCategoryModel.objects.filter(type=self.request.user.profile.type).order_by(
                'name')
        else:
            context['category_list'] = ExpenseCategoryModel.objects.all().order_by('name')
        return context

    def get_form_kwargs(self):
        kwargs = super(ExpenseCreateView, self).get_form_kwargs()
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            kwargs.update({'type': self.request.user.profile.type})
        kwargs.update({'type': self.request.user.profile.type})
        return kwargs


class ExpenseListView(ListView):
    model = ExpenseModel
    fields = '__all__'
    template_name = 'finance/expense/index.html'
    context_object_name = "expense_list"

    def get_queryset(self):
        school_setting = SchoolGeneralInfoModel.objects.first()
        session_id = self.request.GET.get('session')
        session = SessionModel.objects.get(pk=session_id)
        term = self.request.GET.get('term')
        if school_setting.separate_school_section:
            return ExpenseModel.objects.filter(type=self.request.user.profile.type, session=session, term=term).order_by(
                'category__name')
        else:
            return ExpenseModel.objects.filter(session=session, term=term).order_by('category__name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        session_id = self.request.GET.get('session')
        context['current_session'] = SessionModel.objects.get(pk=session_id)
        context['session_list'] = SessionModel.objects.all()
        context['term'] = self.request.GET.get('term')
        return context


class ExpenseDetailView(DetailView):
    model = ExpenseModel
    fields = '__all__'
    template_name = 'finance/expense/detail.html'
    context_object_name = "expense"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ExpenseUpdateView(SuccessMessageMixin, UpdateView):
    model = ExpenseModel
    form_class = ExpenseEditForm
    success_message = 'Expense Updated Successfully'
    template_name = 'finance/expense/edit.html'

    def get_success_url(self):
        return reverse('expense_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['expense'] = self.object
        return context

    def get_form_kwargs(self):
        kwargs = super(ExpenseUpdateView, self).get_form_kwargs()
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            kwargs.update({'type': self.request.user.profile.type})
        kwargs.update({'type': self.request.user.profile.type})
        return kwargs


class ExpenseDeleteView(SuccessMessageMixin, DeleteView):
    model = ExpenseModel
    success_message = 'Expense Deleted Successfully'
    fields = '__all__'
    template_name = 'finance/expense/delete.html'
    context_object_name = "expense"

    def get_success_url(self):
        return reverse("expense_index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class IncomeCategoryCreateView(SuccessMessageMixin, CreateView):
    model = IncomeCategoryModel
    form_class = IncomeCategoryForm
    success_message = 'Income Category Added Successfully'
    template_name = 'finance/income_category/index.html'

    def get_success_url(self):
        return reverse('income_category_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            context['income_category_list'] = IncomeCategoryModel.objects.filter(
                type=self.request.user.profile.type).order_by('name')
        else:
            context['income_category_list'] = IncomeCategoryModel.objects.all().order_by('name')
        return context


class IncomeCategoryListView(ListView):
    model = IncomeCategoryModel
    fields = '__all__'
    template_name = 'finance/income_category/index.html'
    context_object_name = "income_category_list"

    def get_queryset(self):
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            return IncomeCategoryModel.objects.filter(type=self.request.user.profile.type).order_by('name')
        return IncomeCategoryModel.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = IncomeCategoryForm
        return context


class IncomeCategoryUpdateView(SuccessMessageMixin, UpdateView):
    model = IncomeCategoryModel
    form_class = IncomeCategoryEditForm
    success_message = 'Income Category Updated Successfully'
    template_name = 'finance/income_category/index.html'

    def get_success_url(self):
        return reverse('income_category_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            context['income_category_list'] = IncomeCategoryModel.objects.filter(
                type=self.request.user.profile.type).order_by('name')
        else:
            context['income_category_list'] = IncomeCategoryModel.objects.all().order_by('name')
        return context


class IncomeCategoryDeleteView(SuccessMessageMixin, DeleteView):
    model = IncomeCategoryModel
    success_message = 'Income Category Deleted Successfully'
    fields = '__all__'
    template_name = 'finance/income_category/delete.html'
    context_object_name = "income_category"

    def get_success_url(self):
        return reverse("income_category_index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class IncomeSourceCreateView(SuccessMessageMixin, CreateView):
    model = IncomeSourceModel
    form_class = IncomeSourceForm
    success_message = 'Income Source Added Successfully'
    template_name = 'finance/income_source/index.html'

    def get_success_url(self):
        return reverse('income_source_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            context['income_source_list'] = IncomeSourceModel.objects.filter(
                type=self.request.user.profile.type).order_by('name')
        else:
            context['income_source_list'] = IncomeSourceModel.objects.all().order_by('name')
        return context


class IncomeSourceListView(ListView):
    model = IncomeSourceModel
    fields = '__all__'
    template_name = 'finance/income_source/index.html'
    context_object_name = "income_source_list"

    def get_queryset(self):
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            return IncomeSourceModel.objects.filter(type=self.request.user.profile.type).order_by('name')
        else:
            return IncomeSourceModel.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = IncomeSourceForm

        return context


class IncomeSourceUpdateView(SuccessMessageMixin, UpdateView):
    model = IncomeSourceModel
    form_class = IncomeSourceEditForm
    success_message = 'Income Source Updated Successfully'
    template_name = 'finance/income_source/index.html'

    def get_success_url(self):
        return reverse('income_source_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            context['income_source_list'] = IncomeSourceModel.objects.filter(
                type=self.request.user.profile.type).order_by('name')
        else:
            context['income_source_list'] = IncomeSourceModel.objects.all().order_by('name')

        return context


class IncomeSourceDeleteView(SuccessMessageMixin, DeleteView):
    model = IncomeSourceModel
    success_message = 'Income Source Deleted Successfully'
    fields = '__all__'
    template_name = 'finance/income_source/delete.html'
    context_object_name = "income_source"

    def get_success_url(self):
        return reverse("income_source_index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class IncomeCreateView(SuccessMessageMixin, CreateView):
    model = IncomeModel
    form_class = IncomeForm
    success_message = 'Income Added Successfully'
    template_name = 'finance/income/create.html'

    def get_success_url(self):
        return reverse('income_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_form_kwargs(self):
        kwargs = super(IncomeCreateView, self).get_form_kwargs()
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            kwargs.update({'type': self.request.user.profile.type})
        kwargs.update({'type': self.request.user.profile.type})
        return kwargs


class IncomeListView(ListView):
    model = IncomeModel
    fields = '__all__'
    template_name = 'finance/income/index.html'
    context_object_name = "income_list"

    def get_queryset(self):
        school_setting = SchoolGeneralInfoModel.objects.first()
        session_id = self.request.GET.get('session')
        session = SessionModel.objects.get(pk=session_id)
        term = self.request.GET.get('term')
        if school_setting.separate_school_section:
            return IncomeModel.objects.filter(type=self.request.user.profile.type, session=session, term=term).order_by(
                'category__name')
        else:
            return IncomeModel.objects.filter(session=session, term=term).order_by('category__name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        session_id = self.request.GET.get('session')
        context['current_session'] = SessionModel.objects.get(pk=session_id)
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            context['session_list'] = SessionModel.objects.filter(type=self.request.user.profile.type)
        else:
            context['session_list'] = SessionModel.objects.all()

        context['term'] = self.request.GET.get('term')
        return context


class IncomeDetailView(DetailView):
    model = IncomeModel
    fields = '__all__'
    template_name = 'finance/income/detail.html'
    context_object_name = "income"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class IncomeUpdateView(SuccessMessageMixin, UpdateView):
    model = IncomeModel
    form_class = IncomeEditForm
    success_message = 'Income Updated Successfully'
    template_name = 'finance/income/edit.html'

    def get_success_url(self):
        return reverse('income_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['income'] = self.object
        return context

    def get_form_kwargs(self):
        kwargs = super(IncomeUpdateView, self).get_form_kwargs()
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            kwargs.update({'type': self.request.user.profile.type})
        kwargs.update({'type': self.request.user.profile.type})
        return kwargs


class IncomeDeleteView(SuccessMessageMixin, DeleteView):
    model = IncomeModel
    success_message = 'Income Deleted Successfully'
    fields = '__all__'
    template_name = 'finance/income/delete.html'
    context_object_name = "income"

    def get_success_url(self):
        return reverse("income_index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@login_required
@csrf_exempt
def verfiy_paystack_payment(request):
    if 'reference' in request.GET:
        reference = request.GET['reference']
        url = "https://api.paystack.co/transaction/verify/{}".format(reference)

        type = request.user.profile.student.type
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            paystack_secret_key = OnlinePaymentModel.objects.filter(type=type, name='paystack').first()
            payment_setting = FinanceSettingModel.objects.filter(type=type).first()
        else:
            paystack_secret_key = OnlinePaymentModel.objects.filter(name='paystack').first()
            payment_setting = FinanceSettingModel.objects.first()
        key = paystack_secret_key.key
        fernet = Fernet(key)
        secret_key = fernet.decrypt(paystack_secret_key.private_key.encode()).decode()

        headers = {
            "Authorization": f"Bearer {secret_key}",
            "Content-Type": "application/json",
        }
        response = requests.request("GET", url, headers=headers)
        response = response.json()

        meta_data = response["data"]["metadata"]
        reference = meta_data["reference"]

        if response["status"]:
            payment_exist = FeePaymentModel.objects.filter(reference=reference)
            if payment_exist:
                messages.warning(request, 'Payment already Processed, Thank You')
                return redirect(reverse('student_dashboard'))

            method = meta_data["method"].lower()
            student_id = meta_data["student_id"]
            fee_id = meta_data["fee_id"]
            vat = float(meta_data["vat"])
            term = meta_data["term"]
            session_id = meta_data["session_id"]
            amount = float(meta_data["amount"])/100
            status = 'confirmed'

            fee = FeeMasterModel.objects.get(pk=fee_id)
            student = StudentsModel.objects.get(pk=student_id)
            session = SessionModel.objects.get(pk=session_id)
            if payment_setting.use_2fa_online:
                status = 'pending'
            payment = FeePaymentModel.objects.create(fee=fee, student=student, session=session, term=term,
                                                     payment_mode='online', online_payment_method=method, vat=vat,
                                                     amount=amount, reference=reference, type=type, status=status)
            payment.save()
            if payment.id:
                messages.success(request, 'N{} Payment Processed Successfully'.format(amount))
                context = {
                    'status': 'success',
                    'payment': payment,
                    'student': student,
                    'fee': fee,
                    'amount_in_word': num2words(amount)
                }
            else:
                context = {
                    'status': 'fail',
                    'reference': reference
                }
            return render(request, 'finance/online_payment/payment_done.html', context)

        else:
            if response.data.status == 'failed':
                messages.error(request, 'Payment Processing Failed, Try Later')
            elif response.data.status == 'pending':
                messages.warning(request, 'Payment Processing Pending, Please wait while we try to process the payment')
            else:
                messages.warning(request,
                                 'Payment Status not known. Please if you have been charged, wait a while for it to be resolved')
            return redirect(reverse('student_fee'))
    else:
        messages.warning(request, 'Invalid Transaction Link')
        return redirect(reverse('student_fee'))


@login_required
@csrf_exempt
def verfiy_flutterwave_payment(request):
    if 'transaction_id' in request.GET:
        reference = request.GET['transaction_id']
        url = "https://api.flutterwave.com/v3/transactions/{}/verify".format(reference)

        type = request.user.profile.student.type
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            flutterwave_secret_key = OnlinePaymentModel.objects.filter(type=type, name='flutterwave').first()
            payment_setting = FinanceSettingModel.objects.filter(type=type).first()
        else:
            flutterwave_secret_key = OnlinePaymentModel.objects.filter(name='flutterwave').first()
            payment_setting = FinanceSettingModel.objects.first()
        key = flutterwave_secret_key.key
        fernet = Fernet(key)
        secret_key = fernet.decrypt(flutterwave_secret_key.private_key.encode()).decode()

        headers = {
            "Authorization": f"Bearer {secret_key}",
        }
        response = requests.request("GET", url, headers=headers)
        response = response.json()

        meta_data = response["data"]["meta"]
        reference = meta_data["reference"]

        if response["status"]:
            payment_exist = FeePaymentModel.objects.filter(reference=reference)
            if payment_exist:
                messages.warning(request, 'Payment already Processed, Thank You')
                return redirect(reverse('student_dashboard'))

            method = meta_data["method"].lower()
            student_id = meta_data["student_id"]
            fee_id = meta_data["fee_id"]
            vat = float(meta_data["vat"])
            term = meta_data["term"]
            session_id = meta_data["session_id"]
            amount = float(meta_data["amount"])/100
            status = 'confirmed'

            fee = FeeMasterModel.objects.get(pk=fee_id)
            student = StudentsModel.objects.get(pk=student_id)
            session = SessionModel.objects.get(pk=session_id)
            if payment_setting.use_2fa_online:
                status = 'pending'
            payment = FeePaymentModel.objects.create(fee=fee, student=student, session=session, term=term,
                                                     payment_mode='online', online_payment_method=method, vat=vat,
                                                     amount=amount, reference=reference, type=type, status=status)
            payment.save()
            if payment.id:
                messages.success(request, 'N{} Payment Processed Successfully'.format(amount))
                context = {
                    'status': 'success',
                    'payment': payment,
                    'student': student,
                    'fee': fee,
                    'amount_in_word': num2words(amount)
                }
            else:
                context = {
                    'status': 'fail',
                    'reference': reference
                }
            return render(request, 'finance/online_payment/payment_done.html', context)

        else:
            if response.data.status == 'failed':
                messages.error(request, 'Payment Processing Failed, Try Later')
            elif response.data.status == 'pending':
                messages.warning(request, 'Payment Processing Pending, Please wait while we try to process the payment')
            else:
                messages.warning(request,
                                 'Payment Status not known. Please if you have been charged, wait a while for it to be resolved')
            return redirect(reverse('student_fee'))
    else:
        messages.warning(request, 'Invalid Transaction Link')
        return redirect(reverse('student_fee'))


def add_student_to_discount_benefactor(request, discount_pk, student_pk):
    if request.method == 'POST':
        pass
    discount = FeeDiscountModel.objects.get(pk=discount_pk)
    student = StudentsModel.objects.get(pk=student_pk)
    context = {
        'discount': discount,
        'student': student
    }
    return render(request, 'fee_discount/add_benefactor.html', context)


class FinanceSettingView(LoginRequiredMixin, TemplateView):
    template_name = 'finance/setting/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        form_kwargs = {}
        if school_setting.separate_school_section:
            finance_info = FinanceSettingModel.objects.filter(type=self.request.user.profile.type).first()
            form_kwargs['type'] = self.request.user.profile.type
        else:
            finance_info = FinanceSettingModel.objects.first()

        if not finance_info:
            form = FinanceSettingCreateForm(**form_kwargs)
            is_finance_info = False
        else:
            form = FinanceSettingEditForm(instance=finance_info, **form_kwargs)
            is_finance_info = True
        context['form'] = form
        context['is_finance_info'] = is_finance_info
        context['finance_info'] = finance_info
        return context


class FinanceSettingCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = FinanceSettingModel
    form_class = FinanceSettingCreateForm
    template_name = 'finance/setting/index.html'
    success_message = 'Finance Settings updated Successfully'

    def get_success_url(self):
        return reverse('finance_info')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()

        return context

    def get_form_kwargs(self):
        kwargs = super(FinanceSettingCreateView, self).get_form_kwargs()
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            kwargs.update({'type': self.request.user.profile.type})
        kwargs.update({'type': self.request.user.profile.type})
        return kwargs


class FinanceSettingUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = FinanceSettingModel
    form_class = FinanceSettingEditForm
    template_name = 'finance/setting/index.html'
    success_message = 'Finance Setting updated Successfully'

    def get_success_url(self):
        return reverse('finance_info')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

    def get_form_kwargs(self):
        kwargs = super(FinanceSettingUpdateView, self).get_form_kwargs()
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            kwargs.update({'type': self.request.user.profile.type})
        kwargs.update({'type': self.request.user.profile.type})
        return kwargs


class FeeDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'finance/dashboard/fee.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        session_id = self.request.GET.get('session')
        session = SessionModel.objects.get(pk=session_id)
        term = self.request.GET.get('term')
        context['current_session'] = SessionModel.objects.get(pk=session_id)
        context['session_list'] = SessionModel.objects.all()
        context['term'] = term
        context['session'] = session
        school_setting = SchoolGeneralInfoModel.objects.first()

        if school_setting.separate_school_section:
            fee_list = FeeModel.objects.filter(type=self.request.user.profile.type)
            academic_setting = SchoolAcademicInfoModel.objects.filter(type=self.request.user.profile.type).first()
        else:
            academic_setting = SchoolAcademicInfoModel.objects.first()
            fee_list = FeeModel.objects.filter()
        fee_payment_list = {}
        for fee in fee_list:
            fee_paid = FeePaymentModel.objects.filter(session=session, term=term, status='confirmed',
                                                      fee__fee=fee).aggregate(Sum('amount'))['amount__sum']
            if fee_paid is None:
                fee_paid = 0

            fee_payment_list[fee.name.upper()] = fee_paid
        if academic_setting.term == term and academic_setting.session == session:
            has_record = False
            current_term = True
            fee_record = None
        else:
            fee_record = FeeRecordModel.objects.filter(session=session, term=term).first()
            current_term = False
            if fee_record:
                has_record = True
            else:
                has_record = False
        current_day = 7
        start_date = datetime.now() + timedelta(days=1)
        date_list, transaction_list = [], []
        for num in range(1, 8):
            current_date = start_date - timedelta(days=current_day)
            date_list.append('{}-{}-{}T00:00:00.000Z'.format(current_date.year, current_date.month, current_date.day))
            all_transactions = FeePaymentModel.objects.filter(created_at__year=current_date.year,
                                                              created_at__month=current_date.month,
                                                              created_at__day=current_date.day,
                                                              status='confirmed')

            transaction = all_transactions.aggregate(Sum('amount'))['amount__sum']

            if not transaction:
                transaction = 0

            transaction_list.append(transaction)

            current_day -= 1

        total_expected_fee = 0
        if school_setting.separate_school_section:
            class_list = ClassSectionInfoModel.objects.filter(type=self.request.user.profile.type)
        else:
            class_list = ClassSectionInfoModel.objects.all()
        for a_class in class_list:
            student_class = a_class.student_class
            class_section = a_class.section
            number_of_student = StudentsModel.objects.filter(student_class=student_class, class_section=class_section).count()

            if school_setting.separate_school_section:
                fee_master_list = FeeMasterModel.objects.filter(type=self.request.user.profile.type,
                                                                student_class__in=[student_class.id],
                                                                class_section__in=[class_section.id])
            else:
                fee_master_list = FeeMasterModel.objects.filter(student_class__in=[student_class.id],
                                                                class_section__in=[class_section.id])
            for fee_master in fee_master_list:
                if fee_master.fee.fee_occurrence == 'termly':
                    if fee_master.same_termly_price:
                        amount = fee_master.amount
                    else:
                        if term == '1st term':
                            amount = fee_master.first_term_amount
                        elif term == '2nd term':
                            amount = fee_master.second_term_amount
                        elif term == '3rd term':
                            amount = fee_master.third_term_amount
                    total_expected_fee += amount * number_of_student
                else:
                    if fee_master.fee.payment_term == term or fee_master.fee.payment_term == 'any term':
                        total_expected_fee += fee_master.amount * number_of_student

        total_paid_fee = FeePaymentModel.objects.filter(term=term, session=session, status='confirmed').aggregate(
                Sum('amount'))['amount__sum']
        total_paid_fee = total_paid_fee if total_paid_fee else 0

        class_fee_payment_list = {}
        for class_info in class_list:
            fee_paid = FeePaymentModel.objects.filter(session=session, term=term, status='confirmed',
                                                      student__student_class=class_info.student_class,
                                                      ).aggregate(Sum('amount'))[
                'amount__sum']

            if fee_paid is None:
                fee_paid = 0
            class_name = "{} {}".format(class_info.student_class.name.upper(), class_info.section.name.upper())
            class_fee_payment_list[class_name] = fee_paid

        context['date_list'] = date_list
        context['transaction_list'] = transaction_list
        context['has_record'] = has_record
        context['fee_payment_list'] = fee_payment_list
        context['class_fee_payment_list'] = class_fee_payment_list
        context['current_term'] = current_term
        context['fee_record'] = fee_record
        context['fee_paid'] = total_paid_fee
        context['total_expected_fee'] = total_expected_fee
        context['fee_balance'] = total_expected_fee - total_paid_fee
        context['fee_record_list'] = FeeRecordModel.objects.filter(type=self.request.user.profile.type).order_by('id').reverse()[:15]

        return context


class FinanceDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'finance/dashboard/finance.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        session_id = self.request.GET.get('session')
        session = SessionModel.objects.get(pk=session_id)
        term = self.request.GET.get('term')
        context['current_session'] = SessionModel.objects.get(pk=session_id)
        context['session_list'] = SessionModel.objects.all()
        context['term'] = term
        context['session'] = session
        school_setting = SchoolGeneralInfoModel.objects.first()

        if school_setting.separate_school_section:
            academic_setting = SchoolAcademicInfoModel.objects.filter(type=self.request.user.profile.type).first()
            fee_paid = FeePaymentModel.objects.filter(session=session, term=term, status='confirmed',
                                                      type=self.request.user.profile.type).aggregate(Sum('amount'))[
                'amount__sum']
            total_income = IncomeModel.objects.filter(session=session, term=term,
                                                      type=self.request.user.profile.type).aggregate(Sum('amount'))[
                'amount__sum']
            total_expense = ExpenseModel.objects.filter(session=session, term=term,
                                                      type=self.request.user.profile.type).aggregate(Sum('amount'))[
                'amount__sum']
            income_category_list = IncomeCategoryModel.objects.filter(type=self.request.user.profile.type)
            expense_category_list = ExpenseCategoryModel.objects.filter(type=self.request.user.profile.type)
        else:
            academic_setting = SchoolAcademicInfoModel.objects.first()
            fee_paid = FeePaymentModel.objects.filter(session=session, term=term, status='confirmed').aggregate(Sum('amount'))[
                'amount__sum']
            total_income = IncomeModel.objects.filter(session=session, term=term,
                                                      ).aggregate(Sum('amount'))[
                'amount__sum']
            total_expense = ExpenseModel.objects.filter(session=session, term=term,
                                                        ).aggregate(Sum('amount'))[
                'amount__sum']
            income_category_list = IncomeCategoryModel.objects.all()
            expense_category_list = ExpenseCategoryModel.objects.all()
        fee_paid = fee_paid if fee_paid else 0
        total_income = total_income if total_income else 0
        total_expense = total_expense if total_expense else 0

        income_list = {}
        for category in income_category_list:
            income_paid = IncomeModel.objects.filter(session=session, term=term, category=category).aggregate(Sum('amount'))[
                'amount__sum']

            income_paid = income_paid if income_paid else 0
            income_list[category.name.upper()] = income_paid

        expense_list = {}
        for category in expense_category_list:
            expense_paid = ExpenseModel.objects.filter(session=session, term=term, category=category).aggregate(Sum('amount'))[
                'amount__sum']

            expense_paid = expense_paid if expense_paid else 0
            expense_list[category.name.upper()] = expense_paid

        context['current_session'] = session
        context['session_list'] = SessionModel.objects.all()
        context['term'] = term
        context['fee_paid'] = fee_paid
        context['other_income'] = total_income
        context['total_income'] = total_income + fee_paid
        context['total_expense'] = total_expense
        context['gross'] = fee_paid + total_income - total_expense
        context['income_list'] = income_list
        context['expense_list'] = expense_list

        return context


def print_finance_receipt(request, pk, receipt_type):
    if receipt_type == 'detailed_fee_payment':
        fee_payment = FeePaymentSummaryModel.objects.get(pk=pk)
        context = {
            'fee_payment': fee_payment,
            'amount_in_word': num2words(fee_payment.amount)
        }
        return render(request, 'finance/print/detailed_receipt.html', context)

    if receipt_type == 'summary_fee_payment':
        fee_payment = FeePaymentSummaryModel.objects.get(pk=pk)
        context = {
            'fee_payment': fee_payment,
            'amount_in_word': num2words(fee_payment.amount)
        }
        return render(request, 'finance/print/summary_receipt.html', context)

    messages.error(request, 'Invalid Receipt, Could not Print')
    return redirect(request.META.get('HTTP_REFERER', reverse('dashboard')))
