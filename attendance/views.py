from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin, messages
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from student.models import StudentsModel, ParentsModel
from human_resource.models import StaffModel
from attendance.models import *
from attendance.templatetags.attendance_custom_filters import *


class DailyAttendanceView(TemplateView):
    template_name = 'attendance/daily_attendance.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def daily_attendance_api(request):
    identifier = request.GET.get('identifier').lower()
    type = request.user.profile.type
    school_setting = SchoolGeneralInfoModel.objects.first()
    if school_setting.separate_school_section:
        academic_setting = SchoolAcademicInfoModel.objects.filter(type=type).first()
    else:
        academic_setting = SchoolAcademicInfoModel.objects.first()
    term = academic_setting.term
    session = academic_setting.session
    student = StudentsModel.objects.filter(type=type, registration_number=identifier).first()
    staff = StaffModel.objects.filter(type=type, staff_id=identifier).first()
    if student:
        surname = student.surname.title()
        last_name = student.last_name.title()
    elif staff:
        surname = staff.surname.title()
        last_name = staff.last_name.title()
    today = datetime.now().strftime("%d-%m-%y")
    time = datetime.now().strftime("%H:%M")
    if student:
        student_attendance = StudentAttendanceModel.objects.filter(session=session, term=term,
                                                                   student_class=student.student_class,
                                                                   class_section=student.class_section,
                                                                   student=student).first()
        if student_attendance:
            if today in student_attendance.attendance:
                if not student_attendance.attendance[today]["sign_out"]:
                    student_attendance.attendance[today]["sign_out"] = time
                    student_attendance.save()
                    message = 'Student {} {} signed Out Successfully'.format(surname, last_name)
                    status = True
                else:
                    message = 'Student {} {} Already Signed Out'.format(surname, last_name)
                    status = False
            else:
                attendance = {
                    "sign_in": time,
                    "sign_out": False
                }
                student_attendance.attendance[today] = attendance
                student_attendance.save()
                message = 'Student {} {} signed In Successfully'.format(surname, last_name)
                status = True
        else:
            attendance = {
                today: {
                    "sign_in": time,
                    "sign_out": False
                }
            }
            student_attendance = StudentAttendanceModel.objects.create(session=session, term=term,
                                                                       student_class=student.student_class,
                                                                       class_section=student.class_section,
                                                                       student=student, type=type,
                                                                       attendance=attendance)
            student_attendance.save()
            message = 'Student {} {} signed In Successfully'.format(surname, last_name)
            status = True
    elif staff:
        staff_attendance = StaffAttendanceModel.objects.filter(session=session, term=term, staff=staff).first()
        if staff_attendance:
            if today in staff_attendance.attendance:
                if not staff_attendance.attendance[today]["sign_out"]:
                    staff_attendance.attendance[today]["sign_out"] = time
                    staff_attendance.save()
                    message = 'Staff {} {} signed Out Successfully'.format(surname, last_name)
                    status = True
                else:
                    message = 'Staff {} {} Already Signed Out'.format(surname, last_name)
                    status = False
            else:
                attendance = {
                    "sign_in": time,
                    "sign_out": False
                }
                staff_attendance.attendance[today] = attendance
                staff_attendance.save()
                message = 'Staff {} {} signed In Successfully'.format(surname, last_name)
                status = True
        else:
            attendance = {
                today: {
                    "sign_in": time,
                    "sign_out": False
                }
            }
            staff_attendance = StaffAttendanceModel.objects.create(session=session, term=term, staff=staff, type=type,
                                                                   attendance=attendance)
            staff_attendance.save()
            message = 'Staff {} {} signed In Successfully'.format(surname, last_name)
            status = True
    else:
        status = False
        message = "UNKNOWN IDENTIFICATION"

    result = ""

    if student:
        result += """<div class ='row'>
                        <div class ='col-md-4'>
                    """
        if student.image:
            result += """
            <image src = '/media/{}' style = 'width:100px;height:100px;border-radius:5px;' />
            """.format(student.image)
        if not student.image:
            result += """
                   <image src = '/static/admin_dashboard/images/default_image.jpg' style = 'width:100px;height:100px;border-radius:5px;' />
                   """
        result += """
                        </div>
        """
        result += """
            <div class ='col-md-8'>
                <p> {} {}</p>
                <p> {} </p>
                <p> {} {} </p>
            </div>
        </div>
        """.format(surname, last_name, identifier.upper(), student.student_class, student.class_section)
        if status:
            result += """<p class='text-success'><b> {} </b></p>""".format(message)
            result += """<p class='text-success'><b> {} {} </b></p>""".format(today, time)
        else:
            result += """<p class='text-danger'><b> {} </b></p>""".format(message)
    elif staff:
        result += """<div class ='row'>
                                <div class ='col-md-4'>
                            """
        if staff.image:
            result += """
                    <image src = '/media/{}' style = 'width:100px;height:100px;border-radius:5px;' />
                    """.format(staff.image)
        if not staff.image:
            result += """
                           <image src = '/static/admin_dashboard/images/default_image.jpg' style = 'width:100px;height:100px;border-radius:5px;' />
                      """
        result += """
                                </div>
                """
        result += """
                    <div class ='col-md-8'>
                        <p> {} {}</p>
                        <p> {} </p>
                    </div>
                </div>
                """.format(surname, last_name, identifier.upper())
        if status:
            result += """<p class='text-success'><b> {} </b></p>""".format(message)
            result += """<p class='text-success'><b> {} {} </b></p>""".format(today, time)
        else:
            result += """<p class='text-danger'><b> {} </b></p>""".format(message)
    else:
        result += """<p class='text-danger'><b> {} </b></p>""".format(message)
        result += """<p class='text-danger'><b> {} {} </b></p>""".format(today, time)
    return HttpResponse(result)


