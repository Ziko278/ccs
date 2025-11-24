import io
import logging
import secrets

from django.contrib.messages.views import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.urls import resolve
from django.core import serializers
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from xlsxwriter import Workbook

from admin_dashboard.utility import state_list
from inventory.views import FlashFormErrorsMixin
from school_setting.models import *
from django.apps import apps
from student.models import *
from student.forms import *
from django.http import JsonResponse, HttpResponse


logger = logging.getLogger(__name__)

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
            # The 'term' is now an object from academic_setting
            term = academic_setting.term

            student_record.exit_mode = 'departure'
            student_record.session_of_departure = session
            # This line is now correct, assigning the TermModel object
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


class UtilityListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    The main view for displaying the list of utilities. It also provides
    the form instance needed for the 'Add New' modal.
    """
    model = UtilityModel
    # Assuming new permissions parallel to the original
    permission_required = 'student.view_utilitymodel'
    template_name = 'student/utility/index.html' # New template path
    context_object_name = 'utilities'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Provide an empty form for the 'Add New Utility' modal.
        if 'form' not in context:
            context['form'] = UtilityForm()
        return context


class UtilityCreateView(LoginRequiredMixin, PermissionRequiredMixin, FlashFormErrorsMixin, CreateView):
    """
    Handles the creation of a new utility. This view only processes POST
    requests from the modal form on the utility list page.
    """
    model = UtilityModel
    permission_required = 'student.add_utilitymodel'
    form_class = UtilityForm
    template_name = 'student/utility/index.html'  # Required for error redirect context

    def get_success_url(self):
        return reverse('student_utility_list') # New URL name

    def form_valid(self, form):
        messages.success(self.request, f"Utility '{form.cleaned_data['name']}' created successfully.")
        # Omitted form.instance.created_by = self.request.user (field not in model)
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        # This view should not be accessed via GET. It is a POST endpoint only.
        if request.method == 'GET':
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)


class UtilityUpdateView(LoginRequiredMixin, PermissionRequiredMixin, FlashFormErrorsMixin, UpdateView):
    """
    Handles updating an existing utility. This view only processes POST
    requests from the modal form on the utility list page.
    """
    model = UtilityModel
    permission_required = 'student.add_utilitymodel'
    form_class = UtilityForm
    template_name = 'student/utility/index.html'  # Required for error redirect context

    def get_success_url(self):
        return reverse('student_utility_list') # New URL name

    def form_valid(self, form):
        messages.success(self.request, f"Utility '{form.cleaned_data['name']}' updated successfully.")
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        # This view should not be accessed via GET. It is a POST endpoint only.
        if request.method == 'GET':
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)


class UtilityDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    Handles the actual deletion of a utility object. The confirmation
    is handled by a modal on the list page.
    """
    model = UtilityModel
    permission_required = 'student.delete_utilitymodel'
    template_name = 'student/utility/delete.html'  # New template path
    success_url = reverse_lazy('student_utility_list') # New URL name
    context_object_name = 'utility'

    def form_valid(self, form):
        # Add a success message before deleting the object.
        messages.success(self.request, f"Utility '{self.object.name}' was deleted successfully.")
        return super().form_valid(form)


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
        context['utility_list'] = UtilityModel.objects.all()


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


def identify_student_by_fingerprint(request):
    """
    Identify student by fingerprint scan
    """
    return JsonResponse({
        'success': False,
        'message': 'Fingerprint not recognized. Please try again.'
    })


def _create_parent_account(
    surname,
    last_name,
    email=None,
    mobile=None,
    title='MR',
    gender='MALE',
    marital_status='married',
    type='pri',
    excel_pid=None
):
    """
    Creates a ParentsModel record, user account, and user profile.
    Now matches the updated ParentsModel fields and supports excel_pid mapping.
    """
    # --- 1. Basic validation ---
    if not surname or not last_name:
        raise ValueError("Both surname and last_name are required to create a parent.")

    if email and User.objects.filter(email__iexact=email).exists():
        raise ValueError(f"An account with the email '{email}' already exists.")

    # --- 2. Atomic operation to keep data consistent ---
    with transaction.atomic():
        # Create Parent record
        parent = ParentsModel.objects.create(
            title=title.upper() if title else 'MR',
            surname=surname.strip().title(),
            last_name=last_name.strip().title(),
            email=email,
            mobile=mobile,
            gender=gender.upper() if gender else 'MALE',
            marital_status=marital_status.lower() if marital_status else 'married',
            type=type.lower() if type else 'pri',
            excel_pid=excel_pid,  # ✅ store PID for linkage
        )

        # Ensure parent_id is generated
        if not parent.parent_id:
            parent.save()

        username = parent.parent_id

        # --- 3. Generate secure random password ---
        alphabet = 'abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'
        password = ''.join(secrets.choice(alphabet) for _ in range(10))

        # --- 4. Create linked User account ---
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=parent.surname,
            last_name=parent.last_name
        )

        # --- 5. Create profile link ---
        UserProfileModel.objects.create(
            user=user,
            parent=parent,
            default_password=password,
            reference_id=parent.id
        )

    return parent


