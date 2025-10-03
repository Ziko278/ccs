from django.db import models
from django.contrib.auth.models import User
from school_setting.models import SchoolSettingModel, SessionModel
from student.models import StudentsModel, ParentsModel
from academic.models import *
from school_setting.models import SchoolAcademicInfoModel, SchoolGeneralInfoModel


class StudentAttendanceModel(models.Model):
    student = models.ForeignKey(StudentsModel, on_delete=models.CASCADE)
    session = models.ForeignKey(SessionModel, on_delete=models.CASCADE)
    student_class = models.ForeignKey(ClassesModel, on_delete=models.CASCADE)
    class_section = models.ForeignKey(ClassSectionModel, on_delete=models.SET_NULL, null=True)
    TERM = (
        ('1st term', '1st Term'), ('2nd term', '2ndTerm'), ('3rd term', '3rd Term')
    )
    term = models.CharField(max_length=20, choices=TERM)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    attendance = models.JSONField(blank=True, null=True)

    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY'), ('mix', 'GENERAL')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, blank=True)


class StudentClassAttendanceModel(models.Model):
    student = models.ForeignKey(StudentsModel, on_delete=models.CASCADE)
    student_class = models.ForeignKey(ClassesModel, on_delete=models.CASCADE)
    class_section = models.ForeignKey(ClassSectionModel, on_delete=models.SET_NULL, null=True)
    session = models.ForeignKey(SessionModel, on_delete=models.CASCADE)
    TERM = (
        ('1st term', '1st Term'), ('2nd term', '2ndTerm'), ('3rd term', '3rd Term')
    )
    term = models.CharField(max_length=20, choices=TERM)
    attendance = models.JSONField(blank=True, null=True)
    total_attendance = models.IntegerField(default=0)
    present_attendance = models.IntegerField(default=0)
    late_attendance = models.IntegerField(default=0)
    absent_attendance = models.IntegerField(default=0)
    last_attendance_date = models.DateField(null=True, blank=True)
    last_present_date = models.DateField(null=True, blank=True)

    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY'), ('mix', 'GENERAL')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True, null=True)


class StudentClassAttendanceRecordModel(models.Model):
    session = models.ForeignKey(SessionModel, on_delete=models.CASCADE)
    TERM = (
        ('1st term', '1st Term'), ('2nd term', '2ndTerm'), ('3rd term', '3rd Term')
    )
    term = models.CharField(max_length=20, choices=TERM)
    date = models.DateField()
    total_attendance = models.IntegerField(default=0)
    present_attendance = models.IntegerField(default=0)
    late_attendance = models.IntegerField(default=0)
    absent_attendance = models.IntegerField(default=0)
    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY'), ('mix', 'GENERAL')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True, null=True)


class StudentSubjectAttendanceModel(models.Model):
    student = models.ForeignKey(StudentsModel, on_delete=models.CASCADE)
    session = models.ForeignKey(SessionModel, on_delete=models.CASCADE)
    student_class = models.ForeignKey(ClassesModel, on_delete=models.CASCADE)
    class_section = models.ForeignKey(ClassSectionModel, on_delete=models.SET_NULL, null=True)
    subject = models.ForeignKey(SubjectsModel, on_delete=models.CASCADE)
    TERM = (
        ('1st term', '1st Term'), ('2nd term', '2ndTerm'), ('3rd term', '3rd Term')
    )
    term = models.CharField(max_length=20, choices=TERM)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    attendance = models.JSONField(blank=True, null=True)

    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY'), ('mix', 'GENERAL')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, blank=True)


class StaffAttendanceModel(models.Model):
    staff = models.ForeignKey(StaffModel, on_delete=models.CASCADE)
    session = models.ForeignKey(SessionModel, on_delete=models.CASCADE)
    TERM = (
        ('1st term', '1st Term'), ('2nd term', '2ndTerm'), ('3rd term', '3rd Term')
    )
    term = models.CharField(max_length=20, choices=TERM)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    attendance = models.JSONField(blank=True, null=True)

    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY'), ('mix', 'GENERAL')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, blank=True)


class HolidayModel(models.Model):
    session = models.ForeignKey(SessionModel, on_delete=models.CASCADE)
    TERM = (
        ('1st term', '1st Term'), ('2nd term', '2ndTerm'), ('3rd term', '3rd Term')
    )
    term = models.CharField(max_length=20, choices=TERM)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY'), ('mix', 'GENERAL')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, blank=True)


class VacationModel(models.Model):
    session = models.ForeignKey(SessionModel, on_delete=models.CASCADE)
    TERM = (
        ('1st term', '1st Term'), ('2nd term', '2ndTerm'), ('3rd term', '3rd Term')
    )
    term = models.CharField(max_length=20, choices=TERM)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY'), ('mix', 'GENERAL')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, blank=True)


class StaffClassAttendanceModel(models.Model):
    staff = models.ForeignKey(StaffModel, on_delete=models.CASCADE)
    session = models.ForeignKey(SessionModel, on_delete=models.CASCADE)
    TERM = (
        ('1st term', '1st Term'), ('2nd term', '2ndTerm'), ('3rd term', '3rd Term')
    )
    term = models.CharField(max_length=20, choices=TERM)
    student_class = models.ForeignKey(ClassesModel, on_delete=models.CASCADE)
    class_section = models.ForeignKey(ClassSectionModel, on_delete=models.SET_NULL, null=True)
    subject = models.ForeignKey(SubjectsModel, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    attendance = models.JSONField(blank=True, null=True)

    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY'), ('mix', 'GENERAL')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, blank=True)


class EventModel(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    ATTENDANT = (
        ('student', 'STUDENT'), ('parent', 'PARENT'), ('staff', 'STAFF'), ('all', 'ALL')
    )
    attendant = models.CharField(max_length=10, choices=ATTENDANT, blank=True, null=True)
    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY'), ('mix', 'GENERAL')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, blank=True)


class EventDayModel(models.Model):
    event = models.ForeignKey(EventModel, on_delete=models.CASCADE)
    day = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY'), ('mix', 'GENERAL')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, blank=True)


class EventAttendanceModel(models.Model):
    event = models.ForeignKey(EventDayModel, on_delete=models.CASCADE)
    staff = models.ManyToManyField(StaffModel, blank=True)
    student = models.ManyToManyField(StudentsModel, blank=True)
    parent = models.ManyToManyField(ParentsModel, blank=True)
    session = models.ForeignKey(SessionModel, on_delete=models.CASCADE)
    TERM = (
        ('1st term', '1st Term'), ('2nd term', '2ndTerm'), ('3rd term', '3rd Term')
    )
    term = models.CharField(max_length=20, choices=TERM)

    date = models.DateTimeField(auto_now_add=True, blank=True)
    attendance = models.JSONField(blank=True, null=True)

    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY'), ('mix', 'GENERAL')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, blank=True)


class AttendanceSettingModel(models.Model):
    use_barcode_attendance = models.BooleanField(default=True)
    use_id_attendance = models.BooleanField(default=False)
    use_name_attendance = models.BooleanField(default=False)
    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY'), ('mix', 'GENERAL')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, blank=True)