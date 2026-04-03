import secrets
import string
import traceback
from datetime import date, timedelta

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.db import transaction
from django.db.models import Sum, Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin, messages
# from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from communication.models import RecentActivityModel
from finance.models import FeePaymentModel, FeeModel
from human_resource.models import StaffModel
from result.models import ResultModel, TextResultModel
from student.models import StudentsModel
from school_setting.models import SchoolGeneralInfoModel, SchoolAcademicInfoModel
from academic.models import ClassSectionInfoModel, ClassesModel, ClassSectionModel, SubjectGroupModel
from user_management.models import UserProfileModel

from result.models import ResultFieldModel


def setup_test():
    info = SchoolGeneralInfoModel.objects.first()
    if info:
        return True
    return False


def fix(request):
    student_list = StudentsModel.objects.all()
    blue = ClassSectionModel.objects.get(name='blue')
    white = ClassSectionModel.objects.get(name='white')

    for student in student_list:
        if student.student_class.name.lower() == 'js 2':
            if student.class_section.name == 'blue':
                student.class_section = white
            if student.class_section.name == 'white':
                student.class_section = blue
            student.save()


    class_info_list = ClassSectionInfoModel.objects.all()

    for class_info in class_info_list:
        if class_info.section.name == 'blue':
            class_info.section = white
        if class_info.section.name == 'white':
            class_info.section = blue
            class_info.save()


class AdminDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'admin_dashboard/dashboard.html'

    def dispatch(self, *args, **kwargs):
        if setup_test():
            return super(AdminDashboardView, self).dispatch(*args, **kwargs)
        else:
            return redirect(reverse('maintenance_view'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        type = self.request.user.profile.type
        info = SchoolGeneralInfoModel.objects.first()
        if info.school_type == 'mix' and info.separate_school_section:
            academic_info = SchoolAcademicInfoModel.objects.filter(type=type).first()
            context['active_students'] = StudentsModel.objects.filter(status='active', type=type).count()
        else:
            context['active_students'] = StudentsModel.objects.filter(status='active').count()
            academic_info = SchoolAcademicInfoModel.objects.first()
        session = academic_info.session
        term = academic_info.term

        if info.school_type == 'mix' and info.separate_school_section:
            context['notification_list'] = RecentActivityModel.objects.filter(session=session, term=term,
                                           type=type).order_by('id').reverse()[:15]
            context['student_class_list'] = ClassSectionInfoModel.objects.filter(type=type)
        else:
            context['notification_list'] = RecentActivityModel.objects.filter(session=session, term=term).order_by(
                'id').reverse()[:15]

        return context


class AdminMaintenanceView(TemplateView):
    template_name = 'admin_dashboard/maintenance.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


def get_last_monday():
    today = date.today()
    last_monday = today - timedelta(days=today.weekday())  # Monday of the current week
    return last_monday


def send_fee_summary_email(request):
    try:
        # Get the current academic session and term
        academic_info = SchoolAcademicInfoModel.objects.first()
        if not academic_info:
            return JsonResponse({"success": False, "message": "No academic session found"}, status=400)

        session = academic_info.session
        term = academic_info.term

        # Get last Monday
        last_monday = get_last_monday()
        today = date.today()

        # Get fee payment summary from last Monday to today
        payments = FeePaymentModel.objects.filter(date__range=[last_monday, today], status='confirmed')
        total_fee_paid = payments.aggregate(total=Sum("amount"), count=Count("id"))

        # Get fee payments for the given session and term
        term_payments = FeePaymentModel.objects.filter(session=session, term=term, status='confirmed')
        total_term_paid = term_payments.aggregate(total=Sum("amount"), count=Count("id"))

        # Group payments by fee type
        fee_summaries = []
        for fee in FeeModel.objects.all():
            fee_payments = payments.filter(fee__fee=fee)
            fee_total = fee_payments.aggregate(total=Sum("amount"), count=Count("id"))
            if fee_total["total"]:
                fee_summaries.append({
                    "name": fee.name,
                    "total_paid": fee_total["total"],
                    "count": fee_total["count"]
                })

        # Prepare email content
        context = {
            "last_monday": last_monday,
            "today": today,
            "fee_summaries": fee_summaries,
            "total_fee_paid": total_fee_paid["total"] or 0,
            "total_payments_made": total_fee_paid["count"] or 0,
            "total_term_paid": total_term_paid["total"] or 0,
            "total_term_payments_made": total_term_paid["count"] or 0,
            "session": session,
            "term": term
        }

        subject = f"White Cloud Academy Fee Payment Summary ({last_monday} - {today})"
        html_message = render_to_string("admin_dashboard/fee_summary.html", context)
        plain_message = strip_tags(html_message)
        from_email = "whitecloudsauto@gmail.com"
        recipient_list = ["nkiruumahi48@gmail.com", "chika.agwu@whitecloudschool.sch.ng",
                          "accounts@whitecloudschool.sch.ng", "og4chy@gmail.com", "chikagwu@icloud.com",
                          "ucheigweonu@gmail.com", "odekeziko@gmail.com"]

        # Send email
        send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)

        return JsonResponse({"success": True, "message": "Fee summary email sent successfully!"})

    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=400)


