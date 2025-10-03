from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.messages.views import SuccessMessageMixin, messages
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from school_setting.models import SchoolGeneralInfoModel, SchoolAcademicInfoModel
from django.core.mail import EmailMessage, send_mail, get_connection
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.core import serializers
from num2words import num2words
from communication.models import *
from communication.forms import *


class SMTPConfigurationCreateView(SuccessMessageMixin, CreateView):
    model = SMTPConfigurationModel
    form_class = SMTPConfigurationForm
    success_message = 'Email Configuration Added Successfully'
    template_name = 'communication/smtp_configuration/index.html'

    def get_success_url(self):
        return reverse('smtp_configuration_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            context['smtp_configuration_list'] = SMTPConfigurationModel.objects.filter(
                type=self.request.user.profile.type).order_by('name')
        else:
            context['smtp_configuration_list'] = SMTPConfigurationModel.objects.all().order_by('name')
        return context


class SMTPConfigurationListView(ListView):
    model = SMTPConfigurationModel
    fields = '__all__'
    template_name = 'communication/smtp_configuration/index.html'
    context_object_name = "smtp_configuration_list"

    def get_queryset(self):
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            return SMTPConfigurationModel.objects.filter(type=self.request.user.profile.type).order_by('name')
        else:
            return SMTPConfigurationModel.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SMTPConfigurationForm

        return context


class SMTPConfigurationUpdateView(SuccessMessageMixin, UpdateView):
    model = SMTPConfigurationModel
    form_class = SMTPConfigurationEditForm
    success_message = 'Email Configuration Updated Successfully'
    template_name = 'communication/smtp_configuration/index.html'

    def get_success_url(self):
        return reverse('smtp_configuration_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            context['smtp_configuration_list'] = SMTPConfigurationModel.objects.filter(
                type=self.request.user.profile.type).order_by('name')
        else:
            context['smtp_configuration_list'] = SMTPConfigurationModel.objects.all().order_by('name')

        return context


