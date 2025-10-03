from django.db import models
from django.contrib.auth.models import User
from school_setting.models import SchoolGeneralInfoModel, SchoolAcademicInfoModel


class UserProfileModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    staff = models.OneToOneField('human_resource.StaffModel', on_delete=models.CASCADE, null=True, blank=True,
                                 related_name='account')
    parent = models.OneToOneField('student.ParentsModel', on_delete=models.CASCADE, null=True, blank=True,
                                  related_name='parent_account')
    student = models.OneToOneField('student.StudentsModel', on_delete=models.CASCADE, null=True, blank=True,
                                   related_name='student_account')
    reference_id = models.IntegerField()
    reference = models.CharField(max_length=20)
    default_password = models.CharField(max_length=100)
    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY'), ('mix', 'GENERAL')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True, null=True)

    def __str__(self):
        return self.user.username