def fix_issue(request):
    """
    Sets the 'type' field of all UserProfileModel instances (excluding those
    already with type 'pri') to 'pri' and saves the changes.
    """
    profiles_updated = UserProfileModel.objects.exclude(type='pri').update(type='pri')

    if profiles_updated > 0:
        messages.success(request, f"{profiles_updated} user profiles updated to 'PRIMARY'.")
    else:
        messages.info(request, "No user profiles needed updating to 'PRIMARY'.")
    return HttpResponse('updated')



@login_required
@permission_required('student.add_studentsmodel', raise_exception=True)
def fix_missing_student_profiles(request):
    """
    Creates login credentials for students that don't already have a user profile.
    Students with an existing profile are left completely untouched.
    """
    created_count = 0
    skipped_count = 0

    alphabet = string.ascii_letters + string.digits

    # Only get students without a linked profile
    students_without_profile = StudentsModel.objects.filter(
        student_account__isnull=True
    )

    print(f"Students without profile: {students_without_profile.count()}")

    for student in students_without_profile:
        try:
            print(f"PROCESSING: {student} | reg: {student.registration_number}")

            if not student.registration_number:
                skipped_count += 1
                print(f"SKIPPED (no reg no): {student}")
                continue

            username = student.registration_number.lower()

            # Clean up any orphaned user with the same username
            existing_user = User.objects.filter(username=username).first()
            if existing_user:
                print(f"Found orphaned user for {username}, cleaning up...")
                UserProfileModel.objects.filter(user=existing_user).delete()
                existing_user.delete()

            # Generate secure 8-character password
            password = ''.join(secrets.choice(alphabet) for _ in range(8))

            # Create new user
            user = User.objects.create(
                username=username,
                email="",
                password=make_password(password),
                first_name=student.first_name,
                last_name=student.last_name,
            )
            print(f"Created user: {username}")

            # Create corresponding user profile
            UserProfileModel.objects.create(
                user=user,
                student=student,
                reference='student',
                reference_id=student.id,
                default_password=password,
                type=student.type if hasattr(student, 'type') else None,
            )
            print(f"Created profile for: {username}")

            created_count += 1

        except Exception as e:
            skipped_count += 1
            print(f"⚠️ ERROR processing {student} | reg: {student.registration_number} | error: {e}")
            traceback.print_exc()

    print(f"DONE — created: {created_count}, skipped: {skipped_count}")

    messages.success(
        request,
        f"✅ {created_count} student login accounts created successfully. "
        f"⏭️ {skipped_count} skipped (missing reg no or error)."
    )

    return redirect('admin_dashboard')

