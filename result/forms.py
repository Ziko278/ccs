from django.forms import ModelForm, Select, TextInput, DateInput, CheckboxSelectMultiple, RadioSelect
from result.models import *
from django.db.models import Q


class ResultFieldForm(ModelForm):
    """  """
    def __init__(self, *args, **kwargs):
        division = False
        if 'type' in kwargs.keys():
            division = kwargs.pop('type')

        super().__init__(*args, **kwargs)
        if division:
            self.fields['class_section'].queryset = ClassSectionModel.objects.filter(type=division).order_by('name')
            self.fields['student_class'].queryset = ClassesModel.objects.filter(Q(result_type='score') | Q(result_type='mix'), type=division).order_by('name')
        for field in self.fields:
            if field != 'student_class' and field != 'class_section' and field != 'mid_term':
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    'autocomplete': 'off'
                })

    class Meta:
        model = ResultFieldModel
        fields = '__all__'
        widgets = {
            'student_class': CheckboxSelectMultiple(attrs={

            }),
            'class_section': CheckboxSelectMultiple(attrs={

            })
        }


class ResultFieldEditForm(ModelForm):
    """  """
    def __init__(self, *args, **kwargs):
        division = False
        if 'type' in kwargs.keys():
            division = kwargs.pop('type')

        super().__init__(*args, **kwargs)
        if division:
            self.fields['class_section'].queryset = ClassSectionModel.objects.filter(type=division).order_by('name')
            self.fields['student_class'].queryset = ClassesModel.objects.filter(Q(result_type='score') | Q(result_type='mix'), type=division).order_by('name')
        else:
            self.fields['class_section'].queryset = ClassSectionModel.objects.all().order_by('name')
            self.fields['student_class'].queryset = ClassesModel.objects.filter(Q(result_type='score') | Q(result_type='mix')).order_by('name')
        for field in self.fields:
            if field != 'student_class' and field != 'class_section' and field != 'mid_term':
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    'autocomplete': 'off'
                })

    class Meta:
        model = ResultFieldModel
        exclude = ['type', 'user']
        widgets = {
            'student_class': CheckboxSelectMultiple(attrs={

            }),
            'class_section': CheckboxSelectMultiple(attrs={

            })
        }


class ResultGradeForm(ModelForm):
    """  """
    def __init__(self, *args, **kwargs):
        division = False
        if 'type' in kwargs.keys():
            division = kwargs.pop('type')

        super().__init__(*args, **kwargs)
        if division:
            self.fields['class_section'].queryset = ClassSectionModel.objects.filter(type=division).order_by('name')
            self.fields['student_class'].queryset = ClassesModel.objects.filter(Q(result_type='score') | Q(result_type='mix'), type=division,
                                                                                ).order_by('name')
        else:
            self.fields['class_section'].queryset = ClassSectionModel.objects.all().order_by('name')
            self.fields['student_class'].queryset = ClassesModel.objects.filter(Q(result_type='score') | Q(result_type='mix')).order_by('name')
        for field in self.fields:
            if field != 'student_class' and field != 'class_section':
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    'autocomplete': 'off'
                })

    class Meta:
        model = ResultGradeModel
        fields = '__all__'
        widgets = {
            'student_class': CheckboxSelectMultiple(attrs={

            }),
            'class_section': CheckboxSelectMultiple(attrs={

            })
        }


class ResultGradeEditForm(ModelForm):
    """  """
    def __init__(self, *args, **kwargs):
        division = False
        if 'type' in kwargs.keys():
            division = kwargs.pop('type')

        super().__init__(*args, **kwargs)
        if division:
            self.fields['class_section'].queryset = ClassSectionModel.objects.filter(type=division).order_by('name')
            self.fields['student_class'].queryset = ClassesModel.objects.filter(Q(result_type='score') | Q(result_type='mix'), type=division,
                                                                                ).order_by('name')
        else:
            self.fields['class_section'].queryset = ClassSectionModel.objects.all().order_by('name')
            self.fields['student_class'].queryset = ClassesModel.objects.filter(Q(result_type='score') | Q(result_type='mix')).order_by('name')
        for field in self.fields:
            if field != 'student_class' and field != 'class_section':
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    'autocomplete': 'off'
                })

    class Meta:
        model = ResultGradeModel
        exclude = ['type', 'user']
        widgets = {
            'student_class': CheckboxSelectMultiple(attrs={

            }),
            'class_section': CheckboxSelectMultiple(attrs={

            })
        }


