from django.db import models
from student.models import StudentsModel
from academic.models import *
from school_setting.models import *
import random


class ResultFieldModel(models.Model):
    name = models.CharField(max_length=100)
    max_mark = models.FloatField()
    order = models.IntegerField(null=True, blank=True)
    student_class = models.ManyToManyField(ClassesModel, blank=True)
    class_section = models.ManyToManyField(ClassSectionModel, blank=True)
    FIELD_TYPE = (
        ('ca', 'CONTINUOUS ASSESSMENT'), ('exam', 'EXAM')
    )
    field_type = models.CharField(max_length=15, choices=FIELD_TYPE)
    mid_term = models.BooleanField(blank=True, default=False)
    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY'), ('mix', 'GENERAL')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='result_field_updated_by')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.name.upper()


class ResultGradeModel(models.Model):
    name = models.CharField(max_length=100)
    remark = models.CharField(max_length=100)
    min_mark = models.FloatField()
    max_mark = models.FloatField()
    order = models.IntegerField(null=True, blank=True)
    student_class = models.ManyToManyField(ClassesModel, blank=True)
    class_section = models.ManyToManyField(ClassSectionModel, blank=True)
    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY'), ('mix', 'GENERAL')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='result_grade_updated_by')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.name.upper()


class MidResultGradeModel(models.Model):
    name = models.CharField(max_length=100)
    remark = models.CharField(max_length=100)
    min_mark = models.FloatField()
    max_mark = models.FloatField()
    order = models.IntegerField(null=True, blank=True)
    student_class = models.ManyToManyField(ClassesModel, blank=True)
    class_section = models.ManyToManyField(ClassSectionModel, blank=True)
    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY'), ('mix', 'GENERAL')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='mid_result_grade_updated_by')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.name.upper()


class ResultBehaviourCategoryModel(models.Model):
    name = models.CharField(max_length=100)
    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY'), ('mix', 'GENERAL')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='result_behaviour_category_updated_by')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'type'],
                name='unique_result_behaviour_category_type_combo',
                violation_error_message='Result Behaviour Category Already Exists'
            )
        ]

    def __str__(self):
        return self.name.upper()

    def no_of_behaviours(self):
        return ResultBehaviourModel.objects.filter(category=self).count()


class ResultBehaviourModel(models.Model):
    category = models.ForeignKey(ResultBehaviourCategoryModel, on_delete=models.CASCADE,
                                 related_name='student_behaviour')
    name = models.CharField(max_length=100)
    max_mark = models.FloatField()
    order = models.IntegerField(null=True, blank=True)
    student_class = models.ManyToManyField(ClassesModel, blank=True)
    class_section = models.ManyToManyField(ClassSectionModel, blank=True)
    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY'), ('mix', 'GENERAL')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='result_affective_domain_updated_by')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.name.upper()


class ResultTemplateModel(models.Model):
    name = models.CharField(max_length=100)
    path = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    student_class = models.ManyToManyField(ClassesModel, blank=True)
    class_section = models.ManyToManyField(ClassSectionModel, blank=True)
    TEMPLATE_TYPE = (
        ('point based', 'POINT BASED'), ('text based', 'TEXT BASED')
    )
    template_type = models.CharField(max_length=30, choices=TEMPLATE_TYPE, blank=True, null=True)
    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY'), ('mix', 'GENERAL')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


