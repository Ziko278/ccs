from django.db import models
from django.contrib.auth.models import User
from admin_dashboard.storage_backends import MediaStorage


class SessionModel(models.Model):
    start_year = models.IntegerField()
    end_year = models.IntegerField()
    SEPERATOR = (('-', '-'), ('/', '/'))
    seperator = models.CharField(max_length=1, choices=SEPERATOR)
    SessionStatus = (
        ('a', 'ACTIVE'), ('p', 'PAST'), ('n', 'NEXT')
    )
    status = models.CharField(max_length=1, choices=SessionStatus)
    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY'), ('mix', 'MIXED')
    )
    type = models.CharField(max_length=200, choices=TYPE)

    def __str__(self):
        return str(round(self.start_year)) + self.seperator + str(round(self.end_year))


class TermModel(models.Model):
    name = models.CharField(max_length=20, unique=True)
    order = models.PositiveIntegerField(unique=True, help_text="Order for sorting terms (e.g., 1 for 1st Term).")
    is_promotion_term = models.BooleanField(default=False, help_text="Set to True if this is the final term before promotion.")

    class Meta:
        ordering = ['order']
        verbose_name = "Term"
        verbose_name_plural = "Terms"

    def __str__(self):
        return self.name

    def __str__(self):
        return self.name


class SchoolAcademicInfoModel(models.Model):
    session = models.ForeignKey(SessionModel, on_delete=models.CASCADE)
    # --- THIS FIELD HAS BEEN UPDATED ---
    term = models.ForeignKey(TermModel, on_delete=models.SET_NULL, null=True)
    next_resumption_date = models.DateField(null=True, blank=True)
    closing_date = models.DateField(null=True, blank=True)
    current_resumption_date = models.DateField(null=True, blank=True)
    no_of_students = models.FloatField(null=True, blank=True)
    no_of_staff = models.FloatField(null=True, blank=True)
    no_of_parents = models.FloatField(null=True, blank=True)
    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY'), ('mix', 'MIXED')
    )
    type = models.CharField(max_length=200, choices=TYPE)


class SchoolGeneralInfoModel(models.Model):
    name = models.CharField(max_length=250)
    short_name = models.CharField(max_length=50)
    website = models.CharField(max_length=200)
    motto = models.CharField(max_length=250)
    SCHOOL_TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY'), ('mix', 'MIXED')
    )
    school_type = models.CharField(max_length=200, choices=SCHOOL_TYPE)
    logo = models.FileField(upload_to='images/logo', storage=MediaStorage(), blank=True)
    mobile_1 = models.CharField(max_length=20)
    mobile_2 = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    separate_school_section = models.BooleanField(default=True)
    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY'), ('mix', 'MIXED')
    )
    type = models.CharField(max_length=200, choices=TYPE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.short_name.upper()


class SchoolSettingModel(models.Model):
    general_info = models.ForeignKey(SchoolGeneralInfoModel, on_delete=models.CASCADE)
    academic_info = models.ForeignKey(SchoolAcademicInfoModel, on_delete=models.SET_NULL, null=True, blank=True)
