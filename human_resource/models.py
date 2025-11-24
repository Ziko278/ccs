from django.db import models
from django.contrib.auth.models import User, Group
from school_setting.models import SchoolSettingModel, SchoolGeneralInfoModel
from user_management.models import UserProfileModel
from io import BytesIO
from django.apps import apps
from admin_dashboard.storage_backends import MediaStorage


class DepartmentModel(models.Model):
    """  """
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    DEPT_TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY')
    )
    type = models.CharField(max_length=10, choices=DEPT_TYPE, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='department_updated_by')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'type'],
                name='unique_dept_name_type_combo'
            )
        ]

    def __str__(self):
        return self.name.upper()

    def number_of_staff(self):
        return StaffModel.objects.filter(department=self).count()

    def save(self, *args, **kwargs):

        super(DepartmentModel, self).save(*args, **kwargs)


class PositionModel(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(DepartmentModel, on_delete=models.CASCADE, related_name='positions')
    description = models.TextField(null=True, blank=True)
    POSITION_TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY')
    )
    type = models.CharField(max_length=10, choices=POSITION_TYPE, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='position_updated_by')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'department', 'type'],
                name='unique_dept_name_and_dept_and_type_combo'
            )
        ]

    def __str__(self):
        return self.name.upper() + ' (' + self.department.name.upper() + ')'

    def number_of_staff(self):
        return StaffModel.objects.filter(position=self).count()