class ResultSettingModel(models.Model):
    current_result_upload = models.ManyToManyField(ResultFieldModel, blank=True)

    ALLOWED_USER = (
        ('form teacher', 'FORM TEACHER'), ('subject teacher', 'SUBJECT TEACHER'), ('both', 'FORM OR SUBJECT TEACHER'),
        ('any', 'ANY USER')
    )
    allowed_user = models.CharField(max_length=30, choices=ALLOWED_USER, blank=True, null=True)
    text_result_allowed_user = models.CharField(max_length=30, choices=ALLOWED_USER, blank=True, null=True)
    STUDENT_VIEW_RESULT = (
        ('when published', 'WHEN PUBLISHED'), ('once uploaded', 'ONCE UPLOADED')
    )
    fee_payment = models.FloatField(default=0)
    student_view_result = models.CharField(max_length=20, choices=STUDENT_VIEW_RESULT, blank=True, null=True)
    RESULT_STATUS = (
        ('published', 'PUBLISHED'), ('not published', 'NOT PUBLISHED')
    )
    result_status = models.CharField(max_length=20, choices=RESULT_STATUS, blank=True, null=True)

    DEFAULT_COMMENT = (
        ('auto', 'AUTO COMMENTS'), ('manual', 'MANUAL COMMENTS')
    )
    default_comment = models.CharField(max_length=10, choices=DEFAULT_COMMENT, blank=True, null=True)
    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY'), ('mix', 'GENERAL')
    )

    type = models.CharField(max_length=10, choices=TYPE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


class TeacherResultCommentModel(models.Model):
    comment = models.TextField()
    min_score = models.FloatField()
    max_score = models.FloatField()
    student_class = models.ForeignKey(ClassSectionInfoModel, on_delete=models.CASCADE)

    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY'), ('mix', 'GENERAL')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='result_comment_updated_by')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


class HeadTeacherResultCommentModel(models.Model):
    comment = models.TextField()
    min_score = models.FloatField()
    max_score = models.FloatField()
    student_class = models.ManyToManyField(ClassesModel, blank=True)
    class_section = models.ManyToManyField(ClassSectionModel, blank=True)
    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY'), ('mix', 'GENERAL')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='result_head_comment_updated_by')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


class ResultModel(models.Model):
    session = models.ForeignKey(SessionModel, on_delete=models.CASCADE)
    term = models.ForeignKey(TermModel, on_delete=models.CASCADE, null=True)
    student_class = models.ForeignKey(ClassesModel, on_delete=models.CASCADE)
    class_section = models.ForeignKey(ClassSectionModel, on_delete=models.SET_NULL, null=True, blank=True)
    student = models.ForeignKey(StudentsModel, on_delete=models.CASCADE)
    result = models.JSONField(null=True, blank=True)
    total_score = models.FloatField(null=True)
    number_of_course = models.FloatField(null=True)
    user = models.ManyToManyField(User, blank=True)
    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY'), ('mix', 'GENERAL')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True, null=True)

    def __str__(self):
        return "{} - {} {}".format(self.student.__str__(), self.session.__str__(), self.term.name.title())

    def save(self, *args, **kwargs):
        if self.result:
            total_score = 0
            if self.student_class.result_type == 'score' or self.student_class.result_type == 'mix':
                for key, result in self.result.items():
                    try:
                        total_score += result['total']
                    except Exception:
                        pass
                self.total_score = total_score
                self.number_of_course = len(self.result.items())

            if self.student_class.result_type == 'text':
                course = 0
                for key, result in self.result.items():
                    if result:
                        course += 1
                        result = result.lower()
                        if result == 'established':
                            total_score += 5
                        elif result == 'above expectation':
                            total_score += 4
                        elif result == 'as expected':
                            total_score += 3
                        elif result == 'below expectation':
                            total_score += 2
                        if result == 'not yet':
                            total_score += 1
                self.total_score = total_score * 20
                self.number_of_course = course
        super(ResultModel, self).save(*args, **kwargs)

    def student_average(self):
        if self.total_score and self.number_of_course:
            return round((self.total_score / (100 * self.number_of_course)) * 100)
        return 0

    def class_average(self):
        aggregates = ResultModel.objects.filter(
            session=self.session, term=self.term, student_class=self.student_class,
            class_section=self.class_section
        ).aggregate(total_score=models.Sum('total_score'), total_course=models.Sum('number_of_course'))

        total_score = aggregates.get('total_score') or 0
        total_course = aggregates.get('total_course') or 0

        if total_course:
            return round((total_score / (100 * total_course) * 100))
        return 0

    def form_teacher(self):
        class_detail = ClassSectionInfoModel.objects.filter(student_class=self.student_class,
                                                            section=self.class_section).first()
        if class_detail:
            return class_detail.form_teacher or class_detail.assistant_form_teacher
        return None

    def head_teacher(self):
        class_head = HeadTeacherModel.objects.filter(student_class=self.student_class).first()
        if class_head:
            return class_head.head_teacher

        sch_setting = SchoolGeneralInfoModel.objects.first()
        if sch_setting.separate_school_section:
            academic_setting = AcademicSettingModel.objects.filter(type=self.type).first()
        else:
            academic_setting = AcademicSettingModel.objects.first()
        if academic_setting:
            return academic_setting.head_teacher
        return None

    def head_teacher_title(self):
        class_head = HeadTeacherModel.objects.filter(student_class=self.student_class).first()
        if class_head:
            return class_head.name
        return ''

    def get_comment(self, is_head_teacher=False):
        result_behaviour = ResultBehaviourComputeModel.objects.filter(student=self.student, session=self.session,
                                                                      term=self.term).first()
        comment_key = 'head_teacher_comment' if is_head_teacher else 'form_teacher_comment'

        if result_behaviour and result_behaviour.result_remark.get(comment_key):
            return result_behaviour.result_remark[comment_key]

        average_score = self.student_average()

        CommentModel = HeadTeacherResultCommentModel if is_head_teacher else TeacherResultCommentModel
        filter_kwargs = {
            'min_score__lte': average_score,
            'max_score__gte': average_score
        }
        if is_head_teacher:
            filter_kwargs['student_class'] = self.student_class
            filter_kwargs['class_section'] = self.class_section
        else:
            filter_kwargs['student_class__student_class'] = self.student_class
            filter_kwargs['student_class__section'] = self.class_section

        comment_list = CommentModel.objects.filter(**filter_kwargs)

        if comment_list:
            return random.choice(comment_list).comment
        return ''

    def form_teacher_comment(self):
        return self.get_comment(is_head_teacher=False)

    def head_teacher_comment(self):
        return self.get_comment(is_head_teacher=True)


class ResultUploadedModel(models.Model):
    session = models.ForeignKey(SessionModel, on_delete=models.CASCADE)
    term = models.ForeignKey(TermModel, on_delete=models.CASCADE, null=True)
    student_class = models.ForeignKey(ClassesModel, on_delete=models.CASCADE)
    class_section = models.ForeignKey(ClassSectionModel, on_delete=models.SET_NULL, null=True, blank=True)
    subject = models.ForeignKey(SubjectsModel, on_delete=models.CASCADE)
    ca_uploaded = models.BooleanField(null=True)
    exam_uploaded = models.BooleanField(null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField(auto_now=True, blank=True, null=True)
    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY'), ('mix', 'GENERAL')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True, null=True)


class ResultStatisticModel(models.Model):
    session = models.ForeignKey(SessionModel, on_delete=models.CASCADE)
    term = models.ForeignKey(TermModel, on_delete=models.CASCADE, null=True)
    student_class = models.ForeignKey(ClassesModel, on_delete=models.CASCADE)
    class_section = models.ForeignKey(ClassSectionModel, on_delete=models.SET_NULL, null=True, blank=True)
    result_statistic = models.JSONField()
    result_is_published = models.BooleanField(default=False, blank=True)


class ResultBehaviourComputeModel(models.Model):
    session = models.ForeignKey(SessionModel, on_delete=models.CASCADE)
    term = models.ForeignKey(TermModel, on_delete=models.CASCADE, null=True)
    student = models.ForeignKey(StudentsModel, on_delete=models.CASCADE)
    result_remark = models.JSONField()
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.student.__str__()


class ResultRemarkModel(models.Model):
    session = models.ForeignKey(SessionModel, on_delete=models.CASCADE)
    term = models.ForeignKey(TermModel, on_delete=models.CASCADE, null=True)
    student = models.ForeignKey(StudentsModel, on_delete=models.CASCADE)
    result_remark = models.JSONField()


class TextResultCategoryModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    order = models.IntegerField(null=True, blank=True)
    student_class = models.ManyToManyField(ClassesModel, blank=True)
    class_section = models.ManyToManyField(ClassSectionModel, blank=True)
    teachers = models.ManyToManyField(StaffModel, blank=True)
    session = models.ForeignKey(SessionModel, on_delete=models.CASCADE, blank=True, null=True)
    term = models.ForeignKey(TermModel, on_delete=models.CASCADE, blank=True, null=True)
    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY'), ('mix', 'GENERAL')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='text_result_category_updated_by')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        class_str = ', '.join([cls.name for cls in self.student_class.all()])
        return f"{self.name.upper()} - {class_str}"

    def save(self, *args, **kwargs):
        if not self.session or not self.term:
            school_setting = SchoolGeneralInfoModel.objects.first()
            academic_info_qs = SchoolAcademicInfoModel.objects
            if school_setting.separate_school_section and self.type:
                academic_setting = academic_info_qs.filter(type=self.type).first()
            else:
                academic_setting = academic_info_qs.first()

            if academic_setting:
                self.term = academic_setting.term
                self.session = academic_setting.session

        super(TextResultCategoryModel, self).save(*args, **kwargs)


class TextResultModel(models.Model):
    category = models.ForeignKey(TextResultCategoryModel, on_delete=models.CASCADE, related_name='text_result_fields')
    name = models.CharField(max_length=100)
    order = models.IntegerField(null=True, blank=True)
    student_class = models.ManyToManyField(ClassesModel, blank=True)
    class_section = models.ManyToManyField(ClassSectionModel, blank=True)
    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY'), ('mix', 'GENERAL')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='text_result_updated_by')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.name.upper()


class TextBasedResultModel(models.Model):
    session = models.ForeignKey(SessionModel, on_delete=models.CASCADE)
    term = models.ForeignKey(TermModel, on_delete=models.CASCADE, null=True)
    student_class = models.ForeignKey(ClassesModel, on_delete=models.CASCADE)
    class_section = models.ForeignKey(ClassSectionModel, on_delete=models.SET_NULL, null=True, blank=True)
    student = models.ForeignKey(StudentsModel, on_delete=models.CASCADE)
    result = models.JSONField(null=True, blank=True)
    user = models.ManyToManyField(User, blank=True)
    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY'), ('mix', 'GENERAL')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True, null=True)

    def form_teacher(self):
        class_detail = ClassSectionInfoModel.objects.filter(student_class=self.student_class,
                                                            section=self.class_section).first()
        if class_detail:
            return class_detail.form_teacher or class_detail.assistant_form_teacher
        return None

    def head_teacher(self):
        class_head = HeadTeacherModel.objects.filter(student_class=self.student_class).first()
        if class_head:
            return class_head.head_teacher

        sch_setting = SchoolGeneralInfoModel.objects.first()
        if sch_setting.separate_school_section:
            academic_setting = AcademicSettingModel.objects.filter(type=self.type).first()
        else:
            academic_setting = AcademicSettingModel.objects.first()
        if academic_setting:
            return academic_setting.head_teacher
        return None

    def head_teacher_title(self):
        class_head = HeadTeacherModel.objects.filter(student_class__in=[self.student_class]).first()
        if class_head:
            return class_head.name
        return ''

    def get_comment(self, is_head_teacher=False):
        result_behaviour = ResultBehaviourComputeModel.objects.filter(student=self.student, session=self.session,
                                                                      term=self.term).first()
        comment_key = 'head_teacher_comment' if is_head_teacher else 'form_teacher_comment'

        if result_behaviour and result_behaviour.result_remark.get(comment_key):
            return result_behaviour.result_remark[comment_key]

        CommentModel = HeadTeacherResultCommentModel if is_head_teacher else TeacherResultCommentModel
        filter_kwargs = {}
        if is_head_teacher:
            filter_kwargs['student_class'] = self.student_class
            filter_kwargs['class_section'] = self.class_section
        else:
            filter_kwargs['student_class__student_class'] = self.student_class
            filter_kwargs['student_class__section'] = self.class_section

        comment_list = CommentModel.objects.filter(**filter_kwargs)

        if comment_list:
            return random.choice(comment_list).comment
        return ''

    def form_teacher_comment(self):
        return self.get_comment(is_head_teacher=False)

    def head_teacher_comment(self):
        return self.get_comment(is_head_teacher=True)