class MidResultGradeForm(ModelForm):
    """  """
    def __init__(self, *args, **kwargs):
        division = False
        if 'type' in kwargs.keys():
            division = kwargs.pop('type')

        super().__init__(*args, **kwargs)
        if division:
            self.fields['class_section'].queryset = ClassSectionModel.objects.filter(type=division).order_by('name')
            self.fields['student_class'].queryset = ClassesModel.objects.filter(Q(result_type='score') | Q(result_type='mix'), type=division,
                                                                                ).order_by('name')
        else:
            self.fields['class_section'].queryset = ClassSectionModel.objects.all().order_by('name')
            self.fields['student_class'].queryset = ClassesModel.objects.filter(Q(result_type='score') | Q(result_type='mix'),).order_by('name')
        for field in self.fields:
            if field != 'student_class' and field != 'class_section':
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    'autocomplete': 'off'
                })

    class Meta:
        model = MidResultGradeModel
        fields = '__all__'
        widgets = {
            'student_class': CheckboxSelectMultiple(attrs={

            }),
            'class_section': CheckboxSelectMultiple(attrs={

            })
        }


class MidResultGradeEditForm(ModelForm):
    """  """
    def __init__(self, *args, **kwargs):
        division = False
        if 'type' in kwargs.keys():
            division = kwargs.pop('type')

        super().__init__(*args, **kwargs)
        if division:
            self.fields['class_section'].queryset = ClassSectionModel.objects.filter(type=division).order_by('name')
            self.fields['student_class'].queryset = ClassesModel.objects.filter(Q(result_type='score') | Q(result_type='mix'), type=division,
                                                                                ).order_by('name')
        else:
            self.fields['class_section'].queryset = ClassSectionModel.objects.all().order_by('name')
            self.fields['student_class'].queryset = ClassesModel.objects.filter(Q(result_type='score') | Q(result_type='mix'),).order_by('name')
        for field in self.fields:
            if field != 'student_class' and field != 'class_section':
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    'autocomplete': 'off'
                })

    class Meta:
        model = MidResultGradeModel
        exclude = ['type', 'user']
        widgets = {
            'student_class': CheckboxSelectMultiple(attrs={

            }),
            'class_section': CheckboxSelectMultiple(attrs={

            })
        }


class ResultBehaviourCategoryForm(ModelForm):
    """  """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = ResultBehaviourCategoryModel
        fields = '__all__'
        widgets = {
        }


class ResultBehaviourCategoryEditForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'student_class' and field != 'class_section':
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    'autocomplete': 'off'
                })

    class Meta:
        model = ResultBehaviourCategoryModel
        exclude = ['type', 'user']
        widgets = {

        }


class ResultBehaviourForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        division = False
        if 'type' in kwargs.keys():
            division = kwargs.pop('type')

        super().__init__(*args, **kwargs)
        if division:
            self.fields['class_section'].queryset = ClassSectionModel.objects.filter(type=division).order_by('name')
            self.fields['student_class'].queryset = ClassesModel.objects.filter(type=division).order_by('name')
            self.fields['category'].queryset = ResultBehaviourCategoryModel.objects.filter(type=division).order_by(
                'name')
        for field in self.fields:
            if field != 'student_class' and field != 'class_section':
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    'autocomplete': 'off'
                })

    class Meta:
        model = ResultBehaviourModel
        fields = '__all__'
        widgets = {
            'student_class': CheckboxSelectMultiple(attrs={

            }),
            'class_section': CheckboxSelectMultiple(attrs={

            })
        }


class ResultBehaviourEditForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        division = False
        if 'type' in kwargs.keys():
            division = kwargs.pop('type')

        super().__init__(*args, **kwargs)
        if division:
            self.fields['class_section'].queryset = ClassSectionModel.objects.filter(type=division).order_by('name')
            self.fields['student_class'].queryset = ClassesModel.objects.filter(type=division).order_by('name')
        for field in self.fields:
            if field != 'student_class' and field != 'class_section':
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    'autocomplete': 'off'
                })

    class Meta:
        model = ResultBehaviourModel
        exclude = ['type', 'user']
        widgets = {
            'student_class': CheckboxSelectMultiple(attrs={

            }),
            'class_section': CheckboxSelectMultiple(attrs={

            })
        }


class TextResultCategoryForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        division = False
        if 'type' in kwargs.keys():
            division = kwargs.pop('type')

        super().__init__(*args, **kwargs)
        if division:
            self.fields['class_section'].queryset = ClassSectionModel.objects.filter(type=division).order_by('name')
            self.fields['student_class'].queryset = ClassesModel.objects.filter(Q(result_type='text') | Q (result_type='mix'), type=division).order_by('name')
        else:
            self.fields['class_section'].queryset = ClassSectionModel.objects.all().order_by('name')
            self.fields['student_class'].queryset = ClassesModel.objects.filter(Q(result_type='text') | Q (result_type='mix')).order_by('name')
        for field in self.fields:
            if field != 'student_class' and field != 'class_section':
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    'autocomplete': 'off'
                })

    class Meta:
        model = TextResultCategoryModel
        exclude = ['teachers']
        widgets = {
            'student_class': CheckboxSelectMultiple(attrs={

            }),
            'class_section': CheckboxSelectMultiple(attrs={

            }),
            'teachers': CheckboxSelectMultiple(attrs={

            })
        }


class TextResultCategoryEditForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        division = False
        if 'type' in kwargs.keys():
            division = kwargs.pop('type')

        super().__init__(*args, **kwargs)
        if division:
            self.fields['class_section'].queryset = ClassSectionModel.objects.filter(type=division).order_by('name')
            self.fields['student_class'].queryset = ClassesModel.objects.filter(Q(result_type='text') | Q (result_type='mix'),type=division).order_by('name')
        else:
            self.fields['class_section'].queryset = ClassSectionModel.objects.all().order_by('name')
            self.fields['student_class'].queryset = ClassesModel.objects.filter(Q(result_type='text') | Q (result_type='mix')).order_by('name')
        for field in self.fields:
            if field != 'student_class' and field != 'class_section':
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    'autocomplete': 'off'
                })

    class Meta:
        model = TextResultCategoryModel
        exclude = ['teachers', 'type', 'user']
        widgets = {
            'student_class': CheckboxSelectMultiple(attrs={

            }),
            'class_section': CheckboxSelectMultiple(attrs={

            })
        }


class TextResultCategoryTeacherForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        division = False
        if 'type' in kwargs.keys():
            division = kwargs.pop('type')

        super().__init__(*args, **kwargs)
        if division:
            self.fields['teachers'].queryset = StaffModel.objects.filter(type=division, can_teach=True).order_by('surname')
        else:
            self.fields['teachers'].queryset = StaffModel.objects.filter(can_teach=True).order_by('surname')

        for field in self.fields:
            if field != 'teachers':
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    'autocomplete': 'off'
                })

    class Meta:
        model = TextResultCategoryModel
        fields = ['teachers']
        widgets = {
            'teachers': CheckboxSelectMultiple(attrs={

            })
        }


class TextResultForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        division = False
        if 'type' in kwargs.keys():
            division = kwargs.pop('type')

        super().__init__(*args, **kwargs)
        if division:
            self.fields['class_section'].queryset = ClassSectionModel.objects.filter(type=division).order_by('name')
            self.fields['student_class'].queryset = ClassesModel.objects.filter(Q(result_type='text') | Q(result_type='mix'), type=division,
                                                                                ).order_by('name')
            academic_setting = SchoolAcademicInfoModel.objects.filter(type=division).first()
            session = academic_setting.session
            term = academic_setting.term

            self.fields['category'].queryset = TextResultCategoryModel.objects.filter(term=term, session=session, type=division).order_by(
                'name')
        else:
            self.fields['class_section'].queryset = ClassSectionModel.objects.all().order_by('name')
            self.fields['student_class'].queryset = ClassesModel.objects.filter(Q(result_type='text') | Q(result_type='mix')).order_by('name')
            academic_setting = SchoolAcademicInfoModel.objects.first()
            session = academic_setting.session
            term = academic_setting.term
            self.fields['category'].queryset = TextResultCategoryModel.objects.filter(term=term, session=session).order_by(
                'name')
        for field in self.fields:
            if field != 'student_class' and field != 'class_section':
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    'autocomplete': 'off'
                })

    class Meta:
        model = TextResultModel
        fields = '__all__'
        widgets = {
            'student_class': CheckboxSelectMultiple(attrs={

            }),
            'class_section': CheckboxSelectMultiple(attrs={

            })
        }


class TextResultEditForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        division = False
        if 'type' in kwargs.keys():
            division = kwargs.pop('type')

        super().__init__(*args, **kwargs)

        if division:
            self.fields['class_section'].queryset = ClassSectionModel.objects.filter(type=division).order_by('name')
            self.fields['student_class'].queryset = ClassesModel.objects.filter(Q(result_type='text') | Q(result_type='mix'), type=division,
                                                                                ).order_by('name')
            academic_setting = SchoolAcademicInfoModel.objects.filter(type=division).first()
            session = academic_setting.session
            term = academic_setting.term

            self.fields['category'].queryset = TextResultCategoryModel.objects.filter(term=term, session=session, type=division).order_by(
                'name')
        else:
            self.fields['class_section'].queryset = ClassSectionModel.objects.all().order_by('name')
            self.fields['student_class'].queryset = ClassesModel.objects.filter(Q(result_type='text') | Q(result_type='mix')).order_by('name')
            academic_setting = SchoolAcademicInfoModel.objects.first()
            session = academic_setting.session
            term = academic_setting.term
            self.fields['category'].queryset = TextResultCategoryModel.objects.filter(term=term, session=session).order_by(
                'name')
        for field in self.fields:
            if field != 'student_class' and field != 'class_section':
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    'autocomplete': 'off'
                })

    class Meta:
        model = TextResultModel
        exclude = ['type', 'user']
        widgets = {
            'student_class': CheckboxSelectMultiple(attrs={

            }),
            'class_section': CheckboxSelectMultiple(attrs={

            })
        }


class TeacherResultCommentForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        division = False
        teacher = kwargs.pop('teacher')
        teacher = [teacher]
        if 'type' in kwargs.keys():
            division = kwargs.pop('type')

        super().__init__(*args, **kwargs)
        if division:
            self.fields['student_class'].queryset = ClassSectionInfoModel.objects.filter(type=division).filter(
                Q(form_teacher__in=teacher) | Q(assistant_form_teacher__in=teacher)).order_by(
                'student_class__name')
        else:
            self.fields['student_class'].queryset = ClassSectionInfoModel.objects.filter(
                Q(form_teacher__in=teacher) | Q(assistant_form_teacher__in=teacher)).order_by(
                'student_class__name')
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = TeacherResultCommentModel
        fields = '__all__'
        widgets = {

        }


class TeacherResultCommentEditForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        division = False
        teacher = kwargs.pop('teacher')
        teacher = [teacher]
        if 'type' in kwargs.keys():
            division = kwargs.pop('type')

        super().__init__(*args, **kwargs)
        if division:
            self.fields['student_class'].queryset = ClassSectionInfoModel.objects.filter(type=division).filter(
                Q(form_teacher__in=teacher) | Q(assistant_form_teacher__in=teacher)).order_by(
                'student_class__name')
        else:
            self.fields['student_class'].queryset = ClassSectionInfoModel.objects.filter(
                Q(form_teacher__in=teacher) | Q(assistant_form_teacher__in=teacher)).order_by(
                'student_class__name')
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = TeacherResultCommentModel
        exclude = ['type', 'user']
        widgets = {

        }


class HeadTeacherResultCommentForm(ModelForm):
    """"""

    def __init__(self, *args, **kwargs):
        division = False
        if 'type' in kwargs.keys():
            division = kwargs.pop('type')

        super().__init__(*args, **kwargs)
        if division:
            self.fields['class_section'].queryset = ClassSectionModel.objects.filter(type=division).order_by('name')
            self.fields['student_class'].queryset = ClassesModel.objects.filter(type=division).order_by('name')
        for field in self.fields:
            if field != 'student_class' and field != 'class_section':
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    'autocomplete': 'off'
                })

    class Meta:
        model = HeadTeacherResultCommentModel
        fields = '__all__'
        widgets = {
            'student_class': CheckboxSelectMultiple(attrs={

            }),
            'class_section': CheckboxSelectMultiple(attrs={

            })
        }


