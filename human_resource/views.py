from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
import json
from django.contrib import messages
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
import io
from django.forms.models import model_to_dict
from xlsxwriter.workbook import Workbook
from human_resource.models import *
from human_resource.forms import *
from school_setting.models import *
from django.db.models import Sum
from admin_dashboard.utility import state_list


class DepartmentCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = DepartmentModel
    permission_required = 'human_resource.add_departmentmodel'
    form_class = DepartmentForm
    template_name = 'human_resource/department/index.html'
    success_message = 'Department Successfully Registered'

    def get_success_url(self):
        return reverse('department_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            context['department_list'] = DepartmentModel.objects.filter(type=self.request.user.profile.type).order_by(
                'name')
        else:
            context['department_list'] = DepartmentModel.objects.all().order_by('name')
        return context


class DepartmentListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = DepartmentModel
    permission_required = 'human_resource.view_departmentmodel'
    fields = '__all__'
    template_name = 'human_resource/department/index.html'
    context_object_name = "department_list"

    def get_queryset(self):
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            return DepartmentModel.objects.filter(type=self.request.user.profile.type).order_by('name')
        else:
            return DepartmentModel.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = DepartmentForm
        return context


class DepartmentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = DepartmentModel
    permission_required = 'human_resource.change_departmentmodel'
    form_class = DepartmentEditForm
    template_name = 'human_resource/department/index.html'
    success_message = 'Department Successfully Updated'

    def get_success_url(self):
        return reverse('department_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DepartmentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = DepartmentModel
    permission_required = 'human_resource.delete_departmentmodel'
    fields = '__all__'
    template_name = 'human_resource/department/delete.html'
    context_object_name = "department"
    success_message = 'Department Successfully Deleted'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('department_index')


class PositionCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = PositionModel
    permission_required = 'human_resource.add_positionmodel'
    form_class = PositionForm
    template_name = 'human_resource/position/index.html'
    success_message = 'Position Successfully Registered'

    def get_success_url(self):
        return reverse('position_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            context['department_list'] = DepartmentModel.objects.filter(type=self.request.user.profile.type).order_by(
                'name')
            context['position_list'] = PositionModel.objects.filter(type=self.request.user.profile.type).order_by('name')
        else:
            context['department_list'] = DepartmentModel.objects.all().order_by('name')
            context['position_list'] = PositionModel.objects.all().order_by('name')
        return context


class PositionListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = PositionModel
    permission_required = 'human_resource.view_positionmodel'
    fields = '__all__'
    template_name = 'human_resource/position/index.html'
    context_object_name = "position_list"

    def get_queryset(self):
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            return PositionModel.objects.filter(type=self.request.user.profile.type).order_by('name')
        else:
            return PositionModel.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        school_setting = SchoolGeneralInfoModel.objects.first()
        form_kwargs = {}
        if school_setting.separate_school_section:
            context['department_list'] = DepartmentModel.objects.filter(type=self.request.user.profile.type).order_by(
                'name')
            form_kwargs['type'] = self.request.user.profile.type
        else:
            context['department_list'] = DepartmentModel.objects.all().order_by('name')
        context['form'] = PositionForm(**form_kwargs)

        return context


class PositionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = PositionModel
    permission_required = 'human_resource.change_positionmodel'
    form_class = PositionEditForm
    template_name = 'human_resource/position/index.html'
    success_message = 'Position Successfully Updated'

    def get_success_url(self):
        return reverse('position_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PositionDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = PositionModel
    permission_required = 'human_resource.delete_positionmodel'
    fields = '__all__'
    template_name = 'human_resource/position/delete.html'
    context_object_name = "position"
    success_message = 'Position Successfully Deleted'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('position_index')


class StaffCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = StaffModel
    permission_required = 'human_resource.add_staffmodel'
    form_class = StaffForm
    template_name = 'human_resource/staff/create.html'
    success_message = 'Staff Successfully Registered'

    def get_success_url(self):
        return reverse('staff_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            context['department_list'] = DepartmentModel.objects.filter(type=self.request.user.profile.type).order_by('name')
            context['staff_setting'] = HRSettingModel.objects.filter(type=self.request.user.profile.type).first()
        else:
            context['department_list'] = DepartmentModel.objects.all().order_by('name')
            context['staff_setting'] = HRSettingModel.objects.filter().first()
        context['state_list'] = state_list
        return context

    def get_form_kwargs(self):
        kwargs = super(StaffCreateView, self).get_form_kwargs()
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            kwargs.update({'type': self.request.user.profile.type})
        kwargs.update({'type': self.request.user.profile.type})
        return kwargs


class StaffListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = StaffModel
    permission_required = 'human_resource.view_staffmodel'
    fields = '__all__'
    template_name = 'human_resource/staff/index.html'
    context_object_name = "staff_list"

    def get_queryset(self):
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            return StaffModel.objects.filter(type=self.request.user.profile.type, status='active').order_by('surname')
        else:
            return StaffModel.objects.filter(status='active').order_by('surname')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class StaffDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = StaffModel
    permission_required = 'human_resource.view_staffmodel'
    fields = '__all__'
    template_name = 'human_resource/staff/detail.html'
    context_object_name = "staff"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class StaffUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = StaffModel
    permission_required = 'human_resource.change_staffmodel'
    form_class = StaffEditForm
    template_name = 'human_resource/staff/edit.html'
    success_message = 'Staff Information Successfully Updated'

    def get_success_url(self):
        return reverse('staff_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            context['department_list'] = DepartmentModel.objects.filter(type=self.request.user.profile.type).order_by(
                'name')
            context['staff_setting'] = HRSettingModel.objects.filter(type=self.request.user.profile.type).first()
        else:
            context['department_list'] = DepartmentModel.objects.all().order_by('name')
            context['staff_setting'] = HRSettingModel.objects.filter().first()
        context['state_list'] = state_list
        context['staff'] = self.object
        return context

    def get_form_kwargs(self):
        kwargs = super(StaffUpdateView, self).get_form_kwargs()
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            kwargs.update({'type': self.request.user.profile.type})
        kwargs.update({'type': self.request.user.profile.type})
        return kwargs


class StaffDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = StaffModel
    permission_required = 'human_resource.delete_staffmodel'
    fields = '__all__'
    template_name = 'human_resource/staff/delete.html'
    context_object_name = "staff"
    success_message = 'Staff Successfully Deleted'

    def get_success_url(self):
        return reverse('staff_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


def generate_form_view(request):
    if request.method == 'POST':
        staff_list = request.POST.getlist('staff_list[]')
        field_list = request.POST.getlist('form_field[]')
        file_name = request.POST['file_name']
        if not staff_list:
            messages.warning(request, 'No staff Selected')
            return redirect(reverse('staff_form'))
        if not field_list:
            messages.warning(request, 'No Field Selected')
            return redirect(reverse('staff_form'))

        output = io.BytesIO()

        workbook = Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()

        for num in range(len(field_list)):
            field = field_list[num]
            worksheet.write(0, num, field.title())

        for row in range(len(staff_list)):
            staff_pk = staff_list[row]
            staff = StaffModel.objects.get(pk=staff_pk)

            for col in range(len(field_list)):
                field = field_list[col]
                if field == 'full_name':
                    if getattr(staff, "middle_name"):
                        value = getattr(staff, "surname") + ' ' + getattr(staff, "middle_name") + ' ' + getattr(staff, "last_name")
                    else:
                        value = getattr(staff, "surname") + ' ' + getattr(staff, "last_name")
                elif field == 'department':
                    value = staff.department.name.title()
                elif field == 'position':
                    value = staff.position.name.title()
                else:
                    value = getattr(staff, field)
                if isinstance(value, str):
                    value = value.title()
                worksheet.write(row + 1, col, value)
        workbook.close()

        output.seek(0)

        response = HttpResponse(output.read(),
                                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = "attachment; filename="+file_name+".xlsx"

        output.close()

        return response
    school_setting = SchoolGeneralInfoModel.objects.first()
    if school_setting.separate_school_section:
        staff_list = StaffModel.objects.filter(type=request.user.profile.type, status='active').order_by('surname')
    else:
        staff_list = StaffModel.objects.filter(status='active').order_by('surname')

    context = {
        'staff_list': staff_list
    }
    return render(request, 'human_resource/staff/generate_form.html', context)


class HRSettingView(LoginRequiredMixin, TemplateView):
    template_name = 'human_resource/setting/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        form_kwargs = {}
        if school_setting.separate_school_section:
            hr_info = HRSettingModel.objects.filter(type=self.request.user.profile.type).first()
            form_kwargs['type'] = self.request.user.profile.type
        else:
            hr_info = HRSettingModel.objects.first()

        if not hr_info:
            form = HRSettingCreateForm(**form_kwargs)
            is_hr_info = False
        else:
            form = HRSettingEditForm(instance=hr_info, **form_kwargs)
            is_hr_info = True
        context['form'] = form
        context['is_hr_info'] = is_hr_info
        context['hr_info'] = hr_info
        return context


class HRSettingCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = HRSettingModel
    form_class = HRSettingCreateForm
    template_name = 'human_resource/setting/index.html'
    success_message = 'Human Resource Settings updated Successfully'

    def get_success_url(self):
        return reverse('hr_info')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()

        return context

    def get_form_kwargs(self):
        kwargs = super(HRSettingCreateView, self).get_form_kwargs()
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            kwargs.update({'type': self.request.user.profile.type})
        kwargs.update({'type': self.request.user.profile.type})
        return kwargs


class HRSettingUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = HRSettingModel
    form_class = HRSettingEditForm
    template_name = 'human_resource/setting/index.html'
    success_message = 'Human Resource Setting updated Successfully'

    def get_success_url(self):
        return reverse('hr_info')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

    def get_form_kwargs(self):
        kwargs = super(HRSettingUpdateView, self).get_form_kwargs()
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            kwargs.update({'type': self.request.user.profile.type})
        kwargs.update({'type': self.request.user.profile.type})
        return kwargs

