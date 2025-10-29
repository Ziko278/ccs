from django.shortcuts import render, redirect
from django.urls import reverse
from django.template.loader import render_to_string
from django.conf import settings
from django.http import HttpResponse

import random
from django.contrib.messages.views import SuccessMessageMixin, messages
from django.views.generic import TemplateView
from datetime import datetime
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from result.models import *
from django.db.models import Q
from result.forms import *
from school_setting.models import SchoolAcademicInfoModel, TermModel, SchoolGeneralInfoModel, SessionModel

class ResultFieldCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = ResultFieldModel
    permission_required = 'result.add_resultfieldmodel'
    form_class = ResultFieldForm
    success_message = 'Result Field Added Successfully'
    template_name = 'result/result_field/index.html'

    def get_success_url(self):
        return reverse('result_field_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            context['class_list'] = ClassesModel.objects.filter(Q(result_type='score') | Q(result_type='mix'),
                                                                type=self.request.user.profile.type).order_by('name')

            context['class_section_list'] = ClassSectionModel.objects.filter(
                type=self.request.user.profile.type).order_by('name')
            context['result_field_list'] = ResultFieldModel.objects.filter(
                type=self.request.user.profile.type).order_by('name')
        else:
            context['class_list'] = ClassesModel.objects.filter(Q(result_type='score') | Q(result_type='mix')).order_by(
                'name')

            context['class_section_list'] = ClassSectionModel.objects.all().order_by('name')
            context['result_field_list'] = ResultFieldModel.objects.all().order_by('name')
        return context

    def get_form_kwargs(self):
        kwargs = super(ResultFieldCreateView, self).get_form_kwargs()
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            kwargs.update({'type': self.request.user.profile.type})
        kwargs.update({'type': self.request.user.profile.type})
        return kwargs


class ResultFieldListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = ResultFieldModel
    permission_required = 'result.view_resultfieldmodel'
    fields = '__all__'
    template_name = 'result/result_field/index.html'
    context_object_name = "result_field_list"

    def get_queryset(self):
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            return ResultFieldModel.objects.filter(type=self.request.user.profile.type).order_by('order')
        else:
            return ResultFieldModel.objects.all().order_by('order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        form_kwargs = {}
        if school_setting.separate_school_section:
            context['class_section_list'] = ClassSectionModel.objects.filter(
                type=self.request.user.profile.type).order_by('name')
            context['class_list'] = ClassesModel.objects.filter(Q(result_type='score') | Q(result_type='mix'),
                                                                type=self.request.user.profile.type).order_by('name')

            form_kwargs['type'] = self.request.user.profile.type
        else:
            context['class_list'] = ClassesModel.objects.filter(Q(result_type='score') | Q(result_type='mix')).order_by(
                'name')
            context['class_section_list'] = ClassSectionModel.objects.all().order_by('name')
        context['form'] = ResultFieldForm(**form_kwargs)

        return context


class ResultFieldUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = ResultFieldModel
    permission_required = 'result.change_resultfieldmodel'
    form_class = ResultFieldEditForm
    success_message = 'Result Field Updated Successfully'
    template_name = 'result/result_field/index.html'

    def get_success_url(self):
        return reverse('result_field_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        form_kwargs = {}
        if school_setting.separate_school_section:
            context['class_section_list'] = ClassSectionModel.objects.filter(
                type=self.request.user.profile.type).order_by('name')
            context['class_list'] = ClassesModel.objects.filter(Q(result_type='score') | Q(result_type='mix'),
                                                                type=self.request.user.profile.type).order_by('name')

            context['result_field_list'] = ResultFieldModel.objects.filter(
                type=self.request.user.profile.type).order_by('name')
            form_kwargs['type'] = self.request.user.profile.type
        else:
            context['class_section_list'] = ClassSectionModel.objects.all().order_by('name')
            context['class_list'] = ClassesModel.objects.filter(Q(result_type='score') | Q(result_type='mix')).order_by(
                'name')

            context['result_field_list'] = ResultFieldModel.objects.all().order_by('name')
        context['form'] = ResultFieldForm(**form_kwargs)
        return context


class ResultFieldDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = ResultFieldModel
    permission_required = 'result.delete_resultfieldmodel'
    success_message = 'Result Field Deleted Successfully'
    fields = '__all__'
    template_name = 'result/result_field/delete.html'
    context_object_name = "result_field"

    def get_success_url(self):
        return reverse("result_field_index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ResultGradeCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = ResultGradeModel
    permission_required = 'result.add_resultgrademodel'
    form_class = ResultGradeForm
    success_message = 'Result Grade Added Successfully'
    template_name = 'result/result_grade/index.html'

    def get_success_url(self):
        return reverse('result_grade_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            context['class_list'] = ClassesModel.objects.filter(Q(result_type='score') | Q(result_type='mix'),
                                                                type=self.request.user.profile.type).order_by('name')
            context['class_section_list'] = ClassSectionModel.objects.filter(
                type=self.request.user.profile.type).order_by('name')
            context['result_grade_list'] = ResultGradeModel.objects.filter(
                type=self.request.user.profile.type).order_by('name')
        else:
            context['class_list'] = ClassesModel.objects.filter(
                Q(result_type='score') | Q(result_type='mix'), ).order_by('name')
            context['class_section_list'] = ClassSectionModel.objects.all().order_by('name')
            context['result_grade_list'] = ResultGradeModel.objects.all().order_by('name')
        return context

    def get_form_kwargs(self):
        kwargs = super(ResultGradeCreateView, self).get_form_kwargs()
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            kwargs.update({'type': self.request.user.profile.type})
        kwargs.update({'type': self.request.user.profile.type})
        return kwargs


class ResultGradeListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = ResultGradeModel
    permission_required = 'result.view_resultgrademodel'
    fields = '__all__'
    template_name = 'result/result_grade/index.html'
    context_object_name = "result_grade_list"

    def get_queryset(self):
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            return ResultGradeModel.objects.filter(type=self.request.user.profile.type).order_by('name')
        else:
            return ResultGradeModel.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        form_kwargs = {}
        if school_setting.separate_school_section:
            context['class_section_list'] = ClassSectionModel.objects.filter(
                type=self.request.user.profile.type).order_by('name')
            context['class_list'] = ClassesModel.objects.filter(Q(result_type='score') | Q(result_type='mix'),
                                                                type=self.request.user.profile.type).order_by('name')
            context['result_grade_list'] = ResultGradeModel.objects.filter(
                type=self.request.user.profile.type).order_by('name')
            form_kwargs['type'] = self.request.user.profile.type
        else:
            context['class_section_list'] = ClassSectionModel.objects.all().order_by('name')
            context['class_list'] = ClassesModel.objects.filter(
                Q(result_type='score') | Q(result_type='mix'), ).order_by('name')
            context['result_grade_list'] = ResultGradeModel.objects.all().order_by('name')
        context['form'] = ResultGradeForm(**form_kwargs)

        return context


class ResultGradeUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = ResultGradeModel
    permission_required = 'result.change_resultgrademodel'
    form_class = ResultGradeEditForm
    success_message = 'Result Grade Updated Successfully'
    template_name = 'result/result_grade/index.html'

    def get_success_url(self):
        return reverse('result_grade_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        form_kwargs = {}
        if school_setting.separate_school_section:
            context['class_section_list'] = ClassSectionModel.objects.filter(
                type=self.request.user.profile.type).order_by('name')
            context['class_list'] = ClassesModel.objects.filter(Q(result_type='score') | Q(result_type='mix'),
                                                                type=self.request.user.profile.type).order_by('name')
            context['result_grade_list'] = ResultGradeModel.objects.filter(
                type=self.request.user.profile.type).order_by('name')
            form_kwargs['type'] = self.request.user.profile.type
        else:
            context['class_section_list'] = ClassSectionModel.objects.all().order_by('name')
            context['class_list'] = ClassesModel.objects.filter(
                Q(result_type='score') | Q(result_type='mix'), ).order_by('name')
            context['result_grade_list'] = ResultGradeModel.objects.all().order_by('name')
        context['form'] = ResultGradeForm(**form_kwargs)
        return context


class ResultGradeDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = ResultGradeModel
    permission_required = 'result.delete_resultgrademodel'
    success_message = 'Result Grade Deleted Successfully'
    fields = '__all__'
    template_name = 'result/result_grade/delete.html'
    context_object_name = "result_grade"

    def get_success_url(self):
        return reverse("result_grade_index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class MidResultGradeCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = MidResultGradeModel
    permission_required = 'result.add_midresultgrademodel'
    form_class = MidResultGradeForm
    success_message = 'Mid Term Result Grade Added Successfully'
    template_name = 'result/mid_result_grade/index.html'

    def get_success_url(self):
        return reverse('mid_result_grade_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            context['class_list'] = ClassesModel.objects.filter(type=self.request.user.profile.type,
                                                                result_type='score').order_by('name')
            context['class_section_list'] = ClassSectionModel.objects.filter(
                type=self.request.user.profile.type).order_by('name')
            context['result_grade_list'] = MidResultGradeModel.objects.filter(
                type=self.request.user.profile.type).order_by('name')
        else:
            context['class_list'] = ClassesModel.objects.filter(result_type='score').order_by('name')
            context['class_section_list'] = ClassSectionModel.objects.all().order_by('name')
            context['result_grade_list'] = MidResultGradeModel.objects.all().order_by('name')
        return context

    def get_form_kwargs(self):
        kwargs = super(MidResultGradeCreateView, self).get_form_kwargs()
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            kwargs.update({'type': self.request.user.profile.type})
        kwargs.update({'type': self.request.user.profile.type})
        return kwargs


class MidResultGradeListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = MidResultGradeModel
    permission_required = 'result.view_midresultgrademodel'
    fields = '__all__'
    template_name = 'result/mid_result_grade/index.html'
    context_object_name = "result_grade_list"

    def get_queryset(self):
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            return MidResultGradeModel.objects.filter(type=self.request.user.profile.type).order_by('name')
        else:
            return MidResultGradeModel.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        form_kwargs = {}
        if school_setting.separate_school_section:
            context['class_section_list'] = ClassSectionModel.objects.filter(
                type=self.request.user.profile.type).order_by('name')
            context['class_list'] = ClassesModel.objects.filter(type=self.request.user.profile.type,
                                                                result_type='score').order_by('name')
            context['result_grade_list'] = MidResultGradeModel.objects.filter(
                type=self.request.user.profile.type).order_by('name')
            form_kwargs['type'] = self.request.user.profile.type
        else:
            context['class_section_list'] = ClassSectionModel.objects.all().order_by('name')
            context['class_list'] = ClassesModel.objects.filter(result_type='score').order_by('name')
            context['result_grade_list'] = MidResultGradeModel.objects.all().order_by('name')
        context['form'] = MidResultGradeForm(**form_kwargs)

        return context


class MidResultGradeUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = MidResultGradeModel
    permission_required = 'result.change_midresultgrademodel'
    form_class = MidResultGradeEditForm
    success_message = 'Mid Term Result Grade Updated Successfully'
    template_name = 'result/mid_result_grade/index.html'

    def get_success_url(self):
        return reverse('mid_result_grade_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        form_kwargs = {}
        if school_setting.separate_school_section:
            context['class_section_list'] = ClassSectionModel.objects.filter(
                type=self.request.user.profile.type).order_by('name')
            context['class_list'] = ClassesModel.objects.filter(type=self.request.user.profile.type,
                                                                result_type='score').order_by('name')
            context['result_grade_list'] = MidResultGradeModel.objects.filter(
                type=self.request.user.profile.type).order_by('name')
            form_kwargs['type'] = self.request.user.profile.type
        else:
            context['class_section_list'] = ClassSectionModel.objects.all().order_by('name')
            context['class_list'] = ClassesModel.objects.filter(result_type='score').order_by('name')
            context['result_grade_list'] = MidResultGradeModel.objects.all().order_by('name')
        context['form'] = MidResultGradeForm(**form_kwargs)
        return context


class MidResultGradeDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = MidResultGradeModel
    permission_required = 'result.delete_midresultgrademodel'
    success_message = 'Mid Term Result Grade Deleted Successfully'
    fields = '__all__'
    template_name = 'result/mid_result_grade/delete.html'
    context_object_name = "result_grade"

    def get_success_url(self):
        return reverse("mid_result_grade_index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ResultBehaviourCategoryCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = ResultBehaviourCategoryModel
    permission_required = 'result.add_resultaffectivedomainmodel'
    form_class = ResultBehaviourCategoryForm
    success_message = 'Student Behaviour Category Field Added Successfully'
    template_name = 'result/behaviour_category/index.html'

    def get_success_url(self):
        return reverse('result_behaviour_category_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            context['category_list'] = ResultBehaviourCategoryModel.objects.filter(
                type=self.request.user.profile.type).order_by('name')
        else:
            context['category_list'] = ResultBehaviourCategoryModel.objects.all().order_by('name')
        return context


class ResultBehaviourCategoryListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = ResultBehaviourCategoryModel
    permission_required = 'result.view_resultaffectivedomainmodel'
    fields = '__all__'
    template_name = 'result/behaviour_category/index.html'
    context_object_name = "category_list"

    def get_queryset(self):
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            return ResultBehaviourCategoryModel.objects.filter(type=self.request.user.profile.type).order_by('name')
        else:
            return ResultBehaviourCategoryModel.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ResultBehaviourCategoryForm
        return context


class ResultBehaviourCategoryUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = ResultBehaviourCategoryModel
    permission_required = 'result.change_resultaffectivedomainmodel'
    form_class = ResultBehaviourCategoryEditForm
    success_message = 'Student Behaviour Category Updated Successfully'
    template_name = 'result/behaviour_category/index.html'

    def get_success_url(self):
        return reverse('result_behaviour_category_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            context['category_list'] = ResultBehaviourCategoryModel.objects.filter(
                type=self.request.user.profile.type).order_by('name')
        else:
            context['category_list'] = ResultBehaviourCategoryModel.objects.all().order_by('name')
        return context


class ResultBehaviourCategoryDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = ResultBehaviourCategoryModel
    permission_required = 'result.delete_resultaffectivedomainmodel'
    success_message = 'Student Behaviour Category Deleted Successfully'
    fields = '__all__'
    template_name = 'result/behaviour_category/delete.html'
    context_object_name = "category"

    def get_success_url(self):
        return reverse("result_behaviour_category_index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ResultBehaviourCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = ResultBehaviourModel
    permission_required = 'result.add_resultaffectivedomainmodel'
    form_class = ResultBehaviourForm
    success_message = 'Student Behaviour Field Added Successfully'
    template_name = 'result/behaviour/index.html'

    def get_success_url(self):
        return reverse('result_behaviour_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            context['class_list'] = ClassesModel.objects.filter(type=self.request.user.profile.type).order_by('name')
            context['class_section_list'] = ClassSectionModel.objects.filter(
                type=self.request.user.profile.type).order_by('name')
            context['result_behaviour_list'] = ResultBehaviourModel.objects.filter(
                type=self.request.user.profile.type).order_by('name')
            context['category_list'] = ResultBehaviourCategoryModel.objects.filter(
                type=self.request.user.profile.type).order_by('name')
        else:
            context['class_list'] = ClassesModel.objects.all().order_by('name')
            context['class_section_list'] = ClassSectionModel.objects.all().order_by('name')
            context['result_behaviour_list'] = ResultBehaviourModel.objects.all().order_by('name')
            context['category_list'] = ResultBehaviourCategoryModel.objects.all().order_by('name')

    def get_form_kwargs(self):
        kwargs = super(ResultBehaviourCreateView, self).get_form_kwargs()
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            kwargs.update({'type': self.request.user.profile.type})
        kwargs.update({'type': self.request.user.profile.type})
        return kwargs


class ResultBehaviourListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = ResultBehaviourModel
    permission_required = 'result.view_resultaffectivedomainmodel'
    fields = '__all__'
    template_name = 'result/behaviour/index.html'
    context_object_name = "result_behaviour_list"

    def get_queryset(self):
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            return ResultBehaviourModel.objects.filter(type=self.request.user.profile.type).order_by('order')
        else:
            return ResultBehaviourModel.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        form_kwargs = {}
        if school_setting.separate_school_section:
            context['class_section_list'] = ClassSectionModel.objects.filter(
                type=self.request.user.profile.type).order_by('name')
            context['class_list'] = ClassesModel.objects.filter(type=self.request.user.profile.type).order_by('name')
            context['category_list'] = ResultBehaviourCategoryModel.objects.filter(
                type=self.request.user.profile.type).order_by('name')
            form_kwargs['type'] = self.request.user.profile.type
        else:
            context['class_section_list'] = ClassSectionModel.objects.all().order_by('name')
            context['class_list'] = ClassesModel.objects.all().order_by('name')
            context['category_list'] = ResultBehaviourCategoryModel.objects.all().order_by('name')
        context['form'] = ResultBehaviourForm(**form_kwargs)
        return context


class ResultBehaviourUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = ResultBehaviourModel
    permission_required = 'result.change_resultaffectivedomainmodel'
    form_class = ResultBehaviourEditForm
    success_message = 'Student Behaviour Updated Successfully'
    template_name = 'result/behaviour/index.html'

    def get_success_url(self):
        return reverse('result_behaviour_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            context['class_list'] = ClassesModel.objects.filter(type=self.request.user.profile.type).order_by('name')
            context['class_section_list'] = ClassSectionModel.objects.filter(
                type=self.request.user.profile.type).order_by('name')
            context['result_behaviour_list'] = ResultBehaviourModel.objects.filter(
                type=self.request.user.profile.type).order_by('name')
            context['category_list'] = ResultBehaviourCategoryModel.objects.filter(
                type=self.request.user.profile.type).order_by('name')
        else:
            context['class_list'] = ClassesModel.objects.all().order_by('name')
            context['class_section_list'] = ClassSectionModel.objects.all().order_by('name')
            context['result_behaviour_list'] = ResultBehaviourModel.objects.all().order_by('name')
            context['category_list'] = ResultBehaviourCategoryModel.objects.all().order_by('name')

    def get_form_kwargs(self):
        kwargs = super(ResultBehaviourUpdateView, self).get_form_kwargs()
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            kwargs.update({'type': self.request.user.profile.type})
        kwargs.update({'type': self.request.user.profile.type})
        return kwargs


class ResultBehaviourDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = ResultBehaviourModel
    permission_required = 'result.delete_resultaffectivedomainmodel'
    success_message = 'Student Behaviour Deleted Successfully'
    fields = '__all__'
    template_name = 'result/behaviour/delete.html'
    context_object_name = "result_behaviour"

    def get_success_url(self):
        return reverse("result_behaviour_index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@login_required
def result_create_view(request):
    school_setting = SchoolGeneralInfoModel.objects.first()
    if request.method == 'POST':
        # --- POST logic remains the same, as it correctly checks permissions upon submission ---
        student_class_pk = request.POST['student_class']
        class_section_pk = request.POST['class_section']
        subject_pk = request.POST['subject']

        if school_setting.separate_school_section:
            result_setting = ResultSettingModel.objects.filter(type=request.user.profile.type).first()
        else:
            result_setting = ResultSettingModel.objects.first()

        is_allowed = False
        message = 'Access Denied: You do not have the required permissions for the selected class/subject.'
        # Allow superusers to bypass checks
        if request.user.is_superuser:
            is_allowed = True
        elif result_setting and result_setting.allowed_user != 'any':
            current_user = request.user.profile.staff
            if current_user:
                is_form_teacher = ClassSectionInfoModel.objects.filter(
                    student_class_id=student_class_pk, section_id=class_section_pk
                ).filter(
                    Q(form_teacher=current_user) | Q(assistant_form_teacher=current_user)
                ).exists()

                is_subject_teacher = ClassSectionSubjectTeacherModel.objects.filter(
                    subject_id=subject_pk, student_class__id=student_class_pk, class_section__id=class_section_pk,
                    teachers=current_user
                ).exists()

                if result_setting.allowed_user == 'form teacher' and is_form_teacher:
                    is_allowed = True
                elif result_setting.allowed_user == 'subject teacher' and is_subject_teacher:
                    is_allowed = True
                elif result_setting.allowed_user == 'both' and (is_form_teacher or is_subject_teacher):
                    is_allowed = True
        else:
            # This handles the 'any user' case or when no settings are found
            is_allowed = True

        if not is_allowed:
            messages.error(request, message)
            return redirect(reverse('result_create'))

        request.session['student_class'] = student_class_pk
        request.session['class_section'] = class_section_pk
        request.session['subject'] = subject_pk
        if 'update' in request.POST:
            request.session['is_update'] = True
            request.session['session_pk'] = request.POST['session_pk']
            request.session['term_pk'] = request.POST['term_pk']
        return redirect(reverse('result_upload'))

    # =======================================================================
    # START: UPDATED GET REQUEST LOGIC
    # =======================================================================

    user_type = request.user.profile.type
    q_filter = Q(type=user_type) if school_setting.separate_school_section else Q()

    # 1. Define the initial, unfiltered querysets
    class_list = ClassesModel.objects.filter(q_filter, Q(result_type='score') | Q(result_type='mix')).order_by('name')
    text_class_list = ClassesModel.objects.filter(q_filter, Q(result_type='text') | Q(result_type='mix')).order_by('name')
    subject_list = SubjectsModel.objects.filter(q_filter).order_by('name')

    # 2. Get the relevant result setting and staff profile
    if school_setting.separate_school_section:
        result_setting = ResultSettingModel.objects.filter(type=user_type).first()
    else:
        result_setting = ResultSettingModel.objects.first()

    staff = request.user.profile.staff if hasattr(request.user, 'profile') else None

    # 3. Apply permission filters if the user is not a superuser
    if not request.user.is_superuser and result_setting and staff:
        if result_setting.allowed_user == 'form teacher':
            form_teacher_filter = Q(classsectioninfomodel__form_teacher=staff) | Q(classsectioninfomodel__assistant_form_teacher=staff)
            class_list = class_list.filter(form_teacher_filter).distinct()
            text_class_list = text_class_list.filter(form_teacher_filter).distinct()

        elif result_setting.allowed_user == 'subject teacher':
            subject_teacher_class_filter = Q(classsectionsubjectteachermodel__teachers=staff)
            class_list = class_list.filter(subject_teacher_class_filter).distinct()
            text_class_list = text_class_list.filter(subject_teacher_class_filter).distinct()
            subject_list = subject_list.filter(subject_class_section_info__teachers=staff).distinct()

        elif result_setting.allowed_user == 'both':
            combined_filter = Q(classsectioninfomodel__form_teacher=staff) | \
                              Q(classsectioninfomodel__assistant_form_teacher=staff) | \
                              Q(classsectionsubjectteachermodel__teachers=staff)
            class_list = class_list.filter(combined_filter).distinct()
            text_class_list = text_class_list.filter(combined_filter).distinct()
            subject_list = subject_list.filter(subject_class_section_info__teachers=staff).distinct()

        # If allowed_user is 'any', no filtering is done and the initial querysets are used.

    # If settings are restrictive and the user is not a superuser, they might see empty lists.
    # This is the expected behavior.

    # =======================================================================
    # END: UPDATED GET REQUEST LOGIC
    # =======================================================================

    context = {
        'class_list': class_list,
        'text_class_list': text_class_list,
        'subject_list': subject_list,
        'session_list': SessionModel.objects.filter(q_filter),
        'term_list': TermModel.objects.all().order_by('order')
    }

    if 'update' in request.GET:
        return render(request, 'result/result/update.html', context=context)
    return render(request, 'result/result/create.html', context=context)


def result_upload_view(request):
    if request.method == 'POST':
        student_list = request.POST.getlist('students[]')
        session = SessionModel.objects.get(pk=request.POST['session'])
        term = TermModel.objects.get(pk=request.POST['term'])
        subject = SubjectsModel.objects.get(pk=request.POST['subject'])
        student_class = ClassesModel.objects.get(pk=request.POST['student_class'])
        class_section = ClassSectionModel.objects.get(pk=request.POST['class_section'])
        result_field_list = ResultFieldModel.objects.filter(student_class=student_class,
                                                            class_section=class_section).order_by('order')

        has_exam = False
        has_ca = False
        midterm_scores, total_scores = [], []
        out_of = 0
        position_dict = {}
        midterm_dict = {}

        midterm_max = sum(field.max_mark for field in result_field_list if field.mid_term)

        for num in range(len(student_list)):
            student = StudentsModel.objects.get(pk=student_list[num])
            total_score, test_score, midterm_total = 0, 0, 0
            student_result = {}

            for field in result_field_list:
                field_name_post = f'{field.name}[]'
                if field_name_post in request.POST and num < len(request.POST.getlist(field_name_post)):
                    field_result = request.POST.getlist(field_name_post)[num]
                    student_result[field.name.upper()] = field_result
                    if field_result:
                        score = float(field_result)
                        total_score += score
                        if field.field_type == 'ca':
                            test_score += score
                            has_ca = True
                        if field.mid_term:
                            midterm_total += score
                        if field.field_type == 'exam':
                            has_exam = True
                else:
                    student_result[field.name.upper()] = ''

            student_result['TOTAL CA'] = test_score or ''

            if total_score > 0:
                out_of += 1
                total_scores.append(total_score)
                position_dict.setdefault(total_score, []).append(student)

            if midterm_total > 0:
                midterm_scores.append(midterm_total)
                midterm_dict.setdefault(midterm_total, []).append(student)

            grade_list = ResultGradeModel.objects.filter(student_class=student_class, class_section=class_section)
            mid_grade_list = MidResultGradeModel.objects.filter(student_class=student_class,
                                                                class_section=class_section)

            grade, remark = next(
                ((g.name.upper(), g.remark.upper()) for g in grade_list if g.min_mark <= total_score <= g.max_mark),
                ('', ''))
            midterm_grade, midterm_remark = next(((g.name.upper(), g.remark.upper()) for g in mid_grade_list if
                                                  g.min_mark <= midterm_total <= g.max_mark), ('', ''))

            student_result.update({
                'subject': subject.name, 'subject_code': subject.code, 'total': total_score,
                'midterm_total': midterm_total, 'grade': grade, 'midterm_grade': midterm_grade,
                'remark': remark, 'midterm_remark': midterm_remark
            })

            student_complete_result, created = ResultModel.objects.get_or_create(
                session=session, term=term, student=student,
                defaults={'student_class': student_class, 'class_section': class_section, 'result': {},
                          'type': request.user.profile.type}
            )
            if not student_complete_result.result:
                student_complete_result.result = {}
            student_complete_result.result[subject.pk] = student_result
            student_complete_result.save()

        position = 1
        prev_score = -1
        for score in sorted(position_dict.keys(), reverse=True):
            students_at_score = position_dict[score]
            if score != prev_score:
                current_position = position
            for student in students_at_score:
                student_result = ResultModel.objects.filter(session=session, term=term, student=student).first()
                if student_result and student_result.result and subject.pk in student_result.result:
                    student_result.result[subject.pk]['position'] = current_position
                    student_result.save()
            position += len(students_at_score)
            prev_score = score

        position = 1
        prev_score = -1
        for score in sorted(midterm_dict.keys(), reverse=True):
            students_at_score = midterm_dict[score]
            if score != prev_score:
                current_position = position
            for student in students_at_score:
                student_result = ResultModel.objects.filter(session=session, term=term, student=student).first()
                if student_result and student_result.result and subject.pk in student_result.result:
                    student_result.result[subject.pk]['midterm_position'] = current_position
                    student_result.save()
            position += len(students_at_score)
            prev_score = score

        highest_in_class = max(total_scores) if total_scores else 0
        lowest_in_class = min(total_scores) if total_scores else 0
        total_mark_obtained = sum(total_scores)
        average_score = round(total_mark_obtained / out_of, 1) if out_of else 0

        midterm_highest_in_class = max(midterm_scores) if midterm_scores else 0
        midterm_lowest_in_class = min(midterm_scores) if midterm_scores else 0
        midterm_total_mark_obtained = sum(midterm_scores)
        midterm_average_score = round(midterm_total_mark_obtained / out_of, 1) if out_of else 0

        uploaded_by = 'superadmin'
        if not request.user.is_superuser:
            uploaded_by = f"{request.user.profile.staff.surname.title()} {request.user.profile.staff.last_name.title()}"

        result_stat_data = {
            'highest_in_class': highest_in_class, 'lowest_in_class': lowest_in_class,
            'total_mark_obtained': total_mark_obtained, 'average_score': average_score,
            'midterm_highest_in_class': midterm_highest_in_class, 'midterm_lowest_in_class': midterm_lowest_in_class,
            'midterm_total_mark_obtained': midterm_total_mark_obtained, 'midterm_average_score': midterm_average_score,
            'number_of_students': out_of, 'has_exam': has_exam,
            'updated_at': datetime.now().strftime("%d %B %Y"), 'updated_by': uploaded_by
        }

        complete_result_stat, created = ResultStatisticModel.objects.get_or_create(
            session=session, term=term, student_class=student_class, class_section=class_section,
            defaults={'result_statistic': {}}
        )
        if not complete_result_stat.result_statistic:
            complete_result_stat.result_statistic = {}
        complete_result_stat.result_statistic[subject.pk] = result_stat_data
        complete_result_stat.save()

        ResultUploadedModel.objects.update_or_create(
            session=session, term=term, subject=subject, student_class=student_class, class_section=class_section,
            defaults={'user': request.user, 'ca_uploaded': has_ca, 'exam_uploaded': has_exam,
                      'type': request.user.profile.type}
        )

        messages.success(request, 'Result Uploaded Successfully')
        return redirect(reverse('result_create'))

    if 'student_class' not in request.session:
        return redirect(reverse('result_create'))

    class_pk = request.session.pop('student_class')
    class_section_pk = request.session.pop('class_section')
    subject_pk = request.session.pop('subject')

    student_class = ClassesModel.objects.get(pk=class_pk)
    class_section = ClassSectionModel.objects.get(pk=class_section_pk)
    subject = SubjectsModel.objects.get(pk=subject_pk)

    is_update = request.session.pop('is_update', False)
    if is_update:
        session = SessionModel.objects.get(pk=request.session.pop('session_pk'))
        term = TermModel.objects.get(pk=request.session.pop('term_pk'))
    else:
        sch_setting = SchoolGeneralInfoModel.objects.first()
        academic_q = Q(type=request.user.profile.type) if sch_setting.separate_school_section else Q()
        academic_setting = SchoolAcademicInfoModel.objects.filter(academic_q).first()
        session = academic_setting.session
        term = academic_setting.term

    student_list = StudentsModel.objects.filter(student_class=student_class, class_section=class_section, status='active', subject_group__subjects=subject).order_by('surname')

    full_list = {}
    for student in student_list:
        result_obj = ResultModel.objects.filter(session=session, term=term, student=student).first()
        student_result = result_obj.result.get(str(subject_pk)) if result_obj and result_obj.result else {}
        full_list[student.id] = {'student': student, 'result': student_result}

    context = {
        'class': student_class,
        'section': class_section,
        'subject': subject,
        'is_update': is_update,
        'full_list': full_list,
        'academic_setting': {'session': session, 'term': term},
        'result_field_list': ResultFieldModel.objects.filter(student_class=student_class,
                                                             class_section=class_section).order_by('order')
    }
    if is_update:
        context['session_pk'] = session.pk
        context['term_pk'] = term.pk

    return render(request, 'result/result/upload.html', context=context)


@login_required
def uploaded_result(request):
    if all(k in request.GET for k in ['subject', 'student_class', 'class_section']):
        request.session['student_class'] = request.GET['student_class']
        request.session['class_section'] = request.GET['class_section']
        request.session['subject'] = request.GET['subject']
        return redirect(reverse('result_index'))

    sch_setting = SchoolGeneralInfoModel.objects.first()
    academic_q = Q(type=request.user.profile.type) if sch_setting.separate_school_section else Q()
    academic_setting = SchoolAcademicInfoModel.objects.filter(academic_q).first()

    if academic_setting:
        result_list = ResultUploadedModel.objects.filter(session=academic_setting.session,
                                                         term=academic_setting.term).filter(academic_q)
    else:
        result_list = ResultUploadedModel.objects.none()

    context = {'result_list': result_list}
    return render(request, 'result/result/uploaded_result.html', context)


# Create your views here.
def text_result_create_view(request):
    if request.method == 'POST':
        pass

    class_pk = request.GET.get('student_class')
    class_section_pk = request.GET.get('class_section')

    student_class = ClassesModel.objects.get(pk=class_pk)
    class_section = ClassSectionModel.objects.get(pk=class_section_pk)

    student_list = StudentsModel.objects.filter(student_class=student_class, class_section=class_section).order_by(
        'surname')
    school_setting = SchoolGeneralInfoModel.objects.first()
    if school_setting.separate_school_section:
        academic_setting = SchoolAcademicInfoModel.objects.filter(type=request.user.profile.type).first()
    else:
        academic_setting = SchoolAcademicInfoModel.objects.first()
    session = academic_setting.session
    term = academic_setting.term

    context = {
        'student_class': student_class,
        'class_section': class_section,
        'student_list': student_list,

    }

    return render(request, 'result/result/text_result_student_list.html', context=context)


def text_result_upload_view(request, student_pk):
    school_setting = SchoolGeneralInfoModel.objects.first()
    if school_setting.separate_school_section:
        academic_setting = SchoolAcademicInfoModel.objects.filter(type=request.user.profile.type).first()
    else:
        academic_setting = SchoolAcademicInfoModel.objects.first()
    session = academic_setting.session
    term = academic_setting.term
    student = StudentsModel.objects.get(pk=student_pk)
    student_class = student.student_class
    class_section = student.class_section
    result = TextBasedResultModel.objects.filter(term=term, session=session, student=student).first()

    if request.method == 'POST':
        text_result_list = TextResultModel.objects.filter(student_class__in=[student_class]).filter(
            class_section__in=[class_section]).order_by('order')

        result_record = {}
        for field in text_result_list:
            if '{}'.format(field.name) in request.POST:
                field_result = {
                    'rating': request.POST.get('{}'.format(field.name)),
                    'comment': request.POST.get('{}'.format(field.name + '_comment')),
                    'tick': field.name + '_tick' in request.POST
                }
                result_record[field.name.upper()] = field_result

        uploaded_result = TextBasedResultModel.objects.filter(session=session, term=term, student=student).first()
        if uploaded_result:
            uploaded_result.result = result_record
        else:
            uploaded_result = TextBasedResultModel.objects.create(session=session, term=term, student=student,
                                                                  student_class=student_class,
                                                                  class_section=class_section,
                                                                  result=result_record, type=request.user.profile.type)
        uploaded_result.save()

        if uploaded_result.id:
            messages.success(request, 'Student Results computed successfully')

        return redirect(reverse('text_based_result_index', kwargs={'student_pk': student.pk}))

    school_setting = SchoolGeneralInfoModel.objects.first()
    if school_setting.separate_school_section:
        result_category_list = TextResultCategoryModel.objects.filter(session=session, term=term,
                                                                      type=request.user.profile.type,
                                                                      student_class__in=[student.student_class.id],
                                                                      class_section__in=[
                                                                          student.class_section.id]).order_by(
            'order')
        result_field_list = TextResultModel.objects.filter(type=request.user.profile.type,
                                                           student_class__in=[student.student_class.id],
                                                           class_section__in=[student.class_section.id]).order_by(
            'name')
    else:
        result_category_list = TextResultCategoryModel.objects.filter(session=session, term=term,
                                                                      student_class__in=[student.student_class.id],
                                                                      class_section__in=[
                                                                          student.class_section.id]).order_by('order')
        result_field_list = TextResultModel.objects.filter(student_class__in=[student.student_class.id],
                                                           class_section__in=[student.class_section.id]).order_by(
            'name')

    school_setting = SchoolGeneralInfoModel.objects.first()
    if school_setting.separate_school_section:
        result_setting = ResultSettingModel.objects.filter(type=request.user.profile.type).first()
    else:
        result_setting = ResultSettingModel.objects.first()
    is_form_teacher = False
    class_info = ClassSectionInfoModel.objects.filter(student_class=student_class, section=class_section).first()
    staff = request.user.profile.staff
    if class_info:
        if staff == class_info.form_teacher or staff == class_info.assistant_form_teacher:
            is_form_teacher = True
    allowed_subjects = TextResultCategoryModel.objects.filter(session=session, term=term, teachers__in=[staff])
    can_upload = is_form_teacher or len(allowed_subjects) > 0
    context = {
        'student': student,
        'academic_setting': academic_setting,
        'result_list': result,
        'result_category_list': result_category_list,
        'result_field_list': result_field_list,
        'result_setting': result_setting,
        'staff_is_form_teacher': is_form_teacher,
        'allowed_subjects': allowed_subjects,
        'can_upload': can_upload
    }

    return render(request, 'result/result/text_result_upload.html', context=context)


def result_check_view(request):
    """  """
    school_setting = SchoolGeneralInfoModel.objects.first()
    if request.method == 'POST':
        if 'student_id' in request.POST:
            id = request.POST.get('student_id')
            student = StudentsModel.objects.filter(registration_number=id).first()
            if student:
                return redirect(reverse('result_student_detail', kwargs={'pk': student.id}))
            else:
                messages.error(request, 'Student with registration number {} not found'.format(id))
                return redirect(reverse('result_check'))
        student_class_pk = request.POST['student_class']
        stud_class = ClassesModel.objects.get(pk=student_class_pk)
        class_section_pk = request.POST['class_section']
        subject_pk = request.POST['subject']
        subject = SubjectsModel.objects.get(pk=subject_pk)

        if school_setting.separate_school_section:
            result_setting = ResultSettingModel.objects.filter(type=request.user.profile.type).first()
        else:
            result_setting = ResultSettingModel.objects.first()
        is_allowed = False
        if result_setting.allowed_user != 'any':
            current_user = request.user.profile.staff
            if current_user:
                if result_setting.allowed_user == 'form teacher':
                    student_class = ClassSectionInfoModel.objects.filter(student_class=student_class_pk,
                                                                         section=class_section_pk).first()
                    if student_class:
                        if student_class.form_teacher == current_user or student_class.assistant_form_teacher == current_user:
                            is_allowed = True
                        else:
                            message = 'ONLY CLASS FORM TEACHER CAN VIEW CLASS RESULT'
                    else:
                        # if the class don't have a form teacher assigned
                        message = 'CLASS HAS NO FORM TEACHER, AND ONLY FORM TEACHERS CAN VIEW CLASS RESULTS'
                elif result_setting.allowed_user == 'subject teacher':
                    subject_info = ClassSectionSubjectTeacherModel.objects.filter(subject=subject_pk,
                                                                                  student_class__in=[student_class_pk],
                                                                                  class_section__in=[
                                                                                      class_section_pk]).first()
                    if subject_info:
                        if current_user in subject_info.teachers.all():
                            is_allowed = True
                        else:
                            message = 'ONLY {} TEACHERS FOR THE CLASS CAN VIEW SUBJECT RESULT'.format(
                                subject.name.upper())
                    else:
                        # if the subject don't have teachers assigned
                        message = 'SUBJECT HAS NO ASSIGNED TEACHER, ONLY SUBJECT TEACHERS CAN VIEW RESULTS'

                elif result_setting.allowed_user == 'both':
                    student_class = ClassSectionInfoModel.objects.filter(student_class=student_class_pk,
                                                                         section=class_section_pk).first()
                    if student_class:
                        if student_class.form_teacher == current_user or student_class.assistant_form_teacher == current_user:
                            is_allowed = True

                    subject_info = ClassSectionSubjectTeacherModel.objects.filter(subject=subject_pk,
                                                                                  student_class__in=[student_class_pk],
                                                                                  class_section__in=[
                                                                                      class_section_pk]).first()
                    if subject_info:
                        if current_user in subject_info.teachers.all():
                            is_allowed = True
                    if not is_allowed:
                        message = 'ONLY FORM TEACHER OR SUBJECT TEACHERS CAN VIEW RESULTS'

                else:
                    message = 'ADMINISTRATIVE DATA ERROR, CONTACT TECH TEAM'
            else:
                message = 'USER IDENTITY NOT KNOWN, ACCESS DENIED'
        else:
            is_allowed = True
        if request.user.is_superuser:
            is_allowed = True

        if stud_class.result_type == 'text':
            messages.warning(request, 'Use Class Result to check results for this class')
            return redirect(reverse('result_check'))

        if not is_allowed:
            messages.error(request, message)
            return redirect(reverse('result_check'))

        request.session['student_class'] = student_class_pk
        request.session['class_section'] = class_section_pk
        request.session['subject'] = subject_pk
        return redirect(reverse('result_index'))

    if school_setting.separate_school_section:
        class_list = ClassesModel.objects.filter(type=request.user.profile.type).order_by('name')
        subject_list = SubjectsModel.objects.filter(type=request.user.profile.type).order_by('name')
        session_list = SessionModel.objects.filter(type=request.user.profile.type).order_by('id')
    else:
        class_list = ClassesModel.objects.all().order_by('name')
        subject_list = SubjectsModel.objects.all().order_by('name')
        session_list = SessionModel.objects.all().order_by('id')

    context = {
        'class_list': class_list,
        'subject_list': subject_list,
        'session_list': session_list,
    }
    return render(request, 'result/result/check.html', context=context)


def result_spreadsheet_check_view(request):
    school_setting = SchoolGeneralInfoModel.objects.first()
    if request.method == 'POST':
        student_class_pk = request.POST['student_class']
        student_class = ClassesModel.objects.get(pk=student_class_pk)
        session = SessionModel.objects.get(pk=request.POST['session_pk'])
        term = TermModel.objects.get(pk=request.POST['term_pk'])

        result_list = ResultModel.objects.filter(term=term, session=session, student__student_class=student_class)
        result_stat_list = ResultStatisticModel.objects.filter(term=term, session=session, student_class=student_class)

        class_section_pk = request.POST.get('class_section')
        section_selected = False
        class_section = None

        if class_section_pk:
            class_section = ClassSectionModel.objects.filter(pk=class_section_pk).first()
            if class_section:
                section_selected = True
                result_list = result_list.filter(class_section=class_section)
                result_stat_list = result_stat_list.filter(class_section=class_section)

        if class_section:
            class_detail = ClassSectionInfoModel.objects.filter(student_class=student_class,
                                                                section=class_section).first()
        else:
            class_detail = ClassSectionInfoModel.objects.filter(student_class=student_class).first()

        subject_list = class_detail.subjects.all() if class_detail and class_detail.subjects.exists() else SubjectsModel.objects.all()

        result_list = sorted(result_list, key=lambda x: (x.total_score / x.number_of_course) if (
                    x.total_score and x.number_of_course and x.number_of_course > 0) else 0, reverse=True)

        context = {
            'session': session,
            'term': term,
            'student_class': student_class,
            'class_section': class_section,
            'result_list': result_list,
            'result_stat_list': result_stat_list,
            'subject_list': subject_list,
            'section_selected': section_selected,
            'site_info': school_setting,
        }

        return render(request, 'result/result/spreadsheet_detail.html', context)

    if school_setting.separate_school_section:
        class_list = ClassesModel.objects.filter(type=request.user.profile.type).order_by('name')
        subject_list = SubjectsModel.objects.filter(type=request.user.profile.type).order_by('name')
        session_list = SessionModel.objects.filter(type=request.user.profile.type).order_by('id')
    else:
        class_list = ClassesModel.objects.all().order_by('name')
        subject_list = SubjectsModel.objects.all().order_by('name')
        session_list = SessionModel.objects.all().order_by('id')

    context = {
        'class_list': class_list,
        'subject_list': subject_list,
        'session_list': session_list,
        'term_list': TermModel.objects.all().order_by('order'),
    }
    return render(request, 'result/result/spreadsheet.html', context)


def result_archive_check_view(request):
    """  """
    school_setting = SchoolGeneralInfoModel.objects.first()
    if 'POST' == request.method:
        session_pk = request.POST['session_pk']
        term_pk = request.POST['term_pk']
        student_class_pk = request.POST['student_class']
        class_section_pk = request.POST['class_section']
        subject_pk = request.POST['subject']
        subject = SubjectsModel.objects.get(pk=subject_pk)
        session = SessionModel.objects.get(pk=session_pk)
        term = TermModel.objects.get(pk=term_pk)
        student_class = ClassesModel.objects.get(pk=student_class_pk)
        class_section = ClassSectionModel.objects.get(pk=class_section_pk)

        if student_class.result_type == 'text':
            messages.warning(request, 'Please use Student\'s Registration Number')
            return redirect(reverse('result_check'))

        if school_setting.separate_school_section:
            result_setting = ResultSettingModel.objects.filter(type=request.user.profile.type).first()
        else:
            result_setting = ResultSettingModel.objects.first()
        is_allowed = False
        if result_setting.allowed_user != 'any':
            current_user = request.user.profile.staff
            if current_user:
                if result_setting.allowed_user == 'form teacher':
                    student_class_info = ClassSectionInfoModel.objects.filter(student_class=student_class_pk,
                                                                              section=class_section_pk).first()
                    if student_class_info:
                        if student_class_info.form_teacher == current_user or student_class_info.assistant_form_teacher == current_user:
                            is_allowed = True
                        else:
                            message = 'ONLY CLASS FORM TEACHER CAN VIEW CLASS RESULT'
                    else:
                        message = 'CLASS HAS NO FORM TEACHER, AND ONLY FORM TEACHERS CAN VIEW CLASS RESULTS'
                elif result_setting.allowed_user == 'subject teacher':
                    subject_info = ClassSectionSubjectTeacherModel.objects.filter(subject=subject_pk,
                                                                                  student_class__in=[student_class_pk],
                                                                                  class_section__in=[
                                                                                      class_section_pk]).first()
                    if subject_info:
                        if current_user in subject_info.teachers.all():
                            is_allowed = True
                        else:
                            message = 'ONLY {} TEACHERS FOR THE CLASS CAN VIEW SUBJECT RESULT'.format(
                                subject.name.upper())
                    else:
                        message = 'SUBJECT HAS NO ASSIGNED TEACHER, ONLY SUBJECT TEACHERS CAN VIEW RESULTS'

                elif result_setting.allowed_user == 'both':
                    student_class_info = ClassSectionInfoModel.objects.filter(student_class=student_class_pk,
                                                                              section=class_section_pk).first()
                    if student_class_info:
                        if student_class_info.form_teacher == current_user or student_class_info.assistant_form_teacher == current_user:
                            is_allowed = True

                    subject_info = ClassSectionSubjectTeacherModel.objects.filter(subject=subject_pk,
                                                                                  student_class__in=[student_class_pk],
                                                                                  class_section__in=[
                                                                                      class_section_pk]).first()
                    if subject_info:
                        if current_user in subject_info.teachers.all():
                            is_allowed = True
                    if not is_allowed:
                        message = 'ONLY FORM TEACHER OR SUBJECT TEACHERS CAN VIEW RESULTS'

                else:
                    message = 'ADMINISTRATIVE DATA ERROR, CONTACT TECH TEAM'
            else:
                message = 'USER IDENTITY NOT KNOWN, ACCESS DENIED'
        else:
            is_allowed = True
        if request.user.is_superuser:
            is_allowed = True

        if not is_allowed:
            messages.error(request, message)
            return redirect(reverse('result_check'))

        result_list = ResultModel.objects.filter(student_class=student_class, class_section=class_section, term=term,
                                                 session=session).order_by(
            'student__surname')
        full_list = {}
        for result in result_list:
            student = result.student
            if subject_pk in result.result:
                student_result = result.result[subject_pk]
                if student_result['total']:
                    full_list[student.id] = {
                        'student': student,
                        'result': student_result
                    }

        context = {
            'student_class': student_class,
            'class_section': class_section,
            'session': session,
            'term': term,
            'subject': subject,
            'full_list': full_list,
            'result_setting': ResultSettingModel.objects.get(pk=1),
            'result_field_list': ResultFieldModel.objects.filter(student_class__in=[student_class]).filter(
                class_section__in=[class_section]),
            'result_stat': ResultStatisticModel.objects.filter(term=term, session=session, class_section=class_section,
                                                               student_class=student_class).first()

        }

        return render(request, 'result/result/index.html', context=context)
    return redirect(reverse('result_check'))


def result_index_view(request):
    """  """
    school_setting = SchoolGeneralInfoModel.objects.first()
    if school_setting.separate_school_section:
        academic_setting = SchoolAcademicInfoModel.objects.filter(type=request.user.profile.type).first()
    else:
        academic_setting = SchoolAcademicInfoModel.objects.first()

    session = academic_setting.session
    term = academic_setting.term
    if 'student_class' not in request.session:
        return redirect(reverse('result_check'))
    class_pk = request.session['student_class']
    section_pk = request.session['class_section']
    student_class = ClassesModel.objects.get(pk=class_pk)
    class_section = ClassSectionModel.objects.get(pk=section_pk)
    subject_pk = request.session['subject']
    subject = SubjectsModel.objects.get(pk=subject_pk)

    del request.session['student_class']
    del request.session['class_section']
    del request.session['subject']

    student_list = StudentsModel.objects.filter(student_class=student_class, class_section=class_section,
                                                subject_group__subjects=subject).order_by('surname')
    full_list = {}
    for student in student_list:
        student_result = ResultModel.objects.filter(session=session, term=term, class_section=class_section,
                                                    student_class=student_class, student=student).first()

        if student_result:
            if student_result.result.get(subject_pk):
                student_result = student_result.result[subject_pk]
            else:
                student_result = {}
        else:
            student_result = {}

        full_list[student.id] = {
            'student': student,
            'result': student_result
        }

    context = {
        'student_class': student_class,
        'class_section': class_section,
        'session': session,
        'term': term,
        'subject': subject,
        'full_list': full_list,
        'result_setting': ResultSettingModel.objects.get(pk=1),
        'result_field_list': ResultFieldModel.objects.filter(student_class__in=[student_class]).filter(
            class_section__in=[class_section]),
        'result_stat': ResultStatisticModel.objects.filter(term=term, session=session, class_section=class_section,
                                                           student_class=student_class).first()

    }

    return render(request, 'result/result/index.html', context=context)


def text_result_index_view(request, student_pk):
    school_setting = SchoolGeneralInfoModel.objects.first()
    if school_setting.separate_school_section:
        academic_setting = SchoolAcademicInfoModel.objects.filter(type=request.user.profile.type).first()
    else:
        academic_setting = SchoolAcademicInfoModel.objects.first()
    session = academic_setting.session
    term = academic_setting.term
    student = StudentsModel.objects.get(pk=student_pk)
    result = TextBasedResultModel.objects.filter(term=term, session=session, student=student).first()

    if school_setting.separate_school_section:
        result_category_list = TextResultCategoryModel.objects.filter(term=term,
                                                                      student_class__in=[student.student_class.id],
                                                                      class_section__in=[student.class_section.id],
                                                                      session=session,
                                                                      type=request.user.profile.type).order_by(
            'order')
        result_field_list = TextResultModel.objects.filter(type=request.user.profile.type,
                                                           student_class__in=[student.student_class.id],
                                                           class_section__in=[student.class_section.id]).order_by(
            'name')
    else:
        result_category_list = TextResultCategoryModel.objects.filter(term=term, session=session,
                                                                      student_class__in=[student.student_class.id],
                                                                      class_section__in=[
                                                                          student.class_section.id]).order_by('order')
        result_field_list = TextResultModel.objects.filter(student_class__in=[student.student_class.id],
                                                           class_section__in=[student.class_section.id]).order_by(
            'name')

    context = {
        'student': student,
        'academic_setting': academic_setting,
        'result_list': result,
        'result_category_list': result_category_list,
        'result_field_list': result_field_list,
    }

    return render(request, 'result/result/text_result_index.html', context=context)


def result_class_list_view(request):
    """"""
    if request.method == 'POST':
        class_pk = request.POST['student_class']
        section_pk = request.POST['class_section']
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            result_setting = ResultSettingModel.objects.filter(type=request.user.profile.type).first()
        else:
            result_setting = ResultSettingModel.objects.first()
        is_allowed = False
        if result_setting.allowed_user != 'any':
            current_user = request.user.profile.staff
            if current_user:
                student_class_info = ClassSectionInfoModel.objects.filter(student_class=class_pk,
                                                                          section=section_pk).first()
                if student_class_info:
                    if student_class_info.form_teacher == current_user or student_class_info.assistant_form_teacher == current_user:
                        is_allowed = True
                    else:
                        message = 'ONLY CLASS FORM TEACHER CAN VIEW CLASS RESULT'
                else:
                    message = 'CLASS HAS NO FORM TEACHER, AND ONLY FORM TEACHERS CAN VIEW CLASS RESULTS'
            else:
                message = 'USER IDENTITY NOT KNOWN, ACCESS DENIED'
        else:
            is_allowed = True
        if request.user.is_superuser:
            is_allowed = True

        if not is_allowed:
            messages.error(request, message)
            return redirect(reverse('result_check'))
        student_class = ClassesModel.objects.get(pk=class_pk)
        class_section = ClassSectionModel.objects.get(pk=section_pk)
        student_list = StudentsModel.objects.filter(student_class=student_class, class_section=class_section).order_by(
            'surname')

        context = {
            'student_class': student_class,
            'class_section': class_section,
            'student_list': student_list
        }
        return render(request, 'result/result/class_list.html', context=context)

    return redirect(reverse('result_check'))


def result_student_detail_view(request, pk):
    school_setting = SchoolGeneralInfoModel.objects.first()
    if school_setting.separate_school_section:
        academic_setting = SchoolAcademicInfoModel.objects.filter(type=request.user.profile.type).first()
    else:
        academic_setting = SchoolAcademicInfoModel.objects.first()

    student = StudentsModel.objects.get(pk=pk)
    term = academic_setting.term
    session = academic_setting.session
    student_class = student.student_class
    class_section = student.class_section

    result = ResultModel.objects.filter(term=term, session=session, student=student).first()

    session_list = ResultModel.objects.filter(student=student)
    student_session_list = []
    for session_result in session_list:
        if session_result.session not in student_session_list:
            student_session_list.append(session_result.session)
    behaviour_result = ResultBehaviourComputeModel.objects.filter(term=term, session=session, student=student).first()

    if school_setting.separate_school_section:
        behaviour_category_list = ResultBehaviourCategoryModel.objects.filter(type=request.user.profile.type).order_by(
            'name')
        behaviour_list = ResultBehaviourModel.objects.filter(type=request.user.profile.type,
                                                             student_class__in=[student.student_class.id],
                                                             class_section__in=[student.class_section.id]).order_by(
            'name')
    else:
        behaviour_category_list = ResultBehaviourCategoryModel.objects.all().order_by('name')
        behaviour_list = ResultBehaviourModel.objects.filter(student_class__in=[student.student_class.id],
                                                             class_section__in=[student.class_section.id]).order_by(
            'name')
    if student_class.result_type == 'text':
        if school_setting.separate_school_section:
            result_category_list = TextResultCategoryModel.objects.filter(term=term, session=session,
                                                                          type=request.user.profile.type).order_by(
                'order')
            result_field_list = TextResultModel.objects.filter(type=request.user.profile.type,
                                                               student_class__in=[student.student_class.id],
                                                               class_section__in=[student.class_section.id]).order_by(
                'name')
        else:
            result_category_list = TextResultCategoryModel.objects.filter(term=term, session=session).order_by('order')
            result_field_list = TextResultModel.objects.filter(student_class__in=[student.student_class.id],
                                                               class_section__in=[student.class_section.id]).order_by(
                'name')

        context = {
            'student': student,
            'result_list': result,
            'academic_setting': academic_setting,
            'behaviour_category_list': behaviour_category_list,
            'behaviour_list': behaviour_list,
            'behaviour_result': behaviour_result,
            'result_category_list': result_category_list,
            'result_field_list': result_field_list,
            'student_session_list': student_session_list
        }
        return render(request, 'result/result/text_result/student_detail.html', context=context)

    result_stat = ResultStatisticModel.objects.filter(term=term, session=session,
                                                      student_class=student_class, class_section=class_section).first()
    result_remark = ResultRemarkModel.objects.filter(term=term, session=session, student=student).first()

    if result:
        for key, student_result in result.result.items():
            if result_stat and key in result_stat.result_statistic:
                student_result['highest_in_class'] = result_stat.result_statistic[key]['highest_in_class']
                student_result['lowest_in_class'] = result_stat.result_statistic[key]['lowest_in_class']

    context = {
        'student': student,
        'result': result,
        'result_stat': result_stat,
        'result_remark': result_remark,
        'academic_setting': academic_setting,
        'behaviour_category_list': behaviour_category_list,
        'behaviour_list': behaviour_list,
        'behaviour_result': behaviour_result,
        'student_session_list': student_session_list,

    }
    return render(request, 'result/result/student_detail.html', context=context)


def result_affective_domain_view(request, pk):
    school_setting = SchoolGeneralInfoModel.objects.first()
    if school_setting.separate_school_section:
        academic_setting = SchoolAcademicInfoModel.objects.filter(type=request.user.profile.type).first()
    else:
        academic_setting = SchoolAcademicInfoModel.objects.first()
    session = academic_setting.session
    term = academic_setting.term
    student = StudentsModel.objects.get(pk=pk)
    student_class = student.student_class
    class_section = student.class_section
    result = ResultModel.objects.filter(term=term, session=session, student=student).first()

    behaviour_result = ResultBehaviourComputeModel.objects.filter(term=term, session=session, student=student).first()

    if request.method == 'POST':
        result_behaviour_list = ResultBehaviourModel.objects.filter(student_class__in=[student_class]).filter(
            class_section__in=[class_section]).order_by('order')

        behaviour_record = {}
        for field in result_behaviour_list:
            if '{}'.format(field.name) in request.POST:
                field_result = request.POST.get('{}'.format(field.name))
                behaviour_record[field.name.upper()] = field_result
        behaviour_record['form_teacher_comment'] = request.POST['form_teacher_comment']
        behaviour_record['head_teacher_comment'] = request.POST['head_teacher_comment']
        behaviour_record['area_of_focus'] = request.POST['area_of_focus']
        behaviour_record['total_attendance'] = request.POST['total_attendance'].strip()
        behaviour_record['present_attendance'] = request.POST['present_attendance'].strip()

        result_stat, created = ResultBehaviourComputeModel.objects.update_or_create(
            session=session, term=term, student=student,
            defaults={'result_remark': behaviour_record, 'user': request.user}
        )
        if created or result_stat:
            messages.success(request, 'student behaviours  computed successfully')
        return redirect(reverse('result_student_detail', kwargs={'pk': student.pk}))

    if school_setting.separate_school_section:
        behaviour_category_list = ResultBehaviourCategoryModel.objects.filter(type=request.user.profile.type).order_by(
            'name')
        behaviour_list = ResultBehaviourModel.objects.filter(type=request.user.profile.type,
                                                             student_class__in=[student.student_class.id],
                                                             class_section__in=[student.class_section.id]).order_by(
            'name')
    else:
        behaviour_category_list = ResultBehaviourCategoryModel.objects.all().order_by('name')
        behaviour_list = ResultBehaviourModel.objects.filter(student_class__in=[student.student_class.id],
                                                             class_section__in=[student.class_section.id]).order_by(
            'name')

    context = {
        'student': student,
        'academic_setting': academic_setting,
        'result_list': result,
        'behaviour_category_list': behaviour_category_list,
        'behaviour_list': behaviour_list,
        'behaviour_result': behaviour_result,
    }
    return render(request, 'result/result/affective_domain.html', context=context)


def result_student_sheet_view(request, pk):
    result_type = request.GET.get('type', None)
    school_setting = SchoolGeneralInfoModel.objects.first()
    if school_setting.separate_school_section:
        academic_setting = SchoolAcademicInfoModel.objects.filter(type=request.user.profile.type).first()
        academic_info = AcademicSettingModel.objects.filter(type=request.user.profile.type).first()
    else:
        academic_setting = SchoolAcademicInfoModel.objects.first()
        academic_info = AcademicSettingModel.objects.first()

    session = academic_setting.session
    term = academic_setting.term
    student = StudentsModel.objects.get(pk=pk)
    student_class = student.student_class
    class_section = student.class_section
    result = ResultModel.objects.filter(term=term, session=session, student=student).first()
    behaviour_result = ResultBehaviourComputeModel.objects.filter(term=term, session=session,
                                                                  student=student).first()

    result_stat = ResultStatisticModel.objects.filter(term=term, session=session, student_class=student_class,
                                                      class_section=class_section).first()

    result_remark = ResultRemarkModel.objects.filter(term=term, session=session,
                                                     student=student).first()
    total_score = 0
    number_of_course = 0
    average = 0
    total_lowest = 0
    class_minimum = 0
    if result and result.result and result_stat and result_stat.result_statistic:
        for key, student_result in result.result.items():
            if key in result_stat.result_statistic:
                student_result['highest_in_class'] = result_stat.result_statistic[key].get('highest_in_class', 0)
                student_result['lowest_in_class'] = result_stat.result_statistic[key].get('lowest_in_class', 0)
                total_lowest += student_result['lowest_in_class']

        number_of_course = len(result.result)
        class_minimum = round((total_lowest / (100 * number_of_course)) * 100) if number_of_course else 0

        total_score = sum(value.get('total', 0) for value in result.result.values())
        average = round((total_score / (100 * number_of_course)) * 100) if number_of_course else 0

        for key, student_result in result.result.items():
            if key in result_stat.result_statistic:
                stat_data = result_stat.result_statistic[key]
                student_result.update({
                    'average_score': stat_data.get('average_score', ''),
                    'midterm_highest_in_class': stat_data.get('midterm_highest_in_class', ''),
                    'midterm_lowest_in_class': stat_data.get('midterm_lowest_in_class', ''),
                    'midterm_average_score': stat_data.get('midterm_average_score', ''),
                    'number_of_student': stat_data.get('number_of_students', '')
                })

    if school_setting.separate_school_section:
        field_list = ResultFieldModel.objects.filter(student_class=student_class,
                                                     class_section=class_section,
                                                     type=request.user.profile.type).order_by('order')
        grade_list = ResultGradeModel.objects.filter(student_class=student_class,
                                                     class_section=class_section,
                                                     type=request.user.profile.type).order_by('order')
        mid_grade_list = MidResultGradeModel.objects.filter(type=request.user.profile.type).order_by('order')
        behaviour_category_list = ResultBehaviourCategoryModel.objects.filter(type=request.user.profile.type).order_by(
            'name')
    else:
        field_list = ResultFieldModel.objects.filter(student_class=student_class,
                                                     class_section=class_section).order_by('order')
        grade_list = ResultGradeModel.objects.filter(student_class=student_class,
                                                     class_section=class_section).order_by('order')
        behaviour_category_list = ResultBehaviourCategoryModel.objects.all().order_by('name')
        mid_grade_list = MidResultGradeModel.objects.all().order_by('order')
    subject_list = student.subject_group.subjects.all() if student.subject_group else []

    midterm_max = sum(field.max_mark for field in field_list if field.mid_term)
    context = {}
    if student_class.result_type in ['text', 'mix']:
        text_result = TextBasedResultModel.objects.filter(term=term, session=session, student=student).first()
        q_filter = Q(type=request.user.profile.type) if school_setting.separate_school_section else Q()
        result_category_list = TextResultCategoryModel.objects.filter(q_filter, term=term, session=session,
                                                                      student_class=student.student_class,
                                                                      class_section=student.class_section).order_by(
            'order')
        result_field_list = TextResultModel.objects.filter(q_filter, student_class=student.student_class,
                                                           class_section=student.class_section).order_by('order')
        context.update({
            'result_list': text_result,
            'result_category_list': result_category_list,
            'result_field_list': result_field_list,
        })

    context.update({
        'student': student, 'academic_setting': academic_setting, 'academic_info': academic_info,
        'result': result, 'total_score': total_score, 'number_of_course': number_of_course,
        'average_score': average, 'result_remark': result_remark,
        'general_setting': SchoolGeneralInfoModel.objects.first(), 'subject_list': subject_list,
        'field_list': field_list, 'grade_list': grade_list, 'mid_grade_list': mid_grade_list,
        'behaviour_category_list': behaviour_category_list, 'behaviour_result': behaviour_result,
        'class_minimum': class_minimum, 'result_type': result_type, 'midterm_max': midterm_max,
    })
    return render(request, 'result/templates/main_result.html', context=context)


def result_archive_student_sheet_view(request, pk):
    session = SessionModel.objects.get(pk=request.GET.get('session_pk'))
    term = TermModel.objects.get(pk=request.GET.get('term_pk'))
    academic_setting = {'term': term, 'session': session}
    student = StudentsModel.objects.get(pk=pk)

    result = ResultModel.objects.filter(term=term, session=session, student=student).first()
    if not result:
        messages.error(request, "Result not found for the selected session and term.")
        return redirect(reverse('result_student_detail', kwargs={'pk': pk}))

    student_class = result.student_class
    class_section = result.class_section
    behaviour_result = ResultBehaviourComputeModel.objects.filter(term=term, session=session, student=student).first()
    result_stat = ResultStatisticModel.objects.filter(term=term, session=session, student_class=student_class,
                                                      class_section=class_section).first()
    result_remark = ResultRemarkModel.objects.filter(term=term, session=session, student=student).first()

    school_setting = SchoolGeneralInfoModel.objects.first()
    q_filter = Q(type=request.user.profile.type) if school_setting.separate_school_section else Q()

    if student_class.result_type == 'text':
        result_category_list = TextResultCategoryModel.objects.filter(q_filter, term=term, session=session).order_by(
            'order')
        result_field_list = TextResultModel.objects.filter(q_filter, student_class=student.student_class,
                                                           class_section=student.class_section).order_by('name')
        context = {
            'student': student, 'result_list': result, 'academic_setting': academic_setting,
            'behaviour_result': behaviour_result, 'result_category_list': result_category_list,
            'result_field_list': result_field_list, 'general_setting': school_setting,
        }
        return render(request, 'result/result/text_result/main_result_template.html', context=context)

    total_score, number_of_course, average, total_lowest, class_minimum = 0, 0, 0, 0, 0
    if result and result.result and result_stat and result_stat.result_statistic:
        for key, student_result in result.result.items():
            if key in result_stat.result_statistic:
                stat = result_stat.result_statistic[key]
                student_result['highest_in_class'] = stat.get('highest_in_class', 0)
                student_result['lowest_in_class'] = stat.get('lowest_in_class', 0)
                total_lowest += student_result['lowest_in_class']

        number_of_course = len(result.result)
        class_minimum = round((total_lowest / (100 * number_of_course)) * 100) if number_of_course else 0
        total_score = sum(value.get('total', 0) for value in result.result.values())
        average = round((total_score / (100 * number_of_course)) * 100) if number_of_course else 0

    field_list = ResultFieldModel.objects.filter(q_filter, student_class=student_class,
                                                 class_section=class_section).order_by('order')
    grade_list = ResultGradeModel.objects.filter(q_filter).order_by('order')
    behaviour_category_list = ResultBehaviourCategoryModel.objects.filter(q_filter).order_by('name')
    subject_list = SubjectsModel.objects.filter(id__in=result.result.keys())

    context = {
        'student': student, 'academic_setting': academic_setting, 'result': result,
        'total_score': total_score, 'number_of_course': number_of_course, 'average_score': average,
        'result_remark': result_remark, 'general_setting': school_setting, 'subject_list': subject_list,
        'field_list': field_list, 'grade_list': grade_list,
        'behaviour_category_list': behaviour_category_list, 'behaviour_result': behaviour_result,
        'class_minimum': class_minimum
    }
    return render(request, 'result/templates/main_result.html', context=context)


def select_result_cumulative_view(request):
    student_pk = request.GET.get('student_pk')
    session_pk = request.GET.get('session_pk')

    result = ResultModel.objects.filter(student__id=student_pk, session__id=session_pk).first()
    if result:
        student_class = result.student_class
        class_section = result.class_section
        return redirect(reverse('result_cumulative_sheet', kwargs={'student_pk': student_pk, 'session_pk': session_pk,
                                                                   'student_class': student_class.id,
                                                                   'class_section': class_section.id}))
    student = StudentsModel.objects.get(id=student_pk)
    student_class = student.student_class
    class_section = student.class_section
    return redirect(reverse('result_cumulative_sheet', kwargs={'student_pk': student_pk, 'session_pk': session_pk,
                                                               'student_class': student_class.id,
                                                               'class_section': class_section.id}))


def result_cumulative_sheet_view(request, student_pk, session_pk, student_class, class_section):
    session = SessionModel.objects.get(pk=session_pk)
    student = StudentsModel.objects.get(pk=student_pk)
    student_class_obj = ClassesModel.objects.filter(pk=student_class).first()

    if not student_class_obj or student_class_obj.result_type == 'text':
        messages.error(request, 'Cumulative results are not available for this class.')
        return redirect(request.META.get('HTTP_REFERER', reverse('admin_dashboard')))

    class_section_obj = ClassSectionModel.objects.filter(pk=class_section).first()

    first_term = TermModel.objects.filter(order=1).first()
    second_term = TermModel.objects.filter(order=2).first()
    third_term = TermModel.objects.filter(order=3).first()

    first_result = ResultModel.objects.filter(term=first_term, session=session, student=student,
                                              student_class=student_class_obj,
                                              class_section=class_section_obj).first() if first_term else None
    second_result = ResultModel.objects.filter(term=second_term, session=session, student=student,
                                               student_class=student_class_obj,
                                               class_section=class_section_obj).first() if second_term else None
    third_result = ResultModel.objects.filter(term=third_term, session=session, student=student,
                                              student_class=student_class_obj,
                                              class_section=class_section_obj).first() if third_term else None

    subject_list, cumulative_first, cumulative_second, cumulative_third, cumulative_total = {}, {}, {}, {}, {}
    cumulative_average, cumulative_grade, cumulative_remark = {}, {}, {}
    grade_list = ResultGradeModel.objects.filter(student_class=student_class_obj, class_section=class_section_obj)

    all_results = [first_result, second_result, third_result]
    for res in all_results:
        if res and res.result:
            for key, value in res.result.items():
                if key not in subject_list:
                    subject_list[key] = value.get('subject', 'Unknown Subject')

    first_total, second_total, third_total, course_count = 0, 0, 0, 0
    for key, value in subject_list.items():
        subject_total, term_count = 0, 0

        first_term_score = first_result.result[key].get('total',
                                                        0) if first_result and first_result.result and key in first_result.result else 0
        cumulative_first[key] = first_term_score
        if first_term_score > 0: subject_total += first_term_score; first_total += first_term_score; term_count += 1; course_count += 1

        second_term_score = second_result.result[key].get('total',
                                                          0) if second_result and second_result.result and key in second_result.result else 0
        cumulative_second[key] = second_term_score
        if second_term_score > 0: subject_total += second_term_score; second_total += second_term_score; term_count += 1; course_count += 1

        third_term_score = third_result.result[key].get('total',
                                                        0) if third_result and third_result.result and key in third_result.result else 0
        cumulative_third[key] = third_term_score
        if third_term_score > 0: subject_total += third_term_score; third_total += third_term_score; term_count += 1; course_count += 1

        cumulative_total[key] = subject_total
        subject_average = round(subject_total / term_count, 1) if term_count else 0
        cumulative_average[key] = subject_average

        grade, remark = next(
            ((g.name.upper(), g.remark.upper()) for g in grade_list if g.min_mark <= subject_average <= g.max_mark),
            ('', ''))
        cumulative_grade[key] = grade
        cumulative_remark[key] = remark

    total_score = first_total + second_total + third_total
    term_average = total_score / (len(subject_list) * 3) if subject_list else 0
    grade, remark = next(
        ((g.name.upper(), g.remark.upper()) for g in grade_list if g.min_mark <= term_average <= g.max_mark), ('', ''))

    context = {
        'student': student, 'subject_list': subject_list, 'cumulative_first': cumulative_first,
        'cumulative_second': cumulative_second, 'cumulative_third': cumulative_third,
        'cumulative_total': cumulative_total, 'cumulative_average': cumulative_average,
        'cumulative_grade': cumulative_grade, 'cumulative_remark': cumulative_remark,
        'general_setting': SchoolGeneralInfoModel.objects.first(), 'grade_list': grade_list,
        'total_score': total_score, 'term_average': round(term_average, 1),
        'grade': grade, 'remark': remark, 'session': session
    }
    return render(request, 'result/templates/cumulative_result.html', context=context)


class TextResultCategoryCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = TextResultCategoryModel
    permission_required = 'result.add_resultfieldmodel'
    form_class = TextResultCategoryForm
    success_message = 'Text Based Result Category Added Successfully'
    template_name = 'result/text_result_category/index.html'

    def get_success_url(self):
        return reverse('text_result_category_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            context['class_list'] = ClassesModel.objects.filter(Q(result_type='text') | Q(result_type='mix'),
                                                                type=self.request.user.profile.type).order_by('name')
            context['class_section_list'] = ClassSectionModel.objects.filter(
                type=self.request.user.profile.type).order_by('name')
            context['text_result_category_list'] = TextResultCategoryModel.objects.filter(
                type=self.request.user.profile.type).order_by('name')
        else:
            context['class_list'] = ClassesModel.objects.filter(Q(result_type='text') | Q(result_type='mix')).order_by(
                'name')
            context['class_section_list'] = ClassSectionModel.objects.all().order_by('name')
            context['text_result_category_list'] = TextResultCategoryModel.objects.all().order_by('name')
        return context

    def get_form_kwargs(self):
        kwargs = super(TextResultCategoryCreateView, self).get_form_kwargs()
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            kwargs.update({'type': self.request.user.profile.type})
        return kwargs


class TextResultCategoryListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = TextResultCategoryModel
    permission_required = 'result.view_resultfieldmodel'
    fields = '__all__'
    template_name = 'result/text_result_category/index.html'
    context_object_name = "text_result_category_list"

    def get_queryset(self):
        sch_setting = SchoolGeneralInfoModel.objects.first()
        if sch_setting.separate_school_section:
            academic_setting = SchoolAcademicInfoModel.objects.filter(type=self.request.user.profile.type).first()
        else:
            academic_setting = SchoolAcademicInfoModel.objects.first()
        session = academic_setting.session
        term = academic_setting.term

        if sch_setting.separate_school_section:
            return TextResultCategoryModel.objects.filter(term=term, session=session,
                                                          type=self.request.user.profile.type).order_by('name')
        else:
            return TextResultCategoryModel.objects.filter(term=term, session=session).order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        form_kwargs = {}
        if school_setting.separate_school_section:
            context['class_section_list'] = ClassSectionModel.objects.filter(
                type=self.request.user.profile.type).order_by('name')
            context['class_list'] = ClassesModel.objects.filter(Q(result_type='text') | Q(result_type='mix'),
                                                                type=self.request.user.profile.type).order_by('name')
            context['staff_list'] = StaffModel.objects.filter(type=self.request.user.profile.type,
                                                              can_teach=True).order_by('surname')
            form_kwargs['type'] = self.request.user.profile.type
        else:
            context['class_section_list'] = ClassSectionModel.objects.all().order_by('name')
            context['class_list'] = ClassesModel.objects.filter(
                Q(result_type='text') | Q(result_type='mix'), ).order_by('name')
            context['staff_list'] = StaffModel.objects.filter(can_teach=True).order_by('surname')

        context['form'] = TextResultCategoryForm(**form_kwargs)

        return context


class TextResultCategoryUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = TextResultCategoryModel
    permission_required = 'result.change_resultfieldmodel'
    form_class = TextResultCategoryEditForm
    success_message = 'Text Based Result Category Updated Successfully'
    template_name = 'result/text_result_category/index.html'

    def get_success_url(self):
        return reverse('text_result_category_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        form_kwargs = {}
        if school_setting.separate_school_section:
            context['class_section_list'] = ClassSectionModel.objects.filter(
                type=self.request.user.profile.type).order_by('name')
            context['class_list'] = ClassesModel.objects.filter(Q(result_type='text') | Q(result_type='mix'),
                                                                type=self.request.user.profile.type).order_by('name')
            context['text_result_category_list'] = TextResultCategoryModel.objects.filter(
                type=self.request.user.profile.type).order_by('name')
            form_kwargs['type'] = self.request.user.profile.type
        else:
            context['class_section_list'] = ClassSectionModel.objects.all().order_by('name')
            context['class_list'] = ClassesModel.objects.filter(
                Q(result_type='text') | Q(result_type='mix'), ).order_by('name')
            context['text_result_category_list'] = TextResultCategoryModel.objects.all().order_by('name')
        context['form'] = TextResultCategoryEditForm(**form_kwargs)
        return context


class TextResultCategoryTeacherView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = TextResultCategoryModel
    permission_required = 'result.change_resultfieldmodel'
    form_class = TextResultCategoryTeacherForm
    success_message = 'Text Based Result Category Teachers Updated Successfully'
    template_name = 'result/text_result_category/index.html'

    def get_success_url(self):
        return reverse('text_result_category_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        form_kwargs = {}
        if school_setting.separate_school_section:
            context['staff_list'] = StaffModel.objects.filter(type=self.request.user.profile.type,
                                                              can_teach=True).order_by('name')
            context['text_result_category_list'] = TextResultCategoryModel.objects.filter(
                type=self.request.user.profile.type).order_by('name')
            form_kwargs['type'] = self.request.user.profile.type
        else:
            context['staff_list'] = StaffModel.objects.filter(type=self.request.user.profile.type,
                                                              can_teach=True).order_by('name')
            context['text_result_category_list'] = TextResultCategoryModel.objects.all().order_by('name')
        context['form'] = TextResultCategoryTeacherForm(**form_kwargs)
        return context


class TextResultCategoryDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = TextResultCategoryModel
    permission_required = 'result.delete_resultfieldmodel'
    success_message = 'Text Based Result Category Deleted Successfully'
    fields = '__all__'
    template_name = 'result/text_result_category/delete.html'
    context_object_name = "text_result_category"

    def get_success_url(self):
        return reverse("text_result_category_index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class TextResultCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = TextResultModel
    permission_required = 'result.add_resultfieldmodel'
    form_class = TextResultForm
    success_message = 'Text Based Result Field Added Successfully'
    template_name = 'result/text_result/index.html'

    def get_success_url(self):
        return reverse('text_result_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            context['class_list'] = ClassesModel.objects.filter(type=self.request.user.profile.type,
                                                                result_type='text').order_by('name')
            context['class_section_list'] = ClassSectionModel.objects.filter(
                type=self.request.user.profile.type).order_by('name')
            context['text_result_list'] = TextResultModel.objects.filter(
                type=self.request.user.profile.type).order_by('name')
        else:
            context['class_list'] = ClassesModel.objects.filter(result_type='text').order_by('name')
            context['class_section_list'] = ClassSectionModel.objects.all().order_by('name')
            context['text_result_list'] = TextResultModel.objects.all().order_by('name')
        return context

    def get_form_kwargs(self):
        kwargs = super(TextResultCreateView, self).get_form_kwargs()
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            kwargs.update({'type': self.request.user.profile.type})
        return kwargs


class TextResultListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = TextResultModel
    permission_required = 'result.view_resultfieldmodel'
    fields = '__all__'
    template_name = 'result/text_result/index.html'
    context_object_name = "text_result_list"

    def get_queryset(self):
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            academic_setting = SchoolAcademicInfoModel.objects.filter(type=self.request.user.profile.type).first()
        else:
            academic_setting = SchoolAcademicInfoModel.objects.first()
        session = academic_setting.session
        term = academic_setting.term
        if school_setting.separate_school_section:
            return TextResultModel.objects.filter(type=self.request.user.profile.type, category__session=session,
                                                  category__term=term).order_by('name')
        else:
            return TextResultModel.objects.filter(category__session=session, category__term=term).order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            academic_setting = SchoolAcademicInfoModel.objects.filter(type=self.request.user.profile.type).first()
        else:
            academic_setting = SchoolAcademicInfoModel.objects.first()
        session = academic_setting.session
        term = academic_setting.term
        form_kwargs = {}
        if school_setting.separate_school_section:
            context['class_section_list'] = ClassSectionModel.objects.filter(
                type=self.request.user.profile.type).order_by('name')
            context['class_list'] = ClassesModel.objects.filter(Q(result_type='text') | Q(result_type='mix'),
                                                                type=self.request.user.profile.type).order_by('name')
            context['result_category_list'] = TextResultCategoryModel.objects.filter(
                type=self.request.user.profile.type, term=term, session=session).order_by('name')
            form_kwargs['type'] = self.request.user.profile.type
        else:
            context['class_section_list'] = ClassSectionModel.objects.all().order_by('name')
            context['class_list'] = ClassesModel.objects.filter(Q(result_type='text') | Q(result_type='mix')).order_by(
                'name')
            context['result_category_list'] = TextResultCategoryModel.objects.filter(term=term,
                                                                                     session=session).order_by('name')
        context['form'] = TextResultForm(**form_kwargs)

        return context


class TextResultUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = TextResultModel
    permission_required = 'result.change_resultfieldmodel'
    form_class = TextResultCategoryEditForm
    success_message = 'Text Based Result Field Updated Successfully'
    template_name = 'result/text_result/index.html'

    def get_success_url(self):
        return reverse('text_result_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        form_kwargs = {}
        if school_setting.separate_school_section:
            context['class_section_list'] = ClassSectionModel.objects.filter(
                type=self.request.user.profile.type).order_by('name')
            context['class_list'] = ClassesModel.objects.filter(type=self.request.user.profile.type,
                                                                result_type='text').order_by('name')
            context['text_result_list'] = TextResultModel.objects.filter(
                type=self.request.user.profile.type).order_by('name')
            form_kwargs['type'] = self.request.user.profile.type
        else:
            context['class_section_list'] = ClassSectionModel.objects.all().order_by('name')
            context['class_list'] = ClassesModel.objects.filter(result_type='text').order_by('name')
            context['text_result_list'] = TextResultModel.objects.all().order_by('name')
        context['form'] = TextResultEditForm(**form_kwargs)
        return context


class TextResultDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = TextResultModel
    permission_required = 'result.delete_resultfieldmodel'
    success_message = 'Text Based Result Field Deleted Successfully'
    fields = '__all__'
    template_name = 'result/text_result/delete.html'
    context_object_name = "text_result"

    def get_success_url(self):
        return reverse("text_result_index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class TeacherResultCommentCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = TeacherResultCommentModel
    form_class = TeacherResultCommentForm
    success_message = 'Teacher Result Comment Added Successfully'
    template_name = 'result/teacher_comment/index.html'

    def get_success_url(self):
        return reverse('teacher_comment_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            context['class_list'] = ClassSectionInfoModel.objects.filter(type=self.request.user.profile.type).order_by(
                'student_class__name')
            context['result_comment_list'] = TeacherResultCommentModel.objects.filter(
                type=self.request.user.profile.type)
        else:
            context['class_list'] = ClassSectionInfoModel.objects.all().order_by('student_class__name')
            context['result_comment_list'] = TeacherResultCommentModel.objects.all()
        return context

    def get_form_kwargs(self):
        kwargs = super(TeacherResultCommentCreateView, self).get_form_kwargs()
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            kwargs.update({'type': self.request.user.profile.type, 'teacher': self.request.user.profile.staff})
        else:
            kwargs.update({'teacher': self.request.user.profile.staff})
        return kwargs


class TeacherResultCommentListView(LoginRequiredMixin, ListView):
    model = TeacherResultCommentModel

    fields = '__all__'
    template_name = 'result/teacher_comment/index.html'
    context_object_name = "result_comment_list"

    def get_queryset(self):
        if not self.request.user.is_superuser:
            teacher = [self.request.user.profile.staff]
            return TeacherResultCommentModel.objects.filter(
                Q(student_class__form_teacher__in=teacher) | Q(student_class__assistant_form_teacher__in=teacher))
        else:
            school_setting = SchoolGeneralInfoModel.objects.first()
            if school_setting.separate_school_section:
                return TeacherResultCommentModel.objects.filter()
            else:
                return TeacherResultCommentModel.objects.filter()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        form_kwargs = {}
        if school_setting.separate_school_section:
            context['class_list'] = ClassSectionInfoModel.objects.filter(type=self.request.user.profile.type).order_by(
                'student_class__name')
            form_kwargs['type'] = self.request.user.profile.type
        else:
            context['class_list'] = ClassSectionInfoModel.objects.all().order_by('student_class__name')
        form_kwargs['teacher'] = self.request.user.profile.staff
        context['form'] = TeacherResultCommentForm(**form_kwargs)

        return context


class TeacherResultCommentUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = TeacherResultCommentModel

    form_class = TeacherResultCommentEditForm
    success_message = 'Teacher Result Comment Updated Successfully'
    template_name = 'result/teacher_comment/index.html'

    def get_success_url(self):
        return reverse('teacher_comment_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            context['class_list'] = ClassSectionInfoModel.objects.filter(type=self.request.user.profile.type).order_by(
                'student_class__name')
            context['result_comment_list'] = TeacherResultCommentModel.objects.filter(
                type=self.request.user.profile.type)

        else:
            context['class_list'] = ClassSectionInfoModel.objects.all().order_by(
                'student_class__name')
            context['result_comment_list'] = TeacherResultCommentModel.objects.all()

        return context

    def get_form_kwargs(self):
        kwargs = super(TeacherResultCommentUpdateView, self).get_form_kwargs()
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            kwargs.update({'type': self.request.user.profile.type, 'teacher': self.request.user.profile.staff})
        else:
            kwargs.update({'teacher': self.request.user.profile.staff})
        return kwargs


class TeacherResultCommentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = TeacherResultCommentModel
    permission_required = 'result.delete_resultgrademodel'
    success_message = 'Teacher Result Comment Deleted Successfully'
    fields = '__all__'
    template_name = 'result/teacher_comment/delete.html'
    context_object_name = "result_comment"

    def get_success_url(self):
        return reverse("teacher_comment_index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class HeadTeacherResultCommentCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = HeadTeacherResultCommentModel
    form_class = HeadTeacherResultCommentForm
    success_message = 'Head Teacher Result Comment Added Successfully'
    template_name = 'result/head_teacher_comment/index.html'

    def get_success_url(self):
        return reverse('head_teacher_comment_index')

    def dispatch(self, *args, **kwargs):
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            academic_setting = AcademicSettingModel.objects.filter(type=self.request.user.profile.type).first()
        else:
            academic_setting = AcademicSettingModel.objects.filter().first()
        if not academic_setting.head_teacher == self.request.user.profile.staff:
            messages.error(self.request, 'ONLY HEAD TEACHER CAN CREATE THIS RESULT COMMENT')
            if self.request.user.is_superuser:
                return redirect(reverse('head_teacher_comment_index'))
            return redirect(reverse('admin_dashboard'))

        return super(HeadTeacherResultCommentCreateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            context['class_list'] = ClassSectionInfoModel.objects.filter(type=self.request.user.profile.type).order_by(
                'student_class__name')
            context['result_comment_list'] = HeadTeacherResultCommentModel.objects.filter(
                type=self.request.user.profile.type)
        else:
            context['class_list'] = ClassSectionInfoModel.objects.all().order_by('student_class__name')
            context['result_comment_list'] = HeadTeacherResultCommentModel.objects.all()
        return context

    def get_form_kwargs(self):
        kwargs = super(HeadTeacherResultCommentCreateView, self).get_form_kwargs()
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            kwargs.update({'type': self.request.user.profile.type})
        kwargs.update({'type': self.request.user.profile.type})
        return kwargs


class HeadTeacherResultCommentListView(LoginRequiredMixin, ListView):
    model = HeadTeacherResultCommentModel
    fields = '__all__'
    template_name = 'result/head_teacher_comment/index.html'
    context_object_name = "result_comment_list"

    def get_queryset(self):
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            return HeadTeacherResultCommentModel.objects.filter(type=self.request.user.profile.type)
        else:
            return HeadTeacherResultCommentModel.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        form_kwargs = {}
        if school_setting.separate_school_section:
            context['class_section_list'] = ClassSectionModel.objects.filter(
                type=self.request.user.profile.type).order_by('name')
            context['class_list'] = ClassesModel.objects.filter(type=self.request.user.profile.type).order_by('name')
            form_kwargs['type'] = self.request.user.profile.type
        else:
            context['class_section_list'] = ClassSectionModel.objects.all().order_by('name')
            context['class_list'] = ClassesModel.objects.filter().order_by('name')
        context['form'] = HeadTeacherResultCommentForm(**form_kwargs)
        return context

    def dispatch(self, *args, **kwargs):
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            academic_setting = AcademicSettingModel.objects.filter(type=self.request.user.profile.type).first()
        else:
            academic_setting = AcademicSettingModel.objects.filter().first()
        if not academic_setting.head_teacher == self.request.user.profile.staff and not self.request.user.is_superuser:
            messages.error(self.request, 'ONLY HEAD TEACHER CAN VIEW THESE RESULT COMMENTS')
            return redirect(reverse('admin_dashboard'))
        return super(HeadTeacherResultCommentListView, self).dispatch(*args, **kwargs)


class HeadTeacherResultCommentUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = HeadTeacherResultCommentModel
    form_class = HeadTeacherResultCommentEditForm
    success_message = 'Head Teacher Result Comment Updated Successfully'
    template_name = 'result/head_teacher_comment/index.html'

    def get_success_url(self):
        return reverse('head_teacher_comment_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        form_kwargs = {}
        if school_setting.separate_school_section:
            context['class_list'] = ClassSectionInfoModel.objects.filter(type=self.request.user.profile.type).order_by(
                'student_class__name')
            context['result_comment_list'] = HeadTeacherResultCommentModel.objects.filter(
                type=self.request.user.profile.type)
            form_kwargs['type'] = self.request.user.profile.type
        else:
            context['class_list'] = ClassSectionInfoModel.objects.all().order_by('student_class__name')
            context['result_comment_list'] = HeadTeacherResultCommentModel.objects.all()
        context['form'] = HeadTeacherResultCommentEditForm(**form_kwargs)
        return context

    def dispatch(self, *args, **kwargs):
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            academic_setting = AcademicSettingModel.objects.filter(type=self.request.user.profile.type).first()
        else:
            academic_setting = AcademicSettingModel.objects.filter().first()
        if not academic_setting.head_teacher == self.request.user.profile.staff:
            messages.error(self.request, 'ONLY HEAD TEACHER CAN EDIT THIS RESULT COMMENT')
            if self.request.user.is_superuser:
                return redirect(reverse('head_teacher_comment_index'))
            return redirect(reverse('admin_dashboard'))

        return super(HeadTeacherResultCommentUpdateView, self).dispatch(*args, **kwargs)


class HeadTeacherResultCommentDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = HeadTeacherResultCommentModel
    success_message = 'Head Teacher Result Comment Deleted Successfully'
    fields = '__all__'
    template_name = 'result/head_teacher_comment/delete.html'
    context_object_name = "result_comment"

    def get_success_url(self):
        return reverse("head_teacher_comment_index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def dispatch(self, *args, **kwargs):
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            academic_setting = AcademicSettingModel.objects.filter(type=self.request.user.profile.type).first()
        else:
            academic_setting = AcademicSettingModel.objects.filter().first()
        if not academic_setting.head_teacher == self.request.user.profile.staff and not self.request.user.is_superuser:
            messages.error(self.request, 'ONLY HEAD TEACHER CAN DELETE THIS RESULT COMMENT')
            return redirect(reverse('admin_dashboard'))

        return super(HeadTeacherResultCommentDeleteView, self).dispatch(*args, **kwargs)


class ResultSettingView(LoginRequiredMixin, TemplateView):
    template_name = 'result/setting/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        form_kwargs = {}
        if school_setting.separate_school_section:
            result_info = ResultSettingModel.objects.filter(type=self.request.user.profile.type).first()
            form_kwargs['type'] = self.request.user.profile.type
        else:
            result_info = ResultSettingModel.objects.first()

        if not result_info:
            form = ResultSettingCreateForm(**form_kwargs)
            is_result_info = False
        else:
            form = ResultSettingEditForm(instance=result_info, **form_kwargs)
            is_result_info = True
        context['form'] = form
        context['is_result_info'] = is_result_info
        context['result_info'] = result_info
        return context


class ResultSettingCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = ResultSettingModel
    form_class = ResultSettingCreateForm
    template_name = 'result/setting/index.html'
    success_message = 'Result Setting Info updated Successfully'

    def get_success_url(self):
        return reverse('result_info')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            pass
        else:
            pass
        return context

    def get_form_kwargs(self):
        kwargs = super(ResultSettingCreateView, self).get_form_kwargs()
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            kwargs.update({'type': self.request.user.profile.type})
        kwargs.update({'type': self.request.user.profile.type})
        return kwargs


class ResultSettingUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = ResultSettingModel
    form_class = ResultSettingEditForm
    template_name = 'result/setting/index.html'
    success_message = 'Result Setting Info updated Successfully'

    def get_success_url(self):
        return reverse('result_info')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            pass
        else:
            pass
        return context

    def get_form_kwargs(self):
        kwargs = super(ResultSettingUpdateView, self).get_form_kwargs()
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            kwargs.update({'type': self.request.user.profile.type})
        kwargs.update({'type': self.request.user.profile.type})
        return kwargs

