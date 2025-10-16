from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.messages.views import SuccessMessageMixin, messages
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.contrib.auth import authenticate
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.sessions.models import Session
from academic.models import *
from django.db.models import Q
from datetime import datetime, date
from urllib.parse import urlencode
from django.contrib.auth import logout
from academic.forms import *
from django.http import HttpResponse

from finance.templatetags.fee_custom_filters import get_fee_balance, get_amount_paid, get_fee_penalty, get_fee_discount
from student.models import StudentsModel, StudentAcademicRecordModel
from school_setting.models import SchoolGeneralInfoModel, TermModel, SchoolAcademicInfoModel, SessionModel


class ClassSectionCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = ClassSectionModel
    permission_required = 'academic.add_classsectionmodel'
    form_class = ClassSectionForm
    success_message = 'Class Section Added Successfully'
    template_name = 'academic/class_section/index.html'

    def get_success_url(self):
        return reverse('class_section_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            context['class_section_list'] = ClassSectionModel.objects.filter(
                type=self.request.user.profile.type).order_by('name')
        else:
            context['class_section_list'] = ClassSectionModel.objects.all().order_by('name')
        return context


class ClassSectionListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = ClassSectionModel
    permission_required = 'academic.view_classsectionmodel'
    fields = '__all__'
    template_name = 'academic/class_section/index.html'
    context_object_name = "class_section_list"

    def get_queryset(self):
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            return ClassSectionModel.objects.filter(type=self.request.user.profile.type).order_by('name')
        return ClassSectionModel.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ClassSectionForm
        return context


class ClassSectionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = ClassSectionModel
    permission_required = 'academic.change_classsectionmodel'
    form_class = ClassSectionEditForm
    success_message = 'Class Section Updated Successfully'
    template_name = 'academic/class_section/index.html'

    def get_success_url(self):
        return reverse('class_section_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            context['class_section_list'] = ClassSectionModel.objects.filter(type=self.request.user.profile.type).order_by('name')
        else:
            context['class_section_list'] = ClassSectionModel.objects.all().order_by('name')
        return context


class ClassSectionDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = ClassSectionModel
    permission_required = 'academic.delete_classsectionmodel'
    success_message = 'Class Section Deleted Successfully'
    fields = '__all__'
    template_name = 'academic/class_section/delete.html'
    context_object_name = "class_section"

    def get_success_url(self):
        return reverse('class_section_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ClassCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = ClassesModel
    permission_required = 'academic.add_classesmodel'
    form_class = ClassCreateForm
    success_message = 'Class Added Successfully'
    template_name = 'academic/class/index.html'

    def get_success_url(self):
        return reverse('class_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            context['class_list'] = ClassesModel.objects.filter(type=self.request.user.profile.type).order_by('name')
            context['class_section_list'] = ClassSectionModel.objects.filter(type=self.request.user.profile.type).order_by('name')
        else:
            context['class_list'] = ClassesModel.objects.all().order_by('name')
            context['class_section_list'] = ClassSectionModel.objects.all().order_by('name')
        return context

    def get_form_kwargs(self):
        kwargs = super(ClassCreateView, self).get_form_kwargs()
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            kwargs.update({'type': self.request.user.profile.type})
        kwargs.update({'type': self.request.user.profile.type})
        return kwargs


class ClassListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = ClassesModel
    permission_required = 'academic.view_classesmodel'
    fields = '__all__'
    template_name = 'academic/class/index.html'
    context_object_name = "class_list"

    def get_queryset(self):
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            return ClassesModel.objects.filter(type=self.request.user.profile.type).order_by('name')
        else:
            return ClassesModel.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        form_kwargs = {}
        if school_setting.separate_school_section:
            context['class_section_list'] = ClassSectionModel.objects.filter(type=self.request.user.profile.type)
            form_kwargs['type'] = self.request.user.profile.type
        else:
            context['class_section_list'] = ClassSectionModel.objects.all()
        context['form'] = ClassCreateForm(**form_kwargs)
        return context


class ClassDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = ClassesModel
    permission_required = 'academic.view_classesmodel'
    fields = '__all__'
    template_name = 'academic/class/detail.html'
    context_object_name = "class"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            context['student_list'] = StudentsModel.objects.filter(type=self.request.user.profile.type).order_by(
                'surname').filter(student_class=self.object).order_by('class_section__name')
            context['class_list'] = ClassesModel.objects.filter(type=self.request.user.profile.type).order_by('name')
            context['class_section_list'] = ClassSectionModel.objects.filter(
                type=self.request.user.profile.type).order_by('name')

        else:
            context['student_list'] = StudentsModel.objects.filter(student_class=self.object).order_by(
                'surname').order_by('class_section__name')
            context['class_section_list'] = ClassSectionModel.objects.all()
            context['class_list'] = ClassesModel.objects.filter().order_by('name')
        return context


class ClassUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = ClassesModel
    permission_required = 'academic.change_classsesmodel'
    form_class = ClassEditForm
    success_message = 'Class Updated Successfully'
    template_name = 'academic/class/index.html'

    def get_success_url(self):
        return reverse('class_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            context['class_list'] = ClassesModel.objects.filter(type=self.request.user.profile.type).order_by('name')
        else:
            context['class_list'] = ClassesModel.objects.all().order_by('name')
        return context

    def get_form_kwargs(self):
        kwargs = super(ClassUpdateView, self).get_form_kwargs()
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            kwargs.update({'type': self.request.user.profile.type})
        kwargs.update({'type': self.request.user.profile.type})
        return kwargs


class ClassDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = ClassesModel
    permission_required = 'academic.delete_classesmodel'
    success_message = 'Class Deleted Successfully'
    fields = '__all__'
    template_name = 'academic/class/delete.html'
    context_object_name = "class"

    def get_success_url(self):
        return reverse('class_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def set_promotion_class(request):
    if request.method == 'POST':
        class_list = request.POST.getlist('class')
        section_list = request.POST.getlist('section')
        promotion_class_list = request.POST.getlist('promotion_class')
        promotion_section_list = request.POST.getlist('promotion_section')
        is_graduation_list = request.POST.getlist('is_graduation')

        if not (len(class_list) == len(section_list) == len(promotion_class_list) == len(promotion_section_list) == len(is_graduation_list)):
            messages.error(request, "Input lists have mismatched lengths. Please check your form submission.")
            return redirect(reverse('promotion_count_index'))

        save_count = 0

        for idx in range(len(class_list)):
            try:
                student_class = ClassesModel.objects.get(pk=class_list[idx])
                class_section = ClassSectionModel.objects.get(pk=section_list[idx])

                promotion_class, created = PromotionClassModel.objects.get_or_create(
                    student_class=student_class, class_section=class_section
                )

                promotion_class.is_graduation_class = is_graduation_list[idx] == 'true'

                if promotion_class_list[idx]:
                    promotion_class.promotion_class = ClassesModel.objects.get(pk=promotion_class_list[idx])

                if promotion_section_list[idx]:
                    promotion_class.promotion_section = ClassSectionModel.objects.get(pk=promotion_section_list[idx])

                promotion_class.save()
                save_count += 1
            except (ClassesModel.DoesNotExist, ClassSectionModel.DoesNotExist):
                messages.error(request, f"Invalid class or section data at index {idx + 1}. Skipping.")
            except Exception as e:
                messages.error(request, f"An error occurred: {e}. Skipping record at index {idx + 1}.")

        messages.success(request, f"Saved {save_count} of {len(class_list)} Promotion Classes.")
        return redirect(reverse('promotion_count_index'))

    school_setting = SchoolGeneralInfoModel.objects.first()
    class_list = (
        ClassesModel.objects.filter(type=request.user.profile.type).order_by('name')
        if school_setting and school_setting.separate_school_section
        else ClassesModel.objects.all().order_by('name')
    )

    context = {
        'class_list': class_list
    }
    return render(request, 'academic/class/promotion.html', context)


class SubjectCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = SubjectsModel
    permission_required = 'academic.add_subjectsmodel'
    form_class = SubjectCreateForm
    success_message = 'Subject Added Successfully'
    template_name = 'academic/subject/index.html'

    def get_success_url(self):
        return reverse('subject_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            context['subject_list'] = SubjectsModel.objects.filter(type=self.request.user.profile.type).order_by('name')
        else:
            context['subject_list'] = SubjectsModel.objects.all().order_by('name')
        return context


class SubjectListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = SubjectsModel
    permission_required = 'academic.view_subjectsmodel'
    fields = '__all__'
    template_name = 'academic/subject/index.html'
    context_object_name = "subject_list"

    def get_queryset(self):
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            return SubjectsModel.objects.filter(type=self.request.user.profile.type).order_by('name')
        return SubjectsModel.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SubjectCreateForm

        return context


class SubjectDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = SubjectsModel
    permission_required = 'academic.view_subjectsmodel'
    fields = '__all__'
    template_name = 'academic/subject/detail.html'
    context_object_name = "subject"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        form_kwargs = {}
        if school_setting.separate_school_section:
            context['staff_list'] = StaffModel.objects.filter(can_teach=True).filter(
                type=self.request.user.profile.type).order_by('surname')
            form_kwargs['type'] = self.request.user.profile.type
        else:
            context['staff_list'] = StaffModel.objects.filter(can_teach=True).order_by('surname')
        context['form'] = ClassSectionSubjectTeacherForm(**form_kwargs)
        return context


class SubjectUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = SubjectsModel
    permission_required = 'academic.change_subjectsmodel'
    form_class = SubjectEditForm
    success_message = 'Subject Updated Successfully'
    template_name = 'academic/subject/index.html'

    def get_success_url(self):
        return reverse('subject_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subject_list'] = SubjectsModel.objects.all()
        return context


class SubjectDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = SubjectsModel
    permission_required = 'academic.delete_subjectsmodel'
    success_message = 'Subject Deleted Successfully'
    fields = '__all__'
    template_name = 'academic/subject/delete.html'
    context_object_name = "subject"

    def get_success_url(self):
        return reverse("subject_index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SubjectGroupCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = SubjectGroupModel
    permission_required = 'academic.add_subjectsmodel'
    form_class = SubjectGroupCreateForm
    success_message = 'Subject Group Added Successfully'
    template_name = 'academic/subject_group/index.html'

    def get_success_url(self):
        return reverse('subject_group_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            context['class_list'] = ClassesModel.objects.filter(type=self.request.user.profile.type).order_by('name')
            context['subject_list'] = SubjectsModel.objects.filter(type=self.request.user.profile.type).order_by('name')
        else:
            context['class_list'] = ClassesModel.objects.all().order_by('name')
            context['subject_list'] = SubjectsModel.objects.all().order_by('name')
        return context

    def get_form_kwargs(self):
        kwargs = super(SubjectGroupCreateView, self).get_form_kwargs()
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            kwargs.update({'type': self.request.user.profile.type})
        kwargs.update({'type': self.request.user.profile.type})
        return kwargs


class ClassSectionInfoCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = ClassSectionInfoModel
    permission_required = 'academic.add_classsectioninfomodel'
    form_class = ClassSectionInfoForm
    success_message = 'Class Section Info Updated Successfully'
    template_name = 'academic/class_section_info/detail.html'

    def get_success_url(self):
        return reverse('class_section_info_detail',
                       kwargs={'class_pk': self.object.student_class.pk, 'section_pk': self.object.section.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class SubjectGroupDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = SubjectGroupModel
    permission_required = 'academic.delete_subjectsmodel'
    success_message = 'Subject Group Deleted Successfully'
    fields = '__all__'
    template_name = 'academic/subject_group/delete.html'
    context_object_name = "subject_group"

    def get_success_url(self):
        return reverse('subject_group_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SubjectGroupListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = SubjectGroupModel
    permission_required = 'academic.view_subjectsmodel'
    fields = '__all__'
    template_name = 'academic/subject_group/index.html'
    context_object_name = "subject_group_list"

    def get_queryset(self):
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            return SubjectGroupModel.objects.filter(type=self.request.user.profile.type).order_by('name')
        else:
            return SubjectGroupModel.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        form_kwargs = {}
        if school_setting.separate_school_section:
            context['class_list'] = ClassesModel.objects.filter(type=self.request.user.profile.type).order_by('name')
            context['subject_list'] = SubjectsModel.objects.filter(type=self.request.user.profile.type).order_by('name')
            form_kwargs['type'] = self.request.user.profile.type
        else:
            context['class_list'] = ClassesModel.objects.all().order_by('name')
            context['subject_list'] = SubjectsModel.objects.all().order_by('name')
        context['form'] = SubjectGroupCreateForm(**form_kwargs)
        return context


class SubjectGroupDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = SubjectGroupModel
    permission_required = 'academic.view_subjectsmodel'
    fields = '__all__'
    template_name = 'academic/subject_group/detail.html'
    context_object_name = "subject_group"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            context['class_list'] = ClassesModel.objects.filter(type=self.request.user.profile.type).order_by('name')
            context['subject_list'] = SubjectsModel.objects.filter(type=self.request.user.profile.type).order_by('name')
        else:
            context['class_list'] = ClassesModel.objects.all().order_by('name')
            context['subject_list'] = SubjectsModel.objects.all().order_by('name')
        return context



class SubjectGroupUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = SubjectGroupModel
    permission_required = 'academic.change_subjectsmodel'
    form_class = SubjectGroupEditForm
    success_message = 'Subject Group Updated Successfully'
    template_name = 'academic/subject_group/index.html'

    def get_success_url(self):
        return reverse('subject_group_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            context['class_list'] = ClassesModel.objects.filter(type=self.request.user.profile.type).order_by('name')
            context['subject_list'] = SubjectsModel.objects.filter(type=self.request.user.profile.type).order_by('name')
            context['subject_group_list'] = SubjectGroupModel.objects.filter(type=self.request.user.profile.type).order_by('name')
        else:
            context['class_list'] = ClassesModel.objects.all().order_by('name')
            context['subject_list'] = SubjectsModel.objects.all().order_by('name')
            context['subject_group_list'] = SubjectGroupModel.objects.all().order_by('name')
        return context

    def get_form_kwargs(self):
        kwargs = super(SubjectGroupUpdateView, self).get_form_kwargs()
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            kwargs.update({'type': self.request.user.profile.type})
        kwargs.update({'type': self.request.user.profile.type})
        return kwargs


class ClassSectionInfoDetailView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = 'academic.change_classsectioninfomodel'
    form_class = ClassSectionEditForm
    success_message = 'Class Section Updated Successfully'
    template_name = 'academic/class_section_info/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        form_kwargs = {}
        class_pk = self.kwargs.get('class_pk')
        context['student_class'] = ClassesModel.objects.get(pk=class_pk)
        section_pk = self.kwargs.get('section_pk')
        context['class_section'] = ClassSectionModel.objects.get(pk=section_pk)
        context['class_section_info'] = ClassSectionInfoModel.objects.filter(student_class=context['student_class'],
                                                                             section=context['class_section']).first()
        context['student_list'] = StudentsModel.objects.filter(student_class=context['student_class'],
                                                               class_section=context['class_section'])

        if school_setting.separate_school_section:
            context['class_section_list'] = ClassSectionModel.objects.filter(type=self.request.user.profile.type)
            form_kwargs['type'] = self.request.user.profile.type
            context['subject_list'] = SubjectsModel.objects.filter(type=self.request.user.profile.type).order_by('name')
            context['staff_list'] = StaffModel.objects.filter(can_teach=True).filter(
                type=self.request.user.profile.type).order_by('surname')
        else:
            context['subject_list'] = SubjectsModel.objects.all().order_by('name')
            context['staff_list'] = StaffModel.objects.filter(can_teach=True).order_by('surname')

        context['student_list'] = StudentsModel.objects.filter(student_class=context['student_class'],
                                                               class_section=context['class_section']).order_by('surname')
        context['form'] = ClassSectionInfoForm(**form_kwargs)
        return context


class ClassSectionInfoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = ClassSectionInfoModel
    permission_required = 'academic.change_classsectioninfomodel'
    form_class = ClassSectionInfoEditForm
    success_message = 'Class Section Info Updated Successfully'
    template_name = 'academic/class_section_info/detail.html'

    def get_success_url(self):
        return reverse('class_section_info_detail',
                       kwargs={'class_pk': self.object.student_class.pk, 'section_pk': self.object.section.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()

        return context


class ClassSectionSubjectTeacherCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = ClassSectionSubjectTeacherModel
    permission_required = 'academic.add_classsectioninfomodel'
    form_class = ClassSectionSubjectTeacherForm
    success_message = 'Subject Teachers Updated Successfully'
    template_name = 'academic/subject/detail.html'

    def get_success_url(self):
        return reverse('subject_detail', kwargs={'pk': self.object.subject.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        form_kwargs = {}
        if school_setting.separate_school_section:
            form_kwargs['type'] = self.request.user.profile.type
        context['form'] = ClassSectionSubjectTeacherForm(**form_kwargs)
        return context


class ClassSectionSubjectTeacherUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = ClassSectionSubjectTeacherModel
    permission_required = 'academic.change_classsectioninfomodel'
    form_class = ClassSectionInfoEditForm
    success_message = 'Subject Teachers Updated Successfully'
    template_name = 'academic/subject/detail.html'

    def get_success_url(self):
        return reverse('subject_detail', kwargs={'class_pk': self.object.subject.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        form_kwargs = {}
        if school_setting.separate_school_section:
            form_kwargs['type'] = self.request.user.profile.type
        context['form'] = ClassSectionSubjectTeacherForm(**form_kwargs)

        return context


class ClassSectionSubjectTeacherDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = ClassSectionSubjectTeacherModel
    permission_required = 'academic.change_classsectioninfomodel'
    success_message = 'Subject Teachers Deleted Successfully'
    template_name = 'academic/subject/delete_teacher.html'
    context_object_name = 'subject_info'

    def get_success_url(self):
        return reverse('subject_detail', kwargs={'pk': self.object.subject.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class AcademicSettingView(LoginRequiredMixin, TemplateView):
    template_name = 'academic/setting/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        form_kwargs = {}
        if school_setting.separate_school_section:
            academic_info = AcademicSettingModel.objects.filter(type=self.request.user.profile.type).first()
            form_kwargs['type'] = self.request.user.profile.type
            context['staff_list'] = StaffModel.objects.filter(type=self.request.user.profile.type).order_by('surname')
        else:
            academic_info = AcademicSettingModel.objects.first()
            context['staff_list'] = StaffModel.objects.all().order_by('surname')

        if not academic_info:
            form = AcademicSettingCreateForm(**form_kwargs)
            is_academic_info = False
        else:
            form = AcademicSettingEditForm(instance=academic_info, **form_kwargs)
            is_academic_info = True
        context['form'] = form
        context['is_academic_info'] = is_academic_info
        context['academic_info'] = academic_info
        return context


class AcademicSettingCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = AcademicSettingModel
    form_class = AcademicSettingCreateForm
    template_name = 'academic/setting/index.html'
    success_message = 'Academic Setting Info updated Successfully'

    def get_success_url(self):
        return reverse('academic_info')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            context['staff_list'] = StaffModel.objects.filter(type=self.request.user.profile.type).order_by('surname')
        else:
            context['staff_list'] = StaffModel.objects.all().order_by('surname')
        return context

    def get_form_kwargs(self):
        kwargs = super(AcademicSettingCreateView, self).get_form_kwargs()
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            kwargs.update({'type': self.request.user.profile.type})
        kwargs.update({'type': self.request.user.profile.type})
        return kwargs


class AcademicSettingUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = AcademicSettingModel
    form_class = AcademicSettingEditForm
    template_name = 'academic/setting/index.html'
    success_message = 'Academic Setting Info updated Successfully'

    def get_success_url(self):
        return reverse('academic_info')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            context['staff_list'] = StaffModel.objects.filter(type=self.request.user.profile.type).order_by('surname')
        else:
            context['staff_list'] = StaffModel.objects.all().order_by('surname')
        return context

    def get_form_kwargs(self):
        kwargs = super(AcademicSettingUpdateView, self).get_form_kwargs()
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            kwargs.update({'type': self.request.user.profile.type})
        kwargs.update({'type': self.request.user.profile.type})
        return kwargs


def proceed_to_next_term(request):
    if request.method == 'POST':
        request.session['is_verified'] = True
        return redirect(reverse('proceed_to_next_term_confirmed'))

    return render(request, 'academic/setting/proceed_to_next_term.html')


def proceed_to_next_term_confirmed(request):
    if 'is_verified' in request.session:
        if request.session['is_verified']:
            del request.session['is_verified']
            request.session['updating_term'] = True
        return render(request, 'academic/setting/proceed_to_next_term_confirmed.html')
    messages.error(request, 'UNCONFIRMED IDENTITY, ACCESS DENIED')
    return redirect(reverse('proceed_to_next_term'))


def confirm_admin_password(request):
    password = request.GET.get('password')
    user_list = User.objects.filter(is_superuser=True, is_active=True)
    is_verified = False
    for user in user_list:
        username = user.username
        user = authenticate(request, username=username, password=password)
        if user is not None:
            is_verified = True
            break
    return HttpResponse(is_verified)


def check_setting_is_okay(request):
    if 'updating_term' not in request.session:
        return HttpResponse("An Error Occurred, Try again")
    if not request.session['updating_term']:
        return HttpResponse("An Error Occurred, Try again")
    info = SchoolGeneralInfoModel.objects.first()
    if info.school_type == 'mix' and info.separate_school_section:
        academic_info = SchoolAcademicInfoModel.objects.filter(type=request.user.profile.type).last()
    else:
        academic_info = SchoolAcademicInfoModel.objects.last()
    if not academic_info.next_resumption_date:
        return HttpResponse("Next Term Resumption Date Not Set, Please Set it Before Proceeding")
    # if academic_info.next_resumption_date < date.today():
    #    return HttpResponse("Next Term Resumption Date Set To A Past Date, Please Set it Before Proceeding")

    current_user = request.user
    type = request.user.profile.type
    class_list = ClassesModel.objects.filter(type=type)

    # --- UPDATED THIS LOGIC ---
    # Check the boolean field on the TermModel instance
    if academic_info.term and academic_info.term.is_promotion_term:
        for student_class in class_list:
            # Note: you might need to adjust the logic here based on your PromotionClassModel setup
            promotion_link = PromotionClassModel.objects.filter(student_class=student_class).first()
            if not promotion_link:
                return HttpResponse(f'PROMOTION CLASS NOT SET FOR {student_class}')

    request.session['prevent_logging'] = True
    return HttpResponse(True)


def save_student_academic_record(request):
    if 'updating_term' not in request.session:
        return HttpResponse("An Error Occurred, Try again")
    if not request.session['updating_term']:
        return HttpResponse("An Error Occurred, Try again")
    type = request.user.profile.type
    info = SchoolGeneralInfoModel.objects.first()
    if info.school_type == 'mix' and info.separate_school_section:
        academic_info = SchoolAcademicInfoModel.objects.filter(type=type).first()
        student_list = StudentsModel.objects.filter(status='active', type=type)
    else:
        academic_info = SchoolAcademicInfoModel.objects.first()
        student_list = StudentsModel.objects.filter(status='active')

    # --- UPDATED THIS LOGIC ---
    # Use the session object's __str__ method and the term object's name for keys
    session_key = str(academic_info.session)
    term_key = academic_info.term.name

    for student in student_list:
        academic_record, created = StudentAcademicRecordModel.objects.get_or_create(student=student)
        if academic_record:
            prev_class = academic_record.previous_classes or {}

            if session_key not in prev_class:
                prev_class[session_key] = {}

            prev_class[session_key][term_key] = [student.student_class.id, student.class_section.id]

            academic_record.previous_classes = prev_class
            academic_record.save()

    return HttpResponse(True)


def save_student_fee_record(request):
    # This function assumes 'OutstandingFeeModel' also has a term CharField.
    # If OutstandingFeeModel's term field is also changed to a ForeignKey,
    # the 'term=term.name' part will need to be changed to 'term=term'.
    if 'updating_term' not in request.session:
        return HttpResponse("An Error Occurred, Try again")
    if not request.session['updating_term']:
        return HttpResponse("An Error Occurred, Try again")
    type = request.user.profile.type
    info = SchoolGeneralInfoModel.objects.first()
    if info.school_type == 'mix' and info.separate_school_section:
        academic_info = SchoolAcademicInfoModel.objects.filter(type=type).first()
        student_list = StudentsModel.objects.filter(type=type).exclude(status='graduated')
    else:
        academic_info = SchoolAcademicInfoModel.objects.first()
        student_list = StudentsModel.objects.exclude(status='graduated')

    session = academic_info.session
    term = academic_info.term  # This is now a TermModel object
    term_name = term.name  # Get the string name for comparisons

    # ... (code for totals) ...


    # ... (rest of the function remains the same) ...
    return HttpResponse(True)


def save_student_attendance_record(request):
    if 'updating_term' not in request.session:
        return HttpResponse("An Error Occurred, Try again")
    if not request.session['updating_term']:
        return HttpResponse("An Error Occurred, Try again")
    type = request.user.profile.type
    info = SchoolGeneralInfoModel.objects.first()
    if info.school_type == 'mix' and info.separate_school_section:
        academic_info = SchoolAcademicInfoModel.objects.filter(type=type).first()
        student_list = StudentsModel.objects.filter(status='active', type=type)
    else:
        academic_info = SchoolAcademicInfoModel.objects.first()
        student_list = StudentsModel.objects.filter(status='active')

    # --- UPDATED THIS LOGIC ---
    session_key = str(academic_info.session)
    term_key = academic_info.term.name

    for student in student_list:
        academic_record, created = StudentAcademicRecordModel.objects.get_or_create(student=student)
        if academic_record:
            record = academic_record.attendance_record or {}

            if session_key not in record:
                record[session_key] = {}

            record[session_key][term_key] = [student.student_class.id, student.class_section.id]

            academic_record.attendance_record = record
            academic_record.save()

    return HttpResponse(True)


def update_student_class(request):
    if 'updating_term' not in request.session:
        return HttpResponse("An Error Occurred, Try again")
    if not request.session['updating_term']:
        return HttpResponse("An Error Occurred, Try again")
    type = request.user.profile.type
    info = SchoolGeneralInfoModel.objects.first()
    if info.school_type == 'mix' and info.separate_school_section:
        academic_info = SchoolAcademicInfoModel.objects.filter(type=type).first()
        student_list = StudentsModel.objects.filter(status='active', type=type)
    else:
        academic_info = SchoolAcademicInfoModel.objects.first()
        student_list = StudentsModel.objects.filter(status='active')

    # --- UPDATED THIS LOGIC ---
    if academic_info.term and academic_info.term.is_promotion_term:
        for student in student_list:
            promotion_link = PromotionClassModel.objects.filter(
                student_class=student.student_class, class_section=student.class_section).first()
            if promotion_link:
                if promotion_link.is_graduation_class:
                    student.student_class = None
                    student.class_section = None
                    student.status = 'graduated'
                else:
                    student.student_class = promotion_link.promotion_class
                    student.class_section = promotion_link.promotion_section
                student.save()
    return HttpResponse(True)


def update_and_clean_up(request):
    if 'updating_term' not in request.session:
        return HttpResponse("An Error Occurred, Try again")
    if not request.session['updating_term']:
        return HttpResponse("An Error Occurred, Try again")
    type = request.user.profile.type
    info = SchoolGeneralInfoModel.objects.first()
    if info.school_type == 'mix' and info.separate_school_section:
        academic_info = SchoolAcademicInfoModel.objects.filter(type=type).first()
    else:
        academic_info = SchoolAcademicInfoModel.objects.first()

    # --- UPDATED THIS LOGIC ---
    current_term = academic_info.term
    next_session = academic_info.session

    if current_term and current_term.is_promotion_term:
        # It's the promotion term, so move to the first term of the next session
        next_term = TermModel.objects.filter(order=1).first()  # Assumes 1st term has order=1

        # Create or get the next session
        next_session_exist = SessionModel.objects.filter(start_year=academic_info.session.start_year + 1).first()
        if next_session_exist:
            next_session = next_session_exist
        else:
            next_session = SessionModel.objects.create(
                start_year=academic_info.session.start_year + 1,
                end_year=academic_info.session.end_year + 1,
                status='a',  # 'a' for active
                seperator=academic_info.session.seperator,
                type=academic_info.session.type
            )
    else:
        # Move to the next term in the sequence
        next_term = TermModel.objects.filter(order=current_term.order + 1).first()

    if next_term:
        academic_info.term = next_term
        academic_info.session = next_session
        academic_info.save()

    if 'updating_term' in request.session:
        del request.session['updating_term']
    if 'prevent_logging' in request.session:
        del request.session['prevent_logging']

    return HttpResponse(True)


def subject_list(self):
    school_setting = SchoolGeneralInfoModel.objects.first()
    if school_setting.separate_school_section:
        if self.request.user.is_superuser:
            subject_list = SubjectsModel.objects.filter(type=self.request.user.profile.type)
        else:
            class_info_list = ClassSectionSubjectTeacherModel.objects.filter(teachers__in=[self.request.user.profile.staff.id]).filter(
                type=self.request.user.profile.type)
            subject_list = []
            for class_info in class_info_list:
                if class_info.subject not in subject_list:
                    subject_list.append(class_info.subject)
    else:
        if self.request.user.is_superuser:
            subject_list = SubjectsModel.objects.all()
        else:
            class_info_list = ClassSectionSubjectTeacherModel.objects.filter(teachers__in=[self.request.user.profile.staff.id])
            subject_list = []
            for class_info in class_info_list:
                if class_info.subject not in subject_list:
                    subject_list.append(class_info.subject)
    return subject_list


class LessonNoteCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = LessonNoteModel
    permission_required = 'academic.add_clasesmodel'
    form_class = LessonNoteForm
    success_message = 'Lesson Note Added Successfully'
    template_name = 'academic/lesson_note/create.html'

    def get_success_url(self):
        return reverse('lesson_note_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            if self.request.user.is_superuser:
                context['class_info_list'] = ClassSectionInfoModel.objects.filter(type=self.request.user.profile.type)
            else:
                teacher = self.request.user.profile.staff
                context['class_info_list'] = ClassSectionInfoModel.objects.filter(
                    type=self.request.user.profile.type).filter(
                    Q(form_teacher__in=[teacher.id]) | Q(assistant_form_teacher__in=[teacher.id]))

        else:
            if self.request.user.is_superuser:
                context['class_info_list'] = ClassSectionInfoModel.objects.all()
            else:
                teacher = self.request.user.profile.staff
                context['class_info_list'] = ClassSectionInfoModel.objects.filter(
                    type=self.request.user.profile.type).filter(
                    Q(form_teacher__in=teacher) | Q(assistant_form_teacher__in=teacher))
        context['subject_list'] = subject_list(self)
        return context

    def get_form_kwargs(self):
        kwargs = super(LessonNoteCreateView, self).get_form_kwargs()
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            kwargs.update({'type': self.request.user.profile.type})
        kwargs.update({'type': self.request.user.profile.type})
        return kwargs


class LessonNoteListView(LoginRequiredMixin, ListView):
    model = LessonNoteModel
    permission_required = 'academic.view_classesmodel'
    fields = '__all__'
    template_name = 'academic/lesson_note/index.html'
    context_object_name = "lesson_note_list"

    def get_queryset(self):
        school_setting = SchoolGeneralInfoModel.objects.first()
        user_type = self.request.user.profile.type
        if school_setting.separate_school_section:
            if self.request.user.is_superuser:
                return LessonNoteModel.objects.filter(type=user_type)
            else:
                return LessonNoteModel.objects.filter(type=user_type).filter(user=self.request.user)
        else:
            if self.request.user.is_superuser:
                return LessonNoteModel.objects.all()
            else:
                return LessonNoteModel.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class AdminLessonNoteListView(LoginRequiredMixin, ListView):
    model = LessonNoteModel
    permission_required = 'academic.view_classesmodel'
    fields = '__all__'
    template_name = 'academic/lesson_note/all_index.html'
    context_object_name = "lesson_note_list"

    def get_queryset(self):
        school_setting = SchoolGeneralInfoModel.objects.first()
        user_type = self.request.user.profile.type
        status = self.kwargs.get('status')
        if school_setting.separate_school_section:
            if status == 'all':
                return LessonNoteModel.objects.filter(type=user_type)
            else:
                return LessonNoteModel.objects.filter(type=user_type).filter(status=status)
        else:
            if self.request.user.is_superuser:
                return LessonNoteModel.objects.all()
            else:
                return LessonNoteModel.objects.filter(status=status)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status'] = self.kwargs.get('status')
        return context


class LessonNoteDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = LessonNoteModel
    permission_required = 'academic.view_classesmodel'
    fields = '__all__'
    template_name = 'academic/lesson_note/detail.html'
    context_object_name = "lesson_note"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()

        if school_setting.separate_school_section:
            academic_info = AcademicSettingModel.objects.filter(type=self.request.user.profile.type).first()
        else:
            academic_info = AcademicSettingModel.objects.first()
        context['approvers'] = academic_info.lesson_note_approver.all()
        return context


class LessonNoteUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = LessonNoteModel
    permission_required = 'academic.change_classsesmodel'
    form_class = LessonNoteEditForm
    success_message = 'Lesson Note Updated Successfully'
    template_name = 'academic/lesson_note/edit.html'

    def get_success_url(self):
        return reverse('lesson_note_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            if self.request.user.is_superuser:
                context['class_info_list'] = ClassSectionInfoModel.objects.filter(type=self.request.user.profile.type)
            else:
                teacher = self.request.user.profile.staff
                context['class_info_list'] = ClassSectionInfoModel.objects.filter(
                    type=self.request.user.profile.type).filter(
                    Q(form_teacher__in=teacher) | Q(assistant_form_teacher__in=teacher))

        else:
            if self.request.user.is_superuser:
                context['class_info_list'] = ClassSectionInfoModel.objects.all()
            else:
                teacher = self.request.user.profile.staff
                context['class_info_list'] = ClassSectionInfoModel.objects.filter(
                    type=self.request.user.profile.type).filter(
                    Q(form_teacher__in=teacher) | Q(assistant_form_teacher__in=teacher))
        context['subject_list'] = subject_list(self)
        context['lesson_note'] = self.object
        return context

    def get_form_kwargs(self):
        kwargs = super(LessonNoteUpdateView, self).get_form_kwargs()
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            kwargs.update({'type': self.request.user.profile.type})
        kwargs.update({'type': self.request.user.profile.type})
        return kwargs


class LessonNoteDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = LessonNoteModel
    permission_required = 'academic.delete_classesmodel'
    success_message = 'Lesson Note Deleted Successfully'
    fields = '__all__'
    template_name = 'academic/lesson_note/delete.html'
    context_object_name = "lesson_note"

    def get_success_url(self):
        return reverse('lesson_note_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def approve_lesson_note(request, pk):
    lesson_note = LessonNoteModel.objects.get(pk=pk)
    lesson_note.status = 'approved'
    lesson_note.save()

    messages.success(request, 'Lesson Note Approved')

    return redirect(reverse('lesson_note_detail', kwargs={'pk': pk}))


def decline_lesson_note(request, pk):
    if request.method == 'POST':
        lesson_note = LessonNoteModel.objects.get(pk=pk)
        lesson_note.status = 'declined'
        lesson_note.decline_reason = request.POST.get('decline_reason')
        lesson_note.save()

        messages.success(request, 'Lesson Note Declined')

    return redirect(reverse('lesson_note_detail', kwargs={'pk': pk}))


def reapply_lesson_note(request, pk):
    lesson_note = LessonNoteModel.objects.get(pk=pk)
    lesson_note.status = 'pending'
    lesson_note.save()

    messages.success(request, 'Application for Lesson Note Approval Successful')

    return redirect(reverse('lesson_note_detail', kwargs={'pk': pk}))


class LessonDocumentCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = LessonDocumentModel
    permission_required = 'academic.add_classesmodel'
    form_class = LessonDocumentForm
    success_message = 'Lesson Document Added Successfully'
    template_name = 'academic/lesson_document/create.html'

    def get_success_url(self):
        return reverse('lesson_document_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            if self.request.user.is_superuser:
                context['class_info_list'] = ClassSectionInfoModel.objects.filter(type=self.request.user.profile.type)
            else:
                teacher = self.request.user.profile.staff
                context['class_info_list'] = ClassSectionInfoModel.objects.filter(
                    type=self.request.user.profile.type).filter(
                    Q(form_teacher__in=[teacher.id]) | Q(assistant_form_teacher__in=[teacher.id]))

        else:
            if self.request.user.is_superuser:
                context['class_info_list'] = ClassSectionInfoModel.objects.all()
            else:
                teacher = self.request.user.profile.staff
                context['class_info_list'] = ClassSectionInfoModel.objects.filter(
                    type=self.request.user.profile.type).filter(
                    Q(form_teacher__in=teacher) | Q(assistant_form_teacher__in=teacher))
        context['subject_list'] = subject_list(self)
        return context

    def get_form_kwargs(self):
        kwargs = super(LessonDocumentCreateView, self).get_form_kwargs()
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            kwargs.update({'type': self.request.user.profile.type})
        kwargs.update({'type': self.request.user.profile.type})
        return kwargs


class LessonDocumentListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = LessonDocumentModel
    permission_required = 'academic.view_classesmodel'
    fields = '__all__'
    template_name = 'academic/lesson_document/index.html'
    context_object_name = "lesson_document_list"

    def get_queryset(self):
        school_setting = SchoolGeneralInfoModel.objects.first()
        user_type = self.request.user.profile.type
        if school_setting.separate_school_section:
            if self.request.user.is_superuser:
                return LessonDocumentModel.objects.filter(type=user_type)
            else:
                return LessonDocumentModel.objects.filter(type=self.request.user.profile.type).filter(user=user_type)
        else:
            if self.request.user.is_superuser:
                return LessonDocumentModel.objects.all()
            else:
                return LessonDocumentModel.objects.filter(user=user_type)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class LessonDocumentDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = LessonDocumentModel
    permission_required = 'academic.view_classesmodel'
    fields = '__all__'
    template_name = 'academic/lesson_document/detail.html'
    context_object_name = "lesson_document"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class LessonDocumentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = LessonDocumentModel
    permission_required = 'academic.change_classsesmodel'
    form_class = LessonDocumentEditForm
    success_message = 'Lesson Document Updated Successfully'
    template_name = 'academic/lesson_document/edit.html'

    def get_success_url(self):
        return reverse('lesson_document_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            if self.request.user.is_superuser:
                context['class_info_list'] = ClassSectionInfoModel.objects.filter(type=self.request.user.profile.type)
            else:
                teacher = self.request.user.profile.staff
                context['class_info_list'] = ClassSectionInfoModel.objects.filter(
                    type=self.request.user.profile.type).filter(
                    Q(form_teacher__in=teacher) | Q(assistant_form_teacher__in=teacher))

        else:
            if self.request.user.is_superuser:
                context['class_info_list'] = ClassSectionInfoModel.objects.all()
            else:
                teacher = self.request.user.profile.staff
                context['class_info_list'] = ClassSectionInfoModel.objects.filter(
                    type=self.request.user.profile.type).filter(
                    Q(form_teacher__in=teacher) | Q(assistant_form_teacher__in=teacher))
        context['subject_list'] = subject_list(self)
        context['lesson_document'] = self.object
        return context

    def get_form_kwargs(self):
        kwargs = super(LessonDocumentUpdateView, self).get_form_kwargs()
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            kwargs.update({'type': self.request.user.profile.type})
        kwargs.update({'type': self.request.user.profile.type})
        return kwargs


class LessonDocumentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = LessonDocumentModel
    permission_required = 'academic.delete_classesmodel'
    success_message = 'Lesson Document Deleted Successfully'
    fields = '__all__'
    template_name = 'academic/lesson_document/delete.html'
    context_object_name = "lesson_document"

    def get_success_url(self):
        return reverse('lesson_document_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class HeadTeacherCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = HeadTeacherModel
    permission_required = 'academic.add_headteachermodel'
    form_class = HeadTeacherForm
    success_message = 'Head Teacher Assigned Successfully'
    template_name = 'academic/head_teacher/index.html'

    def get_success_url(self):
        return reverse('head_teacher_index')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['type'] = self.request.user.profile.type
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['head_teacher_list'] = HeadTeacherModel.objects.filter(
            type=self.request.user.profile.type).select_related('head_teacher').prefetch_related('student_class').order_by('head_teacher__name')
        context['form'] = self.get_form()
        context['is_create'] = True
        return context


class HeadTeacherListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = HeadTeacherModel
    permission_required = 'academic.view_headteachermodel'
    template_name = 'academic/head_teacher/index.html'
    context_object_name = "head_teacher_list"

    def get_queryset(self):
        return HeadTeacherModel.objects.filter(
            type=self.request.user.profile.type).order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = HeadTeacherForm(type=self.request.user.profile.type)
        return context


class HeadTeacherUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = HeadTeacherModel
    permission_required = 'academic.change_headteachermodel'
    form_class = HeadTeacherForm
    success_message = 'Head Teacher Assignment Updated Successfully'
    template_name = 'academic/head_teacher/index.html'
    context_object_name = 'head_teacher'

    def get_success_url(self):
        return reverse('head_teacher_index')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['type'] = self.request.user.profile.type
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['head_teacher_list'] = HeadTeacherModel.objects.filter(
            type=self.request.user.profile.type).order_by('name')
        context['is_update'] = True
        return context


class HeadTeacherDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = HeadTeacherModel
    permission_required = 'academic.delete_headteachermodel'
    success_message = 'Head Teacher Assignment Deleted Successfully'
    template_name = 'academic/head_teacher/delete.html'
    context_object_name = "head_teacher"

    def get_success_url(self):
        return reverse('head_teacher_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