def check_general_attendance_select_date(request):
    if request.method == 'POST':
        selected_date = request.POST.get('date')
        return redirect(reverse('check_general_attendance', kwargs={'date': selected_date}))

    return render(request, 'attendance/check_general_attendance_select_date.html')


def check_general_attendance(request, date):
    selected_date = datetime.strptime(date, "%Y-%m-%d")
    if selected_date > datetime.now():
        messages.error(request, 'Cannot Check attendance For a Future Date')
        return redirect(reverse('check_general_attendance_select_date'))
    school_setting = SchoolGeneralInfoModel.objects.first()
    user_type = request.user.profile.type
    if school_setting.separate_school_section:
        setting = AcademicSettingModel.objects.filter(type=user_type).first()
        academic_setting = SchoolAcademicInfoModel.objects.filter(type=user_type).first()
    else:
        setting = AcademicSettingModel.objects.first()
        academic_setting = SchoolAcademicInfoModel.objects.first()
    selected_day = selected_date.strftime("%A")
    day_is_valid = False
    all_days = setting.active_days.all()
    for day in all_days:
        if day.name.lower() == selected_day.lower():
            day_is_valid = True
            break
    if not day_is_valid:
        messages.error(request, 'Cannot Check attendance on {} as school is not active'.format(selected_day.title()))
        return redirect(reverse('check_general_attendance_select_date'))

    if school_setting.separate_school_section:
        attendance_list = StudentAttendanceModel.objects.filter(type=user_type)
        staff_attendance_list = StaffAttendanceModel.objects.filter(type=user_type)
        students = StudentsModel.objects.filter(type=user_type).count()
        staff = StaffModel.objects.filter(type=user_type).count()
    else:
        attendance_list = StudentAttendanceModel.objects.all()
        staff_attendance_list = StaffAttendanceModel.objects.all()
        students = StudentsModel.objects.all().count()
        staff = StaffModel.objects.count()
    total_attendance, total_staff_attendance = 0, 0
    selected_date_str = selected_date.strftime("%d-%m-%y")

    session, term = None, None
    for key, attendance in enumerate(attendance_list):
        if key == 1:
            session = attendance.sesskion
            term = attendance.term
        if selected_date_str in attendance.attendance.keys():
            total_attendance += 1

    for key, attendance in enumerate(staff_attendance_list):
        if key == 1 and not session:
            session = attendance.sesskion
            term = attendance.term

        if selected_date_str in attendance.attendance.keys():
            total_staff_attendance += 1
    session = session if session else academic_setting.session
    term = term if term else academic_setting.term

    context = {
        'selected_date': selected_date,
        'total_student': students,
        'total_attendance': total_attendance,
        'absent_student': students - total_attendance,
        'percentage_student': round((total_attendance/students) * 100) if students else 0,

        'total_staff': staff,
        'total_staff_attendance': total_staff_attendance,
        'absent_staff': staff - total_staff_attendance,
        'percentage_staff': round((total_staff_attendance / staff) * 100) if staff else 0,
        'session': session,
        'term': term
    }
    return render(request, 'attendance/check_general_attendance.html', context)


def daily_attendance_select_class(request):
    if request.method == 'POST':
        pk = request.POST.get('class')
        date = request.POST.get('date')
        return redirect(reverse('class_attendance', kwargs={'pk': pk, 'date': date}))

    staff = request.user.profile.staff
    school_setting = SchoolGeneralInfoModel.objects.first()
    user_type = request.user.profile.type
    if school_setting.separate_school_section:
        class_list = ClassSectionInfoModel.objects.filter(Q(form_teacher=staff) | Q(assistant_form_teacher=staff)).filter(type=user_type)
    else:
        class_list = ClassSectionInfoModel.objects.filter(Q(form_teacher=staff) | Q(assistant_form_teacher=staff))
    context = {
        'class_list': class_list
    }
    return render(request, 'attendance/class_attendance_select.html', context)