class SMTPConfigurationDeleteView(SuccessMessageMixin, DeleteView):
    model = SMTPConfigurationModel
    success_message = 'Email Configuration Deleted Successfully'
    fields = '__all__'
    template_name = 'communication/smtp_configuration/delete.html'
    context_object_name = "smtp_configuration"

    def get_success_url(self):
        return reverse("smtp_configuration_index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SMSConfigurationCreateView(SuccessMessageMixin, CreateView):
    model = SMSConfigurationModel
    form_class = SMSConfigurationForm
    success_message = 'SMS Configuration Added Successfully'
    template_name = 'communication/sms_configuration/index.html'

    def get_success_url(self):
        return reverse('sms_configuration_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            context['sms_configuration_list'] = SMSConfigurationModel.objects.filter(
                type=self.request.user.profile.type).order_by('name')
        else:
            context['sms_configuration_list'] = SMSConfigurationModel.objects.all().order_by('name')
        return context



def check_mail_setup(request, user_type=None):
    setting_info = SchoolGeneralInfoModel.objects.first()
    if not user_type:
        user_type = request.user.profile.type
    if setting_info.school_type == 'mix' and setting_info.separate_school_section:
        communication_setting = CommunicationSettingModel.objects.filter(type=user_type).first()
    else:
        communication_setting = CommunicationSettingModel.objects.first()
    if not communication_setting:
        messages.error(request, 'Communication Setting Not Found, Try Later')
        return redirect(request.META.get('HTTP_REFERER', '/'))
    if not communication_setting.default_smtp:
        messages.error(request, 'Email Setting Not Found, Try Later')
        return redirect(request.META.get('HTTP_REFERER', '/'))
    smtp_config = communication_setting.default_smtp
    smtp_connection = get_connection(
        host=smtp_config.host,
        port=smtp_config.port,
        username=smtp_config.username,
        password=smtp_config.password,
        use_tls=True,  # Adjust based on your SMTP configuration
    )
    return smtp_connection, smtp_config.email


def send_email(request):
    smtp_connection, sender_email = check_mail_setup(request)

    if request.method == 'POST':
        setting_info = SchoolGeneralInfoModel.objects.first()
        subject = request.POST.get('subject')
        body = request.POST.get('body')

        context = {
            'domain': get_current_site(request),
            'subject': subject,
            'body': body
        }
        mail_subject = "{} - {}".format(setting_info.name.title(), subject.upper())
        email_list = []
        email_string = request.POST.get('email')
        if email_string:
            email_string_list = email_string.split(",")
            for mail in email_string_list:
                email_list.append(mail.strip().lower())
        if 'recipient' in request.POST:
            recipient = request.POST.getlist('recipient')
            if 'student' in recipient:
                if setting_info.school_type == 'mix' and setting_info.separate_school_section:
                    student_list = StudentsModel.objects.filter(type=request.user.profile.type, status='active')
                else:
                    student_list = StudentsModel.objects.filter(status='active')
                for student in student_list:
                    if student.email and student.email not in email_list:
                        email_list.append(student.email)

            if 'staff' in recipient:
                if setting_info.school_type == 'mix' and setting_info.separate_school_section:
                    staff_list = StaffModel.objects.filter(type=request.user.profile.type, status='active')
                else:
                    staff_list = StaffModel.objects.filter(status='active')
                for staff in staff_list:
                    if staff.email and staff.email not in email_list:
                        email_list.append(staff.email)

            if 'all_parent' in recipient:
                if setting_info.school_type == 'mix' and setting_info.separate_school_section:
                    parent_list = ParentsModel.objects.filter(type=request.user.profile.type, status='active')
                else:
                    parent_list = ParentsModel.objects.filter(status='active')
                for parent in parent_list:
                    if parent.email:
                        email_list.append(parent.email)
            elif 'parent' in recipient:
                if setting_info.school_type == 'mix' and setting_info.separate_school_section:
                    parent_list = ParentsModel.objects.filter(type=request.user.profile.type, status='active')
                else:
                    parent_list = ParentsModel.objects.filter(status='active')
                for parent in parent_list:
                    if parent.email and parent.email not in email_list:
                        email_list.append(parent.email)

        html_message = render_to_string('communication/template/send_mail.html', context)
        plain_message = strip_tags(html_message)

        mail_sent = 0
        for email in email_list:
            mail_sent += send_mail(mail_subject, plain_message, sender_email, [email], html_message=html_message,
                                   fail_silently=True, connection=smtp_connection)

        if mail_sent > 0:
            messages.success(request, '{} Mail(s) sent successfully'.format(mail_sent))
            return redirect(reverse('send_email'))
        else:
            messages.warning(request, 'No mail sent, this may be due to wrong addresses provided')
            return redirect(reverse('send_email'))

    return render(request, 'communication/mail/send.html')


def send_user_account_auto_mail(request):
    smtp_connection, sender_email = check_mail_setup(request)
    if request.method == 'POST':
        email_list = []
        user_detail = {}
        if 'recipient' in request.POST:
            setting_info = SchoolGeneralInfoModel.objects.first()
            recipient = request.POST.getlist('recipient')
            no_mail = 0
            no_mail_error = ''
            if 'student' in recipient:
                if setting_info.school_type == 'mix' and setting_info.separate_school_section:
                    student_list = StudentsModel.objects.filter(type=request.user.profile.type, status='active')
                else:
                    student_list = StudentsModel.objects.filter(status='active')
                for student in student_list:
                    if student.email and student.email not in email_list:
                        email_list.append(student.email)
                        user_detail[student.email] = {
                            'full_name': "{} {}".format(student.surname, student.last_name),
                            'username': student.student_account.user.username,
                            'password': student.student_account.default_password
                        }
                    else:
                        no_mail += 1

            if 'staff' in recipient:
                if setting_info.school_type == 'mix' and setting_info.separate_school_section:
                    staff_list = StaffModel.objects.filter(type=request.user.profile.type, status='active')
                else:
                    staff_list = StaffModel.objects.filter(status='active')
                for staff in staff_list:
                    if staff.email and staff.email not in email_list:
                        email_list.append(staff.email)
                        user_detail[staff.email] = {
                            'full_name': "{} {}".format(staff.surname, staff.last_name),
                            'username': staff.account.user.username,
                            'password': staff.account.default_password
                        }
                    else:
                        no_mail += 1

            if 'parent' in recipient:
                if setting_info.school_type == 'mix' and setting_info.separate_school_section:
                    parent_list = ParentsModel.objects.filter(type=request.user.profile.type, status='active')
                else:
                    parent_list = ParentsModel.objects.filter(status='active')
                for parent in parent_list:
                    if parent.email and parent.email not in email_list:
                        email_list.append(parent.email)
                        user_detail[parent.email] = {
                            'full_name': "{} {}".format(parent.surname, parent.last_name),
                            'username': parent.parent_account.user.username,
                            'password': parent.parent_account.default_password
                        }
                    else:
                        no_mail += 1

            if no_mail > 0:
                no_mail_error += '{} users without email were skipped'.format(no_mail)
            subject = 'User Account Details'
            context = {
                'domain': get_current_site(request),
                'subject': subject,
                'school_info': setting_info
            }
            successful_mail, error_mail = 0, 0
            mail_subject = "{} - {}".format(setting_info.name.title(), subject.upper())
            for email in email_list:
                context['username'] = user_detail[email]['username']
                context['password'] = user_detail[email]['password']
                html_message = render_to_string('communication/template/user_detail_auto_mail.html', context)
                plain_message = strip_tags(html_message)
                try:
                    mail_sent = send_mail(mail_subject, plain_message, 'odekeziko@gmail.com', [email], html_message=html_message,
                                          fail_silently=True, connection=smtp_connection)
                    if mail_sent:
                        successful_mail += 1
                    else:
                        error_mail += 1
                except Exception as e:
                    pass
                    return HttpResponse(str(e))

            if successful_mail == 0:
                messages.error(request, '{}, No User Detail was successfully sent'.format(no_mail_error))
            elif successful_mail == len(email_list):
                messages.success(request, "{}, All {} User Detail(s) was successfully sent".format(no_mail_error, successful_mail))
            else:
                messages.warning(request,
                    "{}, {} successfully sent user detail(s), {} failed".format(no_mail_error, successful_mail,
                                                                            len(email_list) - successful_mail))
            return redirect(reverse('user_account_auto_mail'))
        messages.error(request, 'No User Set was selected')
    return render(request, 'communication/mail/auto_mail.html')


def send_user_password_reset_mail(request, email, full_name, default_password, user_type):
    smtp_connection, sender_email = check_mail_setup(request, user_type)
    setting_info = SchoolGeneralInfoModel.objects.first()
    subject = 'User Account Details'
    context = {
        'domain': get_current_site(request),
        'subject': subject,
        'school_info': setting_info,
        'default_password': default_password,
        'full_name': full_name
    }

    html_message = render_to_string('communication/template/user_password_reset_mail.html', context)
    plain_message = strip_tags(html_message)
    mail_subject = "{} - {}".format(setting_info.name.title(), subject.upper())
    try:
        mail_sent = send_mail(mail_subject, plain_message, sender_email, [email], html_message=html_message,
                              fail_silently=True, connection=smtp_connection)
        if mail_sent:
            return True
        else:
            return False
    except Exception as e:
        return e



class CommunicationSettingView(LoginRequiredMixin, TemplateView):
    template_name = 'communication/setting/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()
        form_kwargs = {}
        if school_setting.separate_school_section:
            communication_info = CommunicationSettingModel.objects.filter(type=self.request.user.profile.type).first()
            form_kwargs['type'] = self.request.user.profile.type
        else:
            communication_info = CommunicationSettingModel.objects.first()

        if not communication_info:
            form = CommunicationSettingCreateForm(**form_kwargs)
            is_communication_info = False
        else:
            form = CommunicationSettingEditForm(instance=communication_info, **form_kwargs)
            is_communication_info = True
        context['form'] = form
        context['is_communication_info'] = is_communication_info
        context['communication_info'] = communication_info
        return context


class CommunicationSettingCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = CommunicationSettingModel
    form_class = CommunicationSettingCreateForm
    template_name = 'communication/setting/index.html'
    success_message = 'Communication Settings updated Successfully'

    def get_success_url(self):
        return reverse('finance_info')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_setting = SchoolGeneralInfoModel.objects.first()

        return context

    def get_form_kwargs(self):
        kwargs = super(CommunicationSettingCreateView, self).get_form_kwargs()
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            kwargs.update({'type': self.request.user.profile.type})
        kwargs.update({'type': self.request.user.profile.type})
        return kwargs


class CommunicationSettingUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = CommunicationSettingModel
    form_class = CommunicationSettingEditForm
    template_name = 'communication/setting/index.html'
    success_message = 'Communication Setting updated Successfully'

    def get_success_url(self):
        return reverse('communication_info')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

    def get_form_kwargs(self):
        kwargs = super(CommunicationSettingUpdateView, self).get_form_kwargs()
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            kwargs.update({'type': self.request.user.profile.type})
        kwargs.update({'type': self.request.user.profile.type})
        return kwargs
