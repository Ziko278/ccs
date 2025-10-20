import secrets
from datetime import date, timedelta

from django.core.mail import send_mail
from django.db.models import Sum, Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags
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


def setup_test():
    info = SchoolGeneralInfoModel.objects.first()
    if info:
        return True
    return False


def fix(request):
    student_list = StudentsModel.objects.all()
    for student in student_list:
        if student.student_class.name.lower() == 'js 2':
            if student.class_section == 'blue':
                student.class_section = 'white'
            if student.class_section == 'white':
                student.class_section = 'blue'

        student.subject_group = SubjectGroupModel.objects.filter(student_class=student.student_class).first()
        student.save()


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