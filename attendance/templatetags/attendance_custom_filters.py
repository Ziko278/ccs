from django import template
from student.models import StudentsModel
from datetime import date, timedelta
from attendance.models import StudentClassAttendanceModel
from django.db.models import Sum
from school_setting.models import SchoolGeneralInfoModel, SchoolAcademicInfoModel

register = template.Library()


@register.filter
def check_student_attendance(student, selected_date):
    selected_date = selected_date.strftime("%d-%m-%y")
    user_type = student.type
    school_setting = SchoolGeneralInfoModel.objects.first()
    if school_setting.separate_school_section:
        academic_info = SchoolAcademicInfoModel.objects.filter(type=user_type).first()
    else:
        academic_info = SchoolAcademicInfoModel.objects.first()

    session = academic_info.session
    term = academic_info.term

    student_attendance = StudentClassAttendanceModel.objects.filter(student=student, session=session, term=term).first()

    if not student_attendance:
        return False

    if selected_date not in student_attendance.attendance:
        return False
    attendance = student_attendance.attendance[selected_date]
    if not attendance:
        return False
    return attendance





