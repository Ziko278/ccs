from django.db import models, transaction
from academic.models import ClassesModel, ClassSectionModel, SubjectGroupModel
from django.contrib.auth.models import User, Group
from user_management.models import UserProfileModel
# --- UPDATED IMPORT TO GET THE NEW TERM MODEL ---
from school_setting.models import SchoolSettingModel, SessionModel, SchoolAcademicInfoModel, SchoolGeneralInfoModel, TermModel
import random
from io import BytesIO
from django.core.files.base import ContentFile
from django.apps import apps
from admin_dashboard.storage_backends import MediaStorage


class UtilityModel(models.Model):
    """
    Represents a school utility/service that students can subscribe to.
    Examples: Boarding, Transport, After-School Care, etc.
    """
    name = models.CharField(max_length=100, unique=True,
                            help_text="Name of the utility (e.g., Boarding, Transport)")
    code = models.CharField(max_length=50, unique=True,
                            help_text="Unique code for this utility (e.g., BRD, TRN)")
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Utility"
        verbose_name_plural = "Utilities"

    def __str__(self):
        return self.name.upper()


class ParentsModel(models.Model):
    """   """
    TITLE = (
        ('MR', 'MR'), ('MRS', 'MRS'), ('MISS', 'MISS'), ('MS', 'MS'), ('MALLAM', 'MALLAM'), ('DOC', 'DOC'),
        ('BARR', 'BARR'), ('PST', 'PST'), ('PROF', 'PROF'),  ('ENGR', 'ENGR'), ('ALHAJI', 'ALHAJI'), ('HAJIYAH', 'HAJIYAH')
    )
    title = models.CharField(max_length=10, choices=TITLE)
    surname = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50)
    excel_pid = models.IntegerField(blank=True, null=True)

    image = models.FileField(blank=True, null=True, storage=MediaStorage(), upload_to='images/parent_images')
    residential_address = models.CharField(max_length=200, null=True, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)

    occupation = models.CharField(max_length=100, null=True, blank=True)
    office_address = models.CharField(max_length=200, null=True, blank=True)
    office_mobile = models.CharField(max_length=20, null=True, blank=True)
    parent_id = models.CharField(max_length=50, blank=True, unique=True)

    state = models.CharField(max_length=100, null=True, blank=True)
    lga = models.CharField(max_length=100, null=True, blank=True)
    RELIGION = (
        ('christianity', 'CHRISTIANITY'), ('islam', 'ISLAM'), ('others', 'OTHERS')
    )
    religion = models.CharField(max_length=30, choices=RELIGION, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    GENDER = (
        ('MALE', 'MALE'), ('FEMALE', 'FEMALE')
    )
    gender = models.CharField(max_length=10, choices=GENDER)
    MARITAL_STATUS = (
        ('single', 'SINGLE'), ('married', 'MARRIED'), ('widowed', 'WIDOWED'), ('separated', 'SEPARATED')
    )
    marital_status = models.CharField(max_length=30, choices=MARITAL_STATUS, null=True, blank=True)

    registration_date = models.DateTimeField(auto_now_add=True, blank=True)
    status = models.CharField(max_length=15, blank=True, default='active')
    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='parent_updated_by')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        if self.middle_name:
            return self.title.title() + ' ' + self.surname.title() + ' ' + self.middle_name.title() + ' ' + self.last_name.title()
        else:
            return self.title.title() + ' ' + self.surname.title() + ' ' + self.last_name.title()

    def number_of_ward(self):
        return StudentsModel.objects.filter(parent=self).count()

    def active_wards_count(self):
        return StudentsModel.objects.filter(parent=self, status='active').count()

    def save(self, *args, **kwargs):
        setting = SchoolGeneralInfoModel.objects.first()
        if setting.school_type == 'mix' and setting.separate_school_section:
            parent_setting = StudentSettingModel.objects.filter(type=self.type).first()
        else:
            parent_setting = StudentSettingModel.objects.first()

        if parent_setting.auto_generate_parent_id and not self.parent_id:
            if setting.school_type == 'mix' and setting.separate_school_section:
                last_parent = ParentIDGeneratorModel.objects.filter(type=self.type).last()
            else:
                last_parent = ParentIDGeneratorModel.objects.filter().last()
            if last_parent:
                parent_id = str(int(last_parent.last_id) + 1)
            else:
                parent_id = str(1)
            while True:
                gen_id = parent_id
                if setting.school_type == 'mix':
                    parent_id = 'p' + self.type[0] + '-' + parent_id.rjust(7, '0')
                else:
                    parent_id = 'p' + parent_id.rjust(8, '0')
                parent_exist = ParentsModel.objects.filter(parent_id=parent_id).first()
                if not parent_exist:
                    break
                else:
                    parent_id = str(int(gen_id) + 1)
            self.parent_id = parent_id

            generate_id = ParentIDGeneratorModel.objects.create(last_id=gen_id, last_parent_id=self.parent_id,
                                                                type=self.type)
            generate_id.save()

        else:
            user_profile = UserProfileModel.objects.get(parent_id=self.id)
            user = user_profile.user
            if self.email:
                user.email = self.email
            user.save()

        super(ParentsModel, self).save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['parent_id', 'type'],
                name='unique_parent_id'
            )
        ]


