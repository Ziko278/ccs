import io

from django.contrib.messages.views import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.urls import resolve
from django.core import serializers
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from xlsxwriter import Workbook

from admin_dashboard.utility import state_list
from school_setting.models import *
from django.apps import apps
from student.models import *
from student.forms import *


@login_required
def disable_student_view(request, pk):
    if request.method == 'POST':
        student = StudentsModel.objects.get(pk=pk)
        student.status = 'disabled'
        student.student_class = None
        student.class_section = None
        student.save()

        student_record = StudentAcademicRecordModel.objects.filter(student=student).first()
        if student_record:
            sch_setting = SchoolGeneralInfoModel.objects.first()
            if sch_setting.separate_school_section:
                academic_setting = SchoolAcademicInfoModel.objects.filter(type=request.user.profile.type).first()
            else:
                academic_setting = SchoolAcademicInfoModel.objects.first()
            session = academic_setting.session
            term = academic_setting.term
            student_record.exit_mode = 'departure'
            student_record.session_of_departure = session
            student_record.term_of_departure = term
            student_record.save()

        messages.success(request, 'Student {} successfully disabled'.format(student.__str__()))

    return redirect(reverse('student_detail', kwargs={'pk': pk}))


class ParentCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = ParentsModel
    permission_required = 'student.add_parentsmodel'
    form_class = ParentForm
    template_name = 'student/parent/create.html'
    success_message = 'Parent Registration Successful'

    def get_success_url(self):
        if 'student-registration' in self.request.path:
            return reverse('student_create', kwargs={'parent_pk': self.object.pk})
        return reverse('parent_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            context['parent_setting'] = StudentSettingModel.objects.filter(type=self.request.user.profile.type).first()
        else:
            context['parent_setting'] = StudentSettingModel.objects.filter().first()
        context['state_list'] = state_list
        return context


class ParentListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = ParentsModel
    permission_required = 'student.view_parentsmodel'
    fields = '__all__'
    template_name = 'student/parent/index.html'
    context_object_name = "parent_list"

    def get_queryset(self):
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            return ParentsModel.objects.filter(type=self.request.user.profile.type).order_by('surname')
        else:
            return ParentsModel.objects.all().order_by('surname')


class ParentDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = ParentsModel
    permission_required = 'student.view_parentsmodel'
    fields = '__all__'
    template_name = 'student/parent/detail.html'
    context_object_name = "parent"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        parent = self.object
        student_list = StudentsModel.objects.filter(parent=parent)
        context['student_list'] = student_list
        return context


class ParentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = ParentsModel
    permission_required = 'student.change_parentsmodel'
    form_class = ParentEditForm
    template_name = 'student/parent/edit.html'
    success_message = 'Parent Information Successfully Updated'

    def get_success_url(self):
        return reverse('parent_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parent'] = self.object
        context['state_list'] = state_list
        return context


class ParentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = ParentsModel
    permission_required = 'student.delete_parentsmodel'
    fields = '__all__'
    template_name = 'student/parent/delete.html'
    success_message = 'Parent Successfully Deleted'
    context_object_name = "parent"

    def get_success_url(self):
        return reverse('parent_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class StudentCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = StudentsModel
    permission_required = 'student.add_studentsmodel'
    form_class = StudentForm
    template_name = 'student/student/create.html'
    success_message = 'Student Successfully Registered'

    def get_success_url(self):
        return reverse('student_detail', kwargs={'pk': self.object.pk})

    def get_form_kwargs(self):
        kwargs = super(StudentCreateView, self).get_form_kwargs()
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            kwargs.update({'type': self.request.user.profile.type})
        kwargs.update({'type': self.request.user.profile.type})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        parent_pk = self.kwargs.get('parent_pk')
        student_parent = ParentsModel.objects.get(pk=parent_pk)
        context['student_parent'] = student_parent
        context['state_list'] = state_list
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            context['class_list'] = ClassesModel.objects.filter(type=self.request.user.profile.type).order_by('name')
            context['student_setting'] = StudentSettingModel.objects.filter(
                type=self.request.user.profile.type).first()
        else:
            context['student_setting'] = StudentSettingModel.objects.filter().first()
            context['class_list'] = ClassesModel.objects.all().order_by('name')

        return context


class StudentListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = StudentsModel
    permission_required = 'student.view_studentsmodel'
    fields = '__all__'
    template_name = 'student/student/index.html'
    context_object_name = "student_list"

    def get_queryset(self):
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            return StudentsModel.objects.filter(type=self.request.user.profile.type).exclude(
                status='graduated').order_by('surname')
        else:
            return StudentsModel.objects.filter().exclude(status='graduated').order_by('surname')


def class_student_list_view(request):
    if 'student_class' in request.GET and 'class_section' in request.GET:
        student_class = request.GET.get('student_class')
        class_section = request.GET.get('class_section')
        student_list = StudentsModel.objects.filter(student_class__id=student_class, class_section__id=class_section).order_by('surname')
        context = {
            'student_list': student_list,
            'student_class': ClassesModel.objects.get(pk=student_class),
            'class_section': ClassSectionModel.objects.get(pk=class_section),
            'is_class': True
        }
        return render(request, 'student/student/index.html', context)

    school_setting = SchoolGeneralInfoModel.objects.first()
    if school_setting.separate_school_section:
        class_list = ClassesModel.objects.filter(type=request.user.profile.type).order_by('name')

    else:
        class_list = ClassesModel.objects.all().order_by('name')
    context = {
        'class_list': class_list,
    }
    return render(request, 'student/student/select_class.html', context)


class StudentAlumniListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = StudentsModel
    permission_required = 'student.view_studentsmodel'
    fields = '__all__'
    template_name = 'student/student/alumni.html'
    context_object_name = "student_list"

    def get_queryset(self):
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            return StudentsModel.objects.filter(type=self.request.user.profile.type).filter(
                status='graduated').order_by('surname')
        else:
            return StudentsModel.objects.filter().filter(status='graduated').order_by('surname')


class StudentDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = StudentsModel
    permission_required = 'student.view_studentsmodel'
    fields = '__all__'
    template_name = 'student/student/detail.html'
    context_object_name = "student"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ResultModel = apps.get_model('result', 'ResultModel')
        TextBasedResultModel = apps.get_model('result', 'TextBasedResultModel')
        session_list = ResultModel.objects.filter(student=self.object)
        session_list_2 = TextBasedResultModel.objects.filter(student=self.object)

        student_session_list = []
        for session_result in session_list:
            if session_result.session not in student_session_list:
                student_session_list.append(session_result.session)

        for session_result in session_list_2:
            if session_result.session not in student_session_list:
                student_session_list.append(session_result.session)
        context['student_session_list'] = student_session_list
        student = self.object
        student_class = student.student_class
        class_section = student.class_section
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            academic_setting = SchoolAcademicInfoModel.objects.filter(type=self.request.user.profile.type).first()
        else:
            academic_setting = SchoolAcademicInfoModel.objects.first()

        context['academic_setting'] = academic_setting
        context['student'] = student

        return context


class StudentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = StudentsModel
    permission_required = 'student.change_studentsmodel'
    form_class = StudentEditForm
    template_name = 'student/student/edit.html'
    success_message = 'Student Information Successfully Updated'

    def get_success_url(self):
        return reverse('student_detail', kwargs={'pk': self.object.pk})

    def dispatch(self, *args, **kwargs):
        return super(StudentUpdateView, self).dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(StudentUpdateView, self).get_form_kwargs()
        # kwargs.update({'division': self.request.session['division']})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['student_parent'] = self.object.parent
        context['student'] = self.object
        context['state_list'] = state_list
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            context['student_setting'] = StudentSettingModel.objects.filter(
                type=self.request.user.profile.type).first()
            context['class_list'] = ClassesModel.objects.filter(type=self.request.user.profile.type).order_by('name')
        else:
            context['student_setting'] = StudentSettingModel.objects.filter().first()
            context['class_list'] = ClassesModel.objects.all().order_by('name')
        return context


class StudentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = StudentsModel
    permission_required = 'student.delete_studentsmodel'
    fields = '__all__'
    template_name = 'student/student/delete.html'
    context_object_name = "student"
    success_message = 'Student Successfully Deleted'

    def get_success_url(self):
        return reverse('student_index')


@login_required
def student_check_parent_view(request):
    school_setting = SchoolGeneralInfoModel.objects.first()
    if school_setting.separate_school_section:
        parent_list = ParentsModel.objects.filter(type=request.user.profile.type)
    else:
        parent_list = ParentsModel.objects.filter()
    parent_list = serializers.serialize("json", parent_list)

    context = {
        'parent_list': parent_list,
    }
    return render(request, 'student/student/check_parent.html', context=context)


@login_required
def student_login_detail_view(request):
    if request.method == 'GET':
        student_class = request.GET.get('student_class')
        class_section = request.GET.get('class_section')
        student_list = StudentsModel.objects.filter(student_class__id=student_class,
                                                    class_section__id=class_section).order_by('surname')
        context = {
            'student_list': student_list,
            'student_class': ClassesModel.objects.get(pk=student_class),
            'class_section': ClassSectionModel.objects.get(pk=class_section),
        }

        return render(request, 'student/student/login_detail.html', context)
    else:
        student_class = ClassesModel.objects.get(id=request.POST.get('student_class'))
        class_section = ClassSectionModel.objects.get(id=request.POST.get('class_section'))

        student_list = StudentsModel.objects.filter(student_class=student_class,
                                                    class_section=class_section).order_by('surname')

        field_list = ['student', 'username', 'password']
        file_name = f"{student_class.__str__()} {class_section.__str__()}-STUDENT-LOGIN-DETAILS"
        if not student_list:
            messages.warning(request, 'No Student Selected')
            return redirect(reverse('student_class_index'))

        output = io.BytesIO()

        workbook = Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()

        for num in range(len(field_list)):
            field = field_list[num]
            worksheet.write(0, num, field.title())

        for row in range(len(student_list)):
            student = student_list[row]

            for col in range(len(field_list)):
                field = field_list[col]
                if field == 'student':
                    value = student.__str__()
                elif field == 'username':
                    value = student.registration_number
                elif field == 'password':
                    try:
                        value = UserProfileModel.objects.get(student=student).default_password
                    except Exception:
                        value = ''
                else:
                    value = ''
                worksheet.write(row + 1, col, value)
        workbook.close()

        output.seek(0)

        response = HttpResponse(output.read(),
                                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = "attachment; filename=" + file_name + ".xlsx"

        output.close()

        return response


class StudentSettingView(LoginRequiredMixin, TemplateView):
    template_name = 'student/setting/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        form_kwargs = {}
        if school_setting.separate_school_section:
            student_info = StudentSettingModel.objects.filter(type=self.request.user.profile.type).first()
            form_kwargs['type'] = self.request.user.profile.type
        else:
            student_info = StudentSettingModel.objects.first()

        if not student_info:
            form = StudentSettingCreateForm(**form_kwargs)
            is_student_info = False
        else:
            form = StudentSettingEditForm(instance=student_info, **form_kwargs)
            is_student_info = True
        context['form'] = form
        context['is_student_info'] = is_student_info
        context['student_info'] = student_info
        return context


class StudentSettingCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = StudentSettingModel
    form_class = StudentSettingCreateForm
    template_name = 'student/setting/index.html'
    success_message = 'Admission Settings updated Successfully'

    def get_success_url(self):
        return reverse('student_info')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()

        return context

    def get_form_kwargs(self):
        kwargs = super(StudentSettingCreateView, self).get_form_kwargs()
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            kwargs.update({'type': self.request.user.profile.type})
        kwargs.update({'type': self.request.user.profile.type})
        return kwargs


class StudentSettingUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = StudentSettingModel
    form_class = StudentSettingEditForm
    template_name = 'student/setting/index.html'
    success_message = 'Admission Setting updated Successfully'

    def get_success_url(self):
        return reverse('student_info')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

    def get_form_kwargs(self):
        kwargs = super(StudentSettingUpdateView, self).get_form_kwargs()
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            kwargs.update({'type': self.request.user.profile.type})
        kwargs.update({'type': self.request.user.profile.type})
        return kwargs