@login_required
def paste_create_parents_view(request):
    """
    Renders the HTML page with the textarea for pasting parent JSON.
    """
    return render(request, 'student/paste_create_parents.html')


@login_required
@require_POST
def ajax_create_parent_view(request):
    """
    AJAX endpoint to create one parent record.
    Accepts excel_pid for future student-parent mapping.
    """
    try:
        data = json.loads(request.body)
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email') or None
        mobile = data.get('mobile') or None
        excel_pid = data.get('excel_pid')  # ✅ new field

        if not first_name:
            return JsonResponse({'status': 'error', 'message': 'First Name is required.'}, status=400)

        parent = _create_parent_account(first_name, last_name, email, mobile)

        # ✅ Store Excel PID for future mapping
        if excel_pid:
            parent.excel_pid = excel_pid
            parent.save(update_fields=['excel_pid'])

        return JsonResponse({
            'status': 'success',
            'message': (
                f"Successfully created parent '{parent.surname} {parent.last_name}' "
                f"(Parent ID: {parent.parent_id}, Excel PID: {parent.excel_pid})."
            )
        })

    except ValueError as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    except Exception as e:
        logger.error("Error in ajax_create_parent_view: %s", e, exc_info=True)
        return JsonResponse({'status': 'error', 'message': 'A critical server error occurred. Check logs.'}, status=500)


@login_required
@require_POST
@transaction.atomic
def ajax_create_student_view(request):
    """
    AJAX endpoint to create one student and their wallet.
    Uses excel_pid to find and link the parent.
    """
    try:
        data = json.loads(request.body)
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        gender_raw = data.get('gender')
        class_code = data.get('class_code')
        class_section_name = data.get('class_section_name')
        excel_pid = data.get('excel_pid')  # ✅ required now

        # --- 1. Validate ---
        if not all([first_name, last_name, gender_raw, class_code, class_section_name, excel_pid]):
            return JsonResponse({'status': 'error', 'message': 'Missing required fields.'}, status=400)

        # --- 2. Find Parent ---
        parent = ParentsModel.objects.filter(excel_pid=excel_pid).first()
        if not parent:
            raise ValueError(f"No parent found with excel_pid={excel_pid}.")

        # --- 3. Find Class and Section ---
        try:
            student_class = ClassesModel.objects.get(code__iexact=class_code)
        except ClassesModel.DoesNotExist:
            raise ValueError(f"Class with code '{class_code}' does not exist.")

        class_section, _ = ClassSectionModel.objects.get_or_create(
            name__iexact=class_section_name,
            defaults={'name': class_section_name}
        )

        # --- 4. Map Gender ---
        gender = None
        if gender_raw.upper().startswith('F'):
            gender = StudentsModel.GENDER[1][0]
        elif gender_raw.upper().startswith('M'):
            gender = StudentsModel.GENDER[0][0]
        else:
            raise ValueError(f"Invalid gender value: '{gender_raw}'. Use 'M' or 'F'.")

        # --- 5. Create Student ---
        student = StudentsModel.objects.create(
            surname=last_name,
            last_name=first_name,  # adjust if your name order differs
            gender=gender,
            parent=parent,
            student_class=student_class,
            class_section=class_section,
            type='pri',  # or 'sec' depending on your data
            relationship_with_parent='father',  # default; can update later
        )

        # --- 6. Create Wallet ---
        StudentWalletModel.objects.create(student=student)

        return JsonResponse({
            'status': 'success',
            'message': (
                f"Student '{student.surname} {student.last_name}' "
                f"({student.registration_number}) created and linked to parent '{parent}'."
            )
        })

    except ValueError as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    except Exception as e:
        logger.error("Critical error in ajax_create_student_view: %s", e, exc_info=True)
        return JsonResponse({'status': 'error', 'message': 'A critical server error occurred. Check logs.'}, status=500)


@login_required
def paste_create_students_view(request):
    """
    Renders the HTML page with the textarea for pasting student JSON.
    """
    return render(request, 'student/paste_create_students.html')
