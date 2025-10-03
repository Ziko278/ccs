from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db.models import Sum
from datetime import date, datetime, timedelta
from num2words import num2words
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from django.contrib.messages.views import SuccessMessageMixin, messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from admin_dashboard.models import *
from django.contrib.auth.models import Group, Permission
from school_setting.forms import *
import math


class GroupCreateView(SuccessMessageMixin, CreateView):
    model = Group
    form_class = GroupForm
    template_name = 'school_setting/group/list.html'
    success_message = 'Group Added Successfully'

    def get_success_url(self):
        return reverse('group_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class GroupListView(ListView):
    model = Group
    fields = '__all__'
    template_name = 'school_setting/group/index.html'
    context_object_name = "group_list"

    def get_queryset(self):
        return Group.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = GroupForm
        return context


class GroupDetailView(DetailView):
    model = Group
    fields = '__all__'
    template_name = 'school_setting/group/detail.html'
    context_object_name = "group"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class GroupUpdateView(SuccessMessageMixin, UpdateView):
    model = Group
    form_class = GroupForm
    template_name = 'school_setting/group/index.html'
    success_message = 'Group Successfully Updated'

    def get_success_url(self):
        return reverse('group_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group'] = self.object
        context['group_list'] = Group.objects.all().order_by('name')
        return context


class GroupPermissionView(SuccessMessageMixin, UpdateView):
    model = Group
    form_class = GroupForm
    template_name = 'school_setting/group/permission.html'
    success_message = 'Group Permission Successfully Updated'

    def get_success_url(self):
        return reverse('group_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group'] = self.object
        context['permission_list'] = Permission.objects.all()
        return context


def group_permission_view(request, pk):
    group = Group.objects.get(pk=pk)
    if request.method == 'POST':
        permissions = request.POST.getlist('permissions[]')
        permission_list = []
        for permission_code in permissions:
            permission = Permission.objects.filter(codename=permission_code).first()
            if permission:
                permission_list.append(permission.id)
        group.permissions.set(permission_list)
        messages.success(request, 'Group Permission Successfully Updated')
        return redirect(reverse('group_index'))
    context = {
        'group': group,
        'permission_codenames': group.permissions.all().values_list('codename', flat=True),
        'permission_list': Permission.objects.all(),

    }
    return render(request, 'school_setting/group/permission.html', context)


class GroupDeleteView(DeleteView):
    model = Group
    fields = '__all__'
    template_name = 'school_setting/group/delete.html'
    context_object_name = "group"

    def get_success_url(self):
        return reverse('group_index')

    def dispatch(self, *args, **kwargs):
        if self.request.POST.get('name') in ['student', 'superadmin', 'teacher', 'parent']:
            messages.error(self.request, 'Restricted Group, Permission Denied')
            return redirect(reverse('group_index'))
        return super(GroupDeleteView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SchoolSettingView(LoginRequiredMixin, TemplateView):
    template_name = 'school_setting/setting/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_info = SchoolGeneralInfoModel.objects.filter(type=self.request.user.profile.type).first()
        if not school_info:
            school_info = SchoolGeneralInfoModel.objects.first()

        form_kwargs = {}
        if school_info.separate_school_section:
            school_info = SchoolGeneralInfoModel.objects.filter(type=self.request.user.profile.type).first()
            form_kwargs['type'] = self.request.user.profile.type
        else:
            school_info = SchoolGeneralInfoModel.objects.first()

        if not school_info:
            form = SchoolSettingCreateForm(**form_kwargs)
            is_school_info = False
        else:
            form = SchoolSettingEditForm(instance=school_info, **form_kwargs)
            is_school_info = True
        context['form'] = form
        context['is_school_info'] = is_school_info
        context['school_info'] = school_info
        return context


class SchoolSettingCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = SchoolGeneralInfoModel
    form_class = SchoolSettingCreateForm
    template_name = 'school_setting/setting/index.html'
    success_message = 'School Setting Info updated Successfully'

    def get_success_url(self):
        return reverse('school_info')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

    def get_form_kwargs(self):
        kwargs = super(SchoolSettingCreateView, self).get_form_kwargs()
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            kwargs.update({'type': self.request.user.profile.type})
        kwargs.update({'type': self.request.user.profile.type})
        return kwargs


class SchoolSettingUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = SchoolGeneralInfoModel
    form_class = SchoolSettingEditForm
    template_name = 'school_setting/setting/index.html'
    success_message = 'School Setting Info updated Successfully'

    def get_success_url(self):
        return reverse('school_info')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()

        return context

    def get_form_kwargs(self):
        kwargs = super(SchoolSettingUpdateView, self).get_form_kwargs()
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            kwargs.update({'type': self.request.user.profile.type})
        kwargs.update({'type': self.request.user.profile.type})
        return kwargs