@login_required
@permission_required("student.change_resultmodel", raise_exception=True)
def result_cleanup_view(request):
    """
    Displays the result cleanup page.
    """
    # Get current session and term info
    academic_info = SchoolAcademicInfoModel.objects.first()

    # Get count of results that need cleaning
    results_count = 0
    if academic_info and academic_info.session and academic_info.term:
        results_count = ResultModel.objects.filter(
            session=academic_info.session,
            term=academic_info.term,
            result__isnull=False
        ).count()

    context = {
        'academic_info': academic_info,
        'results_count': results_count,
    }
    return render(request, 'admin_dashboard/result_cleanup.html', context)


@require_POST
@login_required
@permission_required("student.change_resultmodel", raise_exception=True)
def process_result_cleanup(request):
    """
    Removes blank/zero subjects from result JSON and resaves to recalculate totals.
    A subject is removed if:
      - Its total is zero/blank, OR
      - Any of its exam-type fields is empty/zero
    Processes all results for the current session and term.
    """
    try:
        academic_info = SchoolAcademicInfoModel.objects.first()

        if not academic_info or not academic_info.session or not academic_info.term:
            return JsonResponse({
                'status': 'error',
                'message': 'No active academic session/term found'
            }, status=400)

        current_session = academic_info.session
        current_term = academic_info.term

        # Fetch all exam field names once (uppercased to match JSON keys)
        exam_field_names = set(
            ResultFieldModel.objects.filter(field_type='exam')
            .values_list('name', flat=True)
        )
        exam_field_names_upper = {name.upper() for name in exam_field_names}

        results_to_clean = ResultModel.objects.filter(
            session=current_session,
            term=current_term,
            result__isnull=False
        ).select_related('student', 'student_class')

        cleaned_count = 0
        skipped_count = 0
        total_subjects_removed = 0

        with transaction.atomic():
            for result_obj in results_to_clean:
                if not result_obj.result or not isinstance(result_obj.result, dict):
                    skipped_count += 1
                    continue

                original_result = result_obj.result.copy()
                cleaned_result = {}
                subjects_removed = 0

                for key, subject_data in original_result.items():
                    if subject_data and isinstance(subject_data, dict):
                        total = subject_data.get('total', 0)

                        # Check 1: total must be non-zero
                        try:
                            total_valid = float(total) > 0
                        except (ValueError, TypeError):
                            total_valid = False

                        # Check 2: no exam field should be empty/zero
                        exam_fields_valid = True
                        if total_valid and exam_field_names_upper:
                            for field_key, field_value in subject_data.items():
                                if field_key.upper() in exam_field_names_upper:
                                    try:
                                        if not field_value or float(field_value) == 0:
                                            exam_fields_valid = False
                                            break
                                    except (ValueError, TypeError):
                                        exam_fields_valid = False
                                        break

                        if total_valid and exam_fields_valid:
                            cleaned_result[key] = subject_data
                        else:
                            subjects_removed += 1
                    else:
                        subjects_removed += 1

                if subjects_removed > 0:
                    result_obj.result = cleaned_result
                    result_obj.save()
                    cleaned_count += 1
                    total_subjects_removed += subjects_removed
                else:
                    skipped_count += 1

        return JsonResponse({
            'status': 'success',
            'cleaned': cleaned_count,
            'skipped': skipped_count,
            'subjects_removed': total_subjects_removed,
            'session': str(current_session),
            'term': str(current_term)
        })

    except Exception as e:
        traceback.print_exc()
        return JsonResponse({
            'status': 'error',
            'message': f'An unexpected error occurred: {str(e)}'
        }, status=500)

@login_required
@permission_required("student.change_resultmodel", raise_exception=True)
def process_result_save(request):
    """
    Removes blank/zero subjects from result JSON and resaves to recalculate totals.
    Processes all results for the current session and term.
    """
    try:
        cleaned_count = 0
        result_list = ResultModel.objects.all()
        total = ResultModel.objects.count()

        with transaction.atomic():
            for result in result_list:
                result.save()
                cleaned_count += 1

        return JsonResponse({
            'status': 'success',
            'cleaned': cleaned_count,
            'total': total
        })

    except Exception as e:
        traceback.print_exc()
        return JsonResponse({
            'status': 'error',
            'message': f'An unexpected error occurred: {str(e)}'
        }, status=500)