def daily_class_attendance(request, pk, date):
    selected_date = datetime.strptime(date, "%Y-%m-%d")
    if selected_date > datetime.now():
        messages.error(request, 'Cannot Take attendance For a Future Date')
        return redirect(reverse('class_attendance_select_class'))
    school_setting = SchoolGeneralInfoModel.objects.first()
    type = request.user.profile.type
    if school_setting.separate_school_section:
        academic_setting = SchoolAcademicInfoModel.objects.filter(type=type).first()
        setting = AcademicSettingModel.objects.filter(type=type).first()
    else:
        academic_setting = SchoolAcademicInfoModel.objects.first()
        setting = AcademicSettingModel.objects.first()
    selected_day = selected_date.strftime("%A")
    day_is_valid = False
    all_days = setting.active_days.all()
    for day in all_days:
        if day.name.lower() == selected_day.lower():
            day_is_valid = True
            break
    if not day_is_valid:
        messages.error(request, 'Cannot Take attendance on {} as school is not active'.format(selected_day.title()))
        return redirect(reverse('class_attendance_select_class'))

    if request.method == 'POST':
        student_list = request.POST.getlist('students[]')
        if len(student_list) == 0:
            messages.error(request, 'No Student in Selected Class')
            return redirect(reverse('class_attendance_select_class'))

        term = academic_setting.term
        session = academic_setting.session
        total, present, late, absent = 0, 0, 0, 0

        selected_date_object = selected_date
        selected_date = selected_date.strftime("%d-%m-%y")

        for student_id in student_list:
            total_attendance, present_attendance, late_attendance, absent_attendance = 0, 0, 0, 0
            student = StudentsModel.objects.get(pk=student_id)
            att_id = 'attendance' + str(student.id)
            attendance_status = request.POST.get(att_id)

            student_attendance = StudentClassAttendanceModel.objects.filter(
                session=session, term=term, student_class=student.student_class,
                class_section=student.class_section, student=student).first()

            initial_status = None

            if student_attendance:
                if selected_date in student_attendance.attendance:
                    total += 1
                    initial_status = student_attendance.attendance[selected_date]
                    if initial_status == 'present':
                        student_attendance.present_attendance -= 1
                    if initial_status == 'late':
                        student_attendance.late_attendance -= 1
                    if initial_status == 'absent':
                        student_attendance.absent_attendance -= 1
                    student_attendance.attendance[selected_date] = attendance_status
                    if attendance_status == 'present':
                        student_attendance.present_attendance += 1
                        present += 1
                        student_attendance.last_present_date = selected_date_object
                    if attendance_status == 'late':
                        student_attendance.late_attendance += 1
                        late += 1
                    if attendance_status == 'absent':
                        student_attendance.absent_attendance += 1
                        absent += 1
                else:
                    student_attendance.total_attendance += 1
                    total += 1
                    student_attendance.attendance[selected_date] = attendance_status
                    if attendance_status == 'present':
                        student_attendance.present_attendance += 1
                        present_attendance += 1
                        student_attendance.last_present_date = selected_date_object
                        present += 1
                    if attendance_status == 'late':
                        student_attendance.late_attendance += 1
                        late_attendance += 1
                        late += 1
                    if attendance_status == 'absent':
                        student_attendance.absent_attendance += 1
                        absent_attendance += 1
                        absent += 1

                student_attendance.last_attendance_date = selected_date_object
                student_attendance.save()
            else:
                attendance = {
                    selected_date: attendance_status
                }
                total += 1
                if attendance_status == 'present':
                    total_attendance, present_attendance, late_attendance, absent_attendance = 1, 1, 0, 0
                    present += 1
                if attendance_status == 'late':
                    total_attendance, late_attendance, present_attendance, absent_attendance = 1, 1, 0, 0
                    late += 1
                if attendance_status == 'absent':
                    total_attendance, absent_attendance, present_attendance, late_attendance = 1, 1, 0, 0
                    absent += 1

                student_attendance = StudentClassAttendanceModel.objects.create(
                    session=session, term=term, student_class=student.student_class,
                    class_section=student.class_section, student=student, type=type, attendance=attendance,
                    total_attendance=total_attendance, present_attendance=present_attendance,
                    absent_attendance=absent_attendance, late_attendance=late_attendance,
                    last_attendance_date=selected_date_object, last_present_date=selected_date_object)
                student_attendance.save()

            student_attendance_record = StudentClassAttendanceRecordModel.objects.filter(session=session,
                                        term=term, date=selected_date_object, type=type).first()
            if student_attendance_record:
                if initial_status:
                    student_attendance_record.total_attendance -= 1
                if initial_status == 'present':
                    student_attendance_record.present_attendance -= 1
                if initial_status == 'late':
                    student_attendance_record.late_attendance -= 1
                if initial_status == 'absent':
                    student_attendance_record.absent_attendance -= 1

                if attendance_status == 'present':
                    student_attendance_record.present_attendance += 1
                if attendance_status == 'late':
                    student_attendance_record.late_attendance += 1
                if attendance_status == 'absent':
                    student_attendance_record.absent_attendance += 1
                student_attendance_record.total_attendance += 1
                student_attendance_record.save()
            else:
                student_attendance_record = StudentClassAttendanceRecordModel.objects.create(session=session, term=term,
                    date=selected_date_object, total_attendance=1, present_attendance=present_attendance,
                    late_attendance=late_attendance, absent_attendance=absent_attendance, type=type)
                student_attendance_record.save()

        messages.success(request, "Attendance Saved, Total Students: {} Present: {}, Late: {}, Absent: {}".format(
            total, present, late, absent
        ))
        return redirect(reverse('check_class_attendance', kwargs={'pk': pk, 'date': date}))

    staff = request.user.profile.staff
    try:
        class_info = ClassSectionInfoModel.objects.get(pk=pk)
    except ObjectDoesNotExist:
        messages.error(request, 'Error Selecting Class Students, Try Later')
        return redirect(reverse('class_attendance_select_class'))

    if class_info.form_teacher != staff and class_info.assistant_form_teacher != staff:
        messages.error(request, 'can only take attendance for your class')
        return redirect(reverse('class_attendance_select_class'))

    student_list = StudentsModel.objects.filter(student_class=class_info.student_class,
                                                class_section=class_info.section).order_by('class_number')
    context = {
        'student_list': student_list,
        'class_info': class_info,
        'date': selected_date
    }
    return render(request, 'attendance/class_attendance.html', context)