class HeadTeacherResultCommentEditForm(ModelForm):
    """"""

    def __init__(self, *args, **kwargs):
        division = False
        if 'type' in kwargs.keys():
            division = kwargs.pop('type')

        super().__init__(*args, **kwargs)
        if division:
            self.fields['class_section'].queryset = ClassSectionModel.objects.filter(type=division).order_by('name')
            self.fields['student_class'].queryset = ClassesModel.objects.filter(type=division).order_by('name')
        for field in self.fields:
            if field != 'student_class' and field != 'class_section':
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    'autocomplete': 'off'
                })

    class Meta:
        model = HeadTeacherResultCommentModel
        exclude = ['type', 'user']
        widgets = {
            'student_class': CheckboxSelectMultiple(attrs={

            }),
            'class_section': CheckboxSelectMultiple(attrs={

            })
        }


class ResultSettingCreateForm(ModelForm):
    """Form for creating new result settings"""

    def __init__(self, *args, **kwargs):
        division = False
        if 'type' in kwargs.keys():
            division = kwargs.pop('type')

        super().__init__(*args, **kwargs)

        # Filter current_result_upload by division if provided
        if division:
            self.fields['current_result_upload'].queryset = ResultFieldModel.objects.filter(type=division).order_by(
                'name')

        # Apply form-control class to all fields except checkboxes
        for field in self.fields:
            if field != 'current_result_upload':
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    'autocomplete': 'off'
                })

        # Add special styling for fee restriction type (radio buttons look better)
        self.fields['fee_restriction_type'].widget = RadioSelect(attrs={
            'class': 'form-check-input fee-restriction-radio'
        })

        # Add help text to fee_payment field
        self.fields['fee_payment'].widget.attrs.update({
            'placeholder': 'Enter percentage or amount',
            'min': '0',
            'step': '0.01'
        })

        # Customize fee_restriction_scope field
        self.fields['fee_restriction_scope'].empty_label = "All Fees (Total Balance)"
        self.fields['fee_restriction_scope'].widget.attrs.update({
            'class': 'form-select'
        })

    class Meta:
        model = ResultSettingModel
        fields = '__all__'

        widgets = {
            'current_result_upload': CheckboxSelectMultiple(),
        }

        labels = {
            'fee_restriction_type': 'Fee Restriction Method',
            'fee_payment': 'Threshold Value',
            'fee_restriction_scope': 'Apply Restriction To',
        }


class ResultSettingEditForm(ModelForm):
    """Form for editing existing result settings"""

    def __init__(self, *args, **kwargs):
        division = False
        if 'type' in kwargs.keys():
            division = kwargs.pop('type')

        super().__init__(*args, **kwargs)

        # Filter current_result_upload by division if provided
        if division:
            self.fields['current_result_upload'].queryset = ResultFieldModel.objects.filter(type=division).order_by(
                'name')

        # Apply form-control class to all fields except checkboxes
        for field in self.fields:
            if field != 'current_result_upload':
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    'autocomplete': 'off'
                })

        # Add special styling for fee restriction type (radio buttons)
        self.fields['fee_restriction_type'].widget = RadioSelect(attrs={
            'class': 'form-check-input fee-restriction-radio'
        })

        # Add help text to fee_payment field
        self.fields['fee_payment'].widget.attrs.update({
            'placeholder': 'Enter percentage or amount',
            'min': '0',
            'step': '0.01'
        })

        # Customize fee_restriction_scope field
        self.fields['fee_restriction_scope'].empty_label = "All Fees (Total Balance)"
        self.fields['fee_restriction_scope'].widget.attrs.update({
            'class': 'form-select'
        })

    class Meta:
        model = ResultSettingModel
        exclude = ['type', 'user']

        widgets = {
            'current_result_upload': CheckboxSelectMultiple(),
        }

        labels = {
            'fee_restriction_type': 'Fee Restriction Method',
            'fee_payment': 'Threshold Value',
            'fee_restriction_scope': 'Apply Restriction To',
        }