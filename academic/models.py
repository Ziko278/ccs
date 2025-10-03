from django.db import models
from django.contrib.auth.models import User
from human_resource.models import StaffModel
from school_setting.models import SchoolSettingModel
from django.apps import apps
from admin_dashboard.storage_backends import MediaStorage


class SubjectsModel(models.Model):
    """  """
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)

    SUBJECT_TYPE = (
        ('theory', 'THEORY'), ('practical', 'PRACTICAL'), ('combined', 'COMBINED')
    )
    subject_type = models.CharField(max_length=10, choices=SUBJECT_TYPE, default='theory')

    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY'), ('mix', 'GENERAL')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='subject_updated_by')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'type'],
                name='unique_subject_name_type_combo',
            )
        ]

    def __str__(self):
        return self.name.upper()

    def number_of_class(self):
        return ClassesModel.objects.filter(subjects__in=[self]).count()


class ClassSectionModel(models.Model):
    """  """
    name = models.CharField(max_length=100)
    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY'), ('mix', 'MIXED')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='class_section_updated_by')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'type'],
                name='unique_class_name_type_combo',
            )
        ]

    def __str__(self):
        return self.name.upper()

    def no_of_students(self):
        StudentsModel = apps.get_model('student', 'StudentsModel')
        return StudentsModel.objects.filter(class_section=self).count()

    def save(self, *args, **kwargs):

        super(ClassSectionModel, self).save(*args, **kwargs)


class ClassesModel(models.Model):
    """  """
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    section = models.ManyToManyField(ClassSectionModel, blank=True)
    RESULT_TYPE = (
        ('score', 'SCORE BASED'), ('text', 'TEXT BASED'), ('mix', 'MIX')
    )
    result_type = models.CharField(max_length=20, choices=RESULT_TYPE)

    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='class_updated_by')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'type'],
                name='unique_name_class_type_combo'
            )
        ]

    def __str__(self):
        return self.name.upper()

    def no_of_students(self):
        StudentsModel = apps.get_model('student', 'StudentsModel')
        return StudentsModel.objects.filter(student_class=self).count()

    def save(self, *args, **kwargs):

        super(ClassesModel, self).save(*args, **kwargs)


class HeadTeacherModel(models.Model):
    name = models.CharField(max_length=100)
    student_class = models.ManyToManyField(ClassesModel, blank=True)
    head_teacher = models.ForeignKey(StaffModel, on_delete=models.CASCADE)

    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True)


class PromotionClassModel(models.Model):
    student_class = models.ForeignKey(ClassesModel, on_delete=models.CASCADE)
    class_section = models.ForeignKey(ClassSectionModel, on_delete=models.CASCADE)
    promotion_class = models.ForeignKey(ClassesModel, on_delete=models.CASCADE, related_name='promotion_class')
    promotion_section = models.ForeignKey(ClassSectionModel, on_delete=models.CASCADE, related_name='promotion_section')
    is_graduation_class = models.BooleanField(default=False)

    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student_class', 'class_section', 'type'],
                name='unique_promotion_class_combo'
            )
        ]

    def __str__(self):
        if self.is_graduation_class:
            return f"{self.student_class.__str__()} {self.class_section.__str__()} Graduates"
        return f"{self.student_class.__str__()} {self.class_section.__str__()} promotes to {self.promotion_class.__str__()} {self.promotion_section.__str__()}"