class StaffModel(models.Model):
    """"""
    TITLE = (
        ('MR', 'MR'), ('MRS', 'MRS'), ('MISS', 'MISS'), ('MS', 'MS'), ('MALLAM', 'MALLAM'), ('DR', 'DR'),
        ('BARR', 'BARR'), ('PST', 'PST'), ('PROF', 'PROF'), ('ENGR', 'ENGR'), ('ALHAJI', 'ALHAJI'),
        ('HAJIYAH', 'HAJIYAH')
    )
    title = models.CharField(max_length=10, choices=TITLE, default='MR')
    surname = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, null=True, blank=True, default='')
    last_name = models.CharField(max_length=50)

    image = models.FileField(upload_to='images/staff_images', storage=MediaStorage(), blank=True, null=True)
    residential_address = models.CharField(max_length=200, blank=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True, unique=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    lga = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    GENDER = (
        ('MALE', 'MALE'), ('FEMALE', 'FEMALE')
    )
    gender = models.CharField(max_length=10, choices=GENDER)
    MARITAL_STATUS = (
        ('single', 'SINGLE'), ('married', 'MARRIED'), ('widowed', 'WIDOWED'), ('separated', 'SEPARATED')
    )
    marital_status = models.CharField(max_length=30, choices=MARITAL_STATUS, null=True, blank=True)

    RELIGION = (
        ('christianity', 'CHRISTIANITY'), ('islam', 'ISLAM'), ('others', 'OTHERS')
    )
    religion = models.CharField(max_length=30, choices=RELIGION, null=True, blank=True)

    department = models.ForeignKey(DepartmentModel, on_delete=models.CASCADE, related_name='department_staffs')
    position = models.ForeignKey(PositionModel, on_delete=models.CASCADE, related_name='position_staffs')
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    staff_id = models.CharField(max_length=100, blank=True, null=True)
    employment_date = models.DateField(blank=True, null=True)
    cv = models.FileField(upload_to='staff/cv', storage=MediaStorage(), null=True, blank=True)
    signature = models.ImageField(upload_to='signatures/', blank=True, null=True)
    salary = models.BigIntegerField(blank=True, null=True, default=0)
    bank_name = models.CharField(max_length=100, null=True, blank=True)
    account_name = models.CharField(max_length=100, null=True, blank=True)
    account_number = models.CharField(max_length=50, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)

    status = models.CharField(max_length=30, blank=True, default='active')
    can_teach = models.BooleanField(default=True, blank=True)
    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='staff_updated_by')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        if self.middle_name:
            return f"{self.title} {self.surname} {self.middle_name} {self.last_name}"
        else:
            return f"{self.title} {self.surname} {self.last_name}"

    def is_head_teacher(self):
        setting = SchoolSettingModel.objects.first()
        AcademicModel = apps.get_model('academic', 'AcademicSettingModel')
        if setting.general_info.school_type == 'mix' and setting.general_info.separate_school_section:
            academic_setting = AcademicModel.objects.filter(type=self.type).first()
        else:
            academic_setting = AcademicModel.objects.first()
        if academic_setting:
            if academic_setting.head_teacher == self:
                return True
        return False

    def save(self, *args, **kwargs):
        setting = SchoolGeneralInfoModel.objects.first()
        if setting.school_type == 'mix' and setting.separate_school_section:
            staff_setting = HRSettingModel.objects.filter(type=self.type).first()
        else:
            staff_setting = HRSettingModel.objects.first()

        if staff_setting.auto_generate_staff_id and not self.staff_id:
            if setting.school_type == 'mix' and setting.separate_school_section:
                last_staff = StaffIDGeneratorModel.objects.filter(type=self.type).last()
            else:
                last_staff = StaffIDGeneratorModel.objects.filter().last()
            if last_staff:
                staff_id = str(int(last_staff.last_id) + 1)
            else:
                staff_id = str(1)
            while True:
                gen_id = staff_id
                prefix = staff_setting.staff_id_prefix if staff_setting.staff_id_prefix else ''
                if setting.school_type == 'mix':
                    staff_id = f"{prefix}{self.type[0]}s-{staff_id.rjust(7, '0')}"
                else:
                    staff_id = f"{prefix}s-{staff_id.rjust(7, '0')}"

                staff_exist = StaffModel.objects.filter(staff_id=staff_id).first()
                if not staff_exist:
                    break
                else:
                    staff_id = str(int(gen_id) + 1)
            self.staff_id = staff_id

            generate_id = StaffIDGeneratorModel.objects.create(last_id=gen_id, last_staff_id=self.staff_id,
                                                               type=self.type)
            generate_id.save()

        else:
            user_profile = UserProfileModel.objects.get(staff_id=self.id)
            user = user_profile.user
            if self.email:
                user.email = self.email
            user.save()

            self.group.user_set.add(user)

        super(StaffModel, self).save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['staff_id', 'type'],
                name='unique_staff_id'
            )
        ]

    def subject_list(self):
        SubjectsModel = apps.get_model('academic', 'SubjectsModel')
        ClassSectionSubjectTeacherModel = apps.get_model('academic', 'ClassSectionSubjectTeacherModel')
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            if self.user.is_superuser:
                subject_list = SubjectsModel.objects.filter(type=self.request.user.profile.type)
            else:
                class_info_list = ClassSectionSubjectTeacherModel.objects.filter(teachers__in=[self.staff.id]).filter(
                    type=self.type)
                subject_list = []
                for class_info in class_info_list:
                    if class_info.subject not in subject_list:
                        subject_list.append(class_info.subject)

        else:
            if self.user.is_superuser:
                subject_list = SubjectsModel.objects.all()
            else:
                class_info_list = ClassSectionSubjectTeacherModel.objects.filter(teachers__in=[self.staff.id])
                subject_list = []
                for class_info in class_info_list:
                    if class_info.subject not in subject_list:
                        subject_list.append(class_info.subject)
        return subject_list


class StaffWalletModel(models.Model):
    staff = models.OneToOneField(StaffModel, on_delete=models.CASCADE, related_name='staff_wallet')
    # Use DecimalField for financial accuracy
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.staff}'s Wallet"


class StaffIDGeneratorModel(models.Model):
    last_id = models.IntegerField()
    last_staff_id = models.CharField(max_length=100, null=True, blank=True)
    STATUS = (
        ('s', 'SUCCESS'), ('f', 'FAIL')
    )
    status = models.CharField(max_length=10, choices=STATUS, blank=True, default='f')

    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True)


class HRSettingModel(models.Model):
    auto_generate_staff_id = models.BooleanField(default=True)
    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True)
    staff_id_prefix = models.CharField(max_length=5, blank=True, null=True, default='')