class StudentsModel(models.Model):
    """"""
    surname = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50)
    registration_number = models.CharField(max_length=50, blank=True, null=True)
    class_number = models.IntegerField(blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    subject_group = models.ForeignKey(SubjectGroupModel, null=True, blank=True, on_delete=models.CASCADE)
    GENDER = (
        ('MALE', 'MALE'), ('FEMALE', 'FEMALE')
    )
    gender = models.CharField(max_length=10, choices=GENDER)
    state = models.CharField(max_length=100, null=True, blank=True)
    lga = models.CharField(max_length=100, null=True, blank=True)
    utilities = models.ManyToManyField(
        UtilityModel,
        related_name='students',
        blank=True,
        help_text="Services the student is subscribed to (e.g., Transport, Boarding)"
    )
    RELIGION = (
        ('christianity', 'CHRISTIANITY'), ('islam', 'ISLAM'), ('others', 'OTHERS')
    )
    religion = models.CharField(max_length=30, choices=RELIGION, null=True, blank=True)
    image = models.FileField(blank=True, null=True, storage=MediaStorage(), upload_to='images/student_images')
    mobile = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True, unique=True)
    password = models.CharField(max_length=100, null=True, blank=True)
    BG = (
        ('a+', 'A+'), ('a-', 'A-'), ('b+', 'B+'), ('b-', 'B-'), ('ab+', 'AB+'), ('ab-', 'AB-'), ('o+', 'O+'),
        ('o-', 'O-'),
    )
    age = models.IntegerField(null=True, blank=True)
    student_class = models.ForeignKey(ClassesModel, null=True, on_delete=models.CASCADE)
    class_section = models.ForeignKey(ClassSectionModel, null=True, on_delete=models.CASCADE)
    parent = models.ForeignKey(ParentsModel, on_delete=models.PROTECT, related_name='wards')

    RELATIONSHIP_WITH_PARENT = (
        ('father', 'FATHER'), ('mother', 'MOTHER'), ('sister', 'SISTER'), ('brother', 'BROTHER'), ('uncle', 'UNCLE'),
        ('aunty', 'AUNTY'), ('pastor', 'PASTOR'), ('others', 'OTHERS')
    )
    relationship_with_parent = models.CharField(max_length=20, choices=RELATIONSHIP_WITH_PARENT)

    registration_date = models.DateField(auto_now_add=True, blank=True, null=True)
    status = models.CharField(max_length=15, blank=True, default='active')
    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    is_new = models.BooleanField(default=False, blank=True)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='student_updated_by')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        if self.middle_name:
            return self.surname + ' ' + self.middle_name + ' ' + self.last_name
        else:
            return self.surname + ' ' + self.last_name

    def save(self, *args, **kwargs):
        with transaction.atomic():  # Ensuring atomicity for the entire save operation
            # Fetch school settings
            setting = SchoolGeneralInfoModel.objects.first()
            student_setting = (
                StudentSettingModel.objects.filter(type=self.type).first()
                if setting.school_type == 'mix' and setting.separate_school_section
                else StudentSettingModel.objects.first()
            )
            academic_info = (
                SchoolAcademicInfoModel.objects.filter(type=self.type).first()
                if setting.school_type == 'mix' and setting.separate_school_section
                else SchoolAcademicInfoModel.objects.first()
            )
            session = str(academic_info.session.start_year)[-2:]  # Get last two digits of the session start year

            # Generate registration number if required
            if student_setting.auto_generate_student_id and not self.registration_number:
                # Fetch the last student ID for the session and type
                last_student = (
                    StudentIDGeneratorModel.objects.filter(session=session)
                    .filter(type=self.type if setting.school_type == 'mix' else None)
                    .last()
                )
                student_id = str(int(last_student.last_id) + 1) if last_student else "1"

                # Loop to ensure unique registration number
                while True:
                    gen_id = student_id
                    prefix = 'ccs'
                    registration_number = f"{prefix}/{session}/{gen_id.rjust(4, '0')}"
                    if not StudentsModel.objects.filter(registration_number=registration_number).exists():
                        break
                    student_id = str(int(gen_id) + 1)

                # Save the last ID to the generator model
                StudentIDGeneratorModel.objects.create(
                    last_id=gen_id, session=academic_info.session, last_student_id=registration_number, type=self.type
                )
                self.registration_number = registration_number

            # Handle user account creation
            if self.id:
                try:
                    # Check if a user profile exists for the student
                    user_profile = UserProfileModel.objects.get(student_id=self.id)
                    user = user_profile.user
                    if self.email:
                        user.email = self.email  # Update email if provided
                    user.save()  # Save updated user details
                except UserProfileModel.DoesNotExist:
                    pass

            # Save the student instance
        super().save(*args, **kwargs)

    def no_in_class(self):
        return StudentsModel.objects.filter(student_class=self.student_class, class_section=self.class_section).count()