def check_attendance_select_class(request):
    if request.method == 'POST':
        pk = request.POST.get('class')
        date = request.POST.get('date')
        return redirect(reverse('check_class_attendance', kwargs={'pk': pk, 'date': date}))
    staff = request.user.profile.staff
    class_list = ClassSectionInfoModel.objects.filter(Q(form_teacher=staff) | Q(assistant_form_teacher=staff))
    context = {
        'class_list': class_list
    }
    return render(request, 'attendance/check_class_attendance_select.html', context)


def check_class_attendance(request, pk, date):
    selected_date = datetime.strptime(date, "%Y-%m-%d")
    if selected_date > datetime.now():
        messages.error(request, 'Cannot Check attendance For a Future Date')
        return redirect(reverse('check_class_attendance_select_class'))
    school_setting = SchoolGeneralInfoModel.objects.first()
    type = request.user.profile.type
    if school_setting.separate_school_section:
        academic_setting = SchoolAcademicInfoModel.objects.filter(type=type).first()
        setting = AcademicSettingModel.objects.filter(type=type).first()
    else:
        academic_setting = SchoolAcademicInfoModel.objects.first()
        setting = AcademicSettingModel.objects.first()
    selected_day = selected_date.strftime("%A")
    day_is_valid = False
    all_days = setting.active_days.all()
    for day in all_days:
        if day.name.lower() == selected_day.lower():
            day_is_valid = True
            break
    if not day_is_valid:
        messages.error(request, 'Cannot Check attendance on {} as school is not active'.format(selected_day.title()))
        return redirect(reverse('check_class_attendance_select_class'))

    staff = request.user.profile.staff
    try:
        class_info = ClassSectionInfoModel.objects.get(pk=pk)
    except ObjectDoesNotExist:
        messages.error(request, 'Error Selecting Class Students, Try Later')
        return redirect(reverse('class_attendance_select_class'))

    if class_info.form_teacher != staff and class_info.assistant_form_teacher != staff and not request.user.is_superuser:
        messages.error(request, 'can only check attendance for your class')
        return redirect(reverse('check_class_attendance_select_class'))
    student_list = StudentsModel.objects.filter(student_class=class_info.student_class,
                                                class_section=class_info.section).order_by('surname')
    total_attendance, present_attendance, late_attendance, absent_attendance = 0, 0, 0, 0
    for student in student_list:
        student_attendance = check_student_attendance(student, selected_date)
        if student_attendance:
            total_attendance += 1
            if student_attendance == 'present':
                present_attendance += 1
            elif student_attendance == 'late':
                late_attendance += 1
            elif student_attendance == 'absent':
                absent_attendance += 1
    context = {
        'student_list': student_list,
        'class_info': class_info,
        'date': selected_date,
        'total_attendance': total_attendance,
        'present_attendance': present_attendance,
        'late_attendance': late_attendance,
        'absent_attendance': absent_attendance
    }
    return render(request, 'attendance/check_class_attendance.html', context)