class ClassSectionInfoModel(models.Model):
    """  """
    student_class = models.ForeignKey(ClassesModel, on_delete=models.CASCADE)
    section = models.ForeignKey(ClassSectionModel, blank=True, on_delete=models.CASCADE)
    subjects = models.ManyToManyField(SubjectsModel, blank=True, related_name='subject_class_info')
    form_teacher = models.ForeignKey(StaffModel, null=True, blank=True, on_delete=models.SET_NULL)
    assistant_form_teacher = models.ForeignKey(StaffModel, related_name='assistant_form_teacher', null=True, blank=True,
                                               on_delete=models.SET_NULL)
    class_rep = models.ForeignKey('student.StudentsModel', related_name='class_rep', null=True, blank=True,
                                  on_delete=models.SET_NULL)
    assistant_class_rep = models.ForeignKey('student.StudentsModel', related_name='assistant_class_rep', null=True,
                                            blank=True, on_delete=models.SET_NULL)
    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='class_section_info_updated_by')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        ordering = []
        constraints = [
            models.UniqueConstraint(
                fields=['student_class', 'section', 'type'],
                name='unique_student_class_section_combo'
            )
        ]

    def __str__(self):
        return "{} {}".format(self.student_class.name.upper(), self.section.name.upper())

    def number_of_students(self):
        StudentsModel = apps.get_model('student', 'StudentsModel')
        return StudentsModel.objects.filter(student_class=self.student_class, class_section=self.section).count()


class SubjectGroupModel(models.Model):
    """  """
    name = models.CharField(max_length=250)
    student_class = models.ManyToManyField(ClassesModel, blank=True, )
    subjects = models.ManyToManyField(SubjectsModel, blank=True, related_name='subject_group')
   
    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='subject_group_updated_by')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        ordering = []
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'type'],
                name='unique_subject_group_combo'
            )
        ]

    def __str__(self):
        return self.name.upper()


class ClassSectionSubjectTeacherModel(models.Model):
    """  """
    subject = models.ForeignKey(SubjectsModel, blank=True, on_delete=models.CASCADE,
                                related_name='subject_class_section_info')
    student_class = models.ManyToManyField(ClassesModel, blank=True)
    class_section = models.ManyToManyField(ClassSectionModel, blank=True)
    teachers = models.ManyToManyField(StaffModel, blank=True)
    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='class_section_subject_updated_by')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


class DaysModel(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name.upper()


class AcademicSettingModel(models.Model):
    """"""
    active_days = models.ManyToManyField(DaysModel, blank=True, related_name='active_days')
    week_start_day = models.ForeignKey(DaysModel, on_delete=models.SET_NULL, null=True, blank=True)
    head_teacher = models.ForeignKey(StaffModel, on_delete=models.SET_NULL, blank=True, null=True)
    nursery_head_teacher = models.ForeignKey(StaffModel, related_name='nursery', on_delete=models.SET_NULL, blank=True, null=True)
    promotion_cutoff_score = models.FloatField(default=30)
    date_school_closed = models.DateField(blank=True, null=True)
    next_term_open = models.DateField(blank=True, null=True)
    use_promotion_cutoff = models.BooleanField(default=True)
    lesson_note_approver = models.ManyToManyField(StaffModel, blank=True, related_name='lesson_note_approver')
    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True)

    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def week_active_days(self):
        return self.active_days.count()

    def termly_active_days(self):
        return 0


class LessonNoteModel(models.Model):
    student_class = models.ManyToManyField(ClassSectionInfoModel, blank=True)
    subject = models.ForeignKey(SubjectsModel, blank=True, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    scheduled_date = models.DateField(blank=True, null=True)
    scheduled_time = models.TimeField(blank=True, null=True)
    content = models.TextField()
    attachment = models.FileField(blank=True, storage=MediaStorage(), null=True, upload_to='lesson_note')
    STATUS = (('pending', 'PENDING'), ('approved', 'APPROVED'), ('declined', 'DECLINED'))
    status = models.CharField(max_length=20, blank=True, default='pending')
    decline_reason = models.TextField(null=True, blank=True)
    grant_access = models.BooleanField(default=False)
    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='lesson_note_updated_by')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


class LessonDocumentModel(models.Model):
    student_class = models.ManyToManyField(ClassSectionInfoModel, blank=True)
    subject = models.ForeignKey(SubjectsModel, blank=True, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    grant_access = models.BooleanField(default=False)
    document = models.FileField(upload_to='lesson_document', storage=MediaStorage())
    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='lesson_document_updated_by')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