class StudentAcademicRecordModel(models.Model):
    student = models.OneToOneField(StudentsModel, on_delete=models.CASCADE, related_name='student_academic_record')
    entry_class = models.ForeignKey(ClassesModel, on_delete=models.SET_NULL, null=True)
    entry_class_section = models.ForeignKey(ClassSectionModel, on_delete=models.SET_NULL, null=True)
    entry_session = models.ForeignKey(SessionModel, on_delete=models.SET_NULL, null=True, related_name='entry_session')
    # --- THIS FIELD HAS BEEN UPDATED ---
    entry_term = models.ForeignKey(TermModel, on_delete=models.SET_NULL, null=True, related_name='entry_records')
    previous_classes = models.JSONField(null=True, blank=True)
    attendance_record = models.JSONField(null=True, blank=True)
    date_of_graduation = models.DateField(null=True)
    session_of_graduation = models.ForeignKey(SessionModel, on_delete=models.SET_NULL, null=True)
    exit_mode = models.CharField(max_length=20, null=True)
    session_of_departure = models.ForeignKey(SessionModel, on_delete=models.SET_NULL, related_name='departure',
                                             null=True)
    # --- THIS FIELD HAS BEEN UPDATED ---
    term_of_departure = models.ForeignKey(TermModel, on_delete=models.SET_NULL, null=True, related_name='departure_records')
    entry_age = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return "{} {}".format(self.student.surname.title(), self.student.last_name.title())


class StudentIDGeneratorModel(models.Model):
    last_id = models.IntegerField()
    last_student_id = models.CharField(max_length=100, null=True, blank=True)
    session = models.ForeignKey(SessionModel, on_delete=models.CASCADE, null=True, blank=True)
    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True)


class StudentWalletModel(models.Model):
    student = models.OneToOneField(StudentsModel, on_delete=models.CASCADE, related_name='student_wallet')
    # Use DecimalField for financial accuracy
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    debt = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.student}'s Wallet"


class ParentIDGeneratorModel(models.Model):
    last_id = models.IntegerField()
    last_parent_id = models.CharField(max_length=100, null=True, blank=True)
    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True)


class StudentSettingModel(models.Model):
    auto_generate_student_id = models.BooleanField(default=True)
    auto_generate_parent_id = models.BooleanField(default=True)
    student_id_prefix = models.CharField(max_length=5, blank=True, null=True, default='')
    TYPE = (('pri', 'PRIMARY'), ('sec', 'SECONDARY'))
    type = models.CharField(max_length=10, choices=TYPE, blank=True)

