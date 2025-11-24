from django.contrib.auth import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm, Select, TextInput, DateInput, CheckboxSelectMultiple, Textarea, \
    ModelMultipleChoiceField
from student.models import ParentsModel, StudentsModel, StudentSettingModel, UtilityModel


class UtilityForm(ModelForm):
    """
    Form for creating and updating school utilities.
    """

    class Meta:
        model = UtilityModel
        fields = ['name', 'code', 'description']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Boarding, Transport'}),
            'code': TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., BRD, TRN'}),
            'description': Textarea(attrs={'class': 'form-control', 'rows': 3,
                                                 'placeholder': 'Optional: A brief description of the utility'}),
        }

    def clean_name(self):
        """
        Custom validation to ensure the utility name is unique (case-insensitive).
        """
        name = self.cleaned_data.get('name')
        if not name:
            raise ValidationError("Utility name cannot be empty.")

        # Check for other utilities with the same name, ignoring case.
        qs = UtilityModel.objects.filter(name__iexact=name)

        # If we are in "update" mode, exclude the current instance from the check.
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise ValidationError("A utility with this name already exists.")

        return name

    def clean_code(self):
        """
        Custom validation to ensure the utility code is unique (case-insensitive).
        """
        code = self.cleaned_data.get('code')
        if not code:
            raise ValidationError("Utility code cannot be empty.")

        # Check for other utilities with the same code, ignoring case.
        qs = UtilityModel.objects.filter(code__iexact=code)

        # If we are in "update" mode, exclude the current instance from the check.
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise ValidationError("A utility with this code already exists.")

        return code


class ParentForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = ParentsModel
        fields = '__all__'
        exclude = []
        widgets = {
            'date_of_birth': DateInput(attrs={
                'type': 'date'
            }),
        }


class ParentEditForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = ParentsModel
        fields = '__all__'
        exclude = ['type', 'user', 'parent_id']
        widgets = {
            'date_of_birth': DateInput(attrs={
                'type': 'date'
            }),
        }


class StudentForm(ModelForm):
    """"""
    utilities = ModelMultipleChoiceField(
        queryset=StudentsModel.utilities.field.related_model.objects.all(),
        widget=CheckboxSelectMultiple,
        required=False,  # Allow students to have no utilities
        label="Subscribed Utilities"
    )

    def __init__(self, *args, **kwargs):
        division = False
        if 'type' in kwargs.keys():
            division = kwargs.pop('type')

        super().__init__(*args, **kwargs)
        boolean_fields = ['is_new']
        for field in self.fields:
            if field not in boolean_fields:
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    'autocomplete': 'off'
                })

    def clean(self):
        cleaned_data = super().clean()
        registration_number = cleaned_data.get('registration_number')

        if registration_number:
            # Check if the registration number already exists
            if StudentsModel.objects.filter(registration_number=registration_number).exists():
                raise forms.ValidationError({
                    'registration_number': f'A student with this registration number {registration_number} already exists.'
                })

        return cleaned_data

    class Meta:
        model = StudentsModel
        fields = '__all__'
        exclude = []
        widgets = {
            'school': TextInput(attrs={
                'class': 'form-control',
            }),
            'date_of_birth': TextInput(attrs={
                'type': 'date',
                'class': 'form-control',
            })
        }


class StudentEditForm(ModelForm):
    """"""

    def __init__(self, *args, **kwargs):
        division = False
        if 'type' in kwargs.keys():
            division = kwargs.pop('type')

        super().__init__(*args, **kwargs)
        boolean_fields = ['is_new']
        for field in self.fields:
            if field not in boolean_fields:
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    'autocomplete': 'off'
                })

    def clean(self):
        cleaned_data = super().clean()
        registration_number = cleaned_data.get('registration_number')
        student = self.instance  # The current student instance being edited

        # Check if the registration number has been changed
        if registration_number and registration_number != student.registration_number:
            # If registration number has been modified, check if it already exists
            if StudentsModel.objects.filter(registration_number=registration_number).exclude(id=student.id).exists():
                raise forms.ValidationError({
                    'registration_number': f'A student with this registration number {registration_number} already exists.'
                })

        return cleaned_data

    class Meta:
        model = StudentsModel
        exclude = ['type', 'user', 'status', 'parent']
        widgets = {
            'school': TextInput(attrs={
                'class': 'form-control',
            }),
            'date_of_birth': TextInput(attrs={
                'type': 'date',
                'class': 'form-control',
            })
        }


class StudentSettingCreateForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        division = False
        if 'type' in kwargs.keys():
            division = kwargs.pop('type')

        super().__init__(*args, **kwargs)
        if division:
            pass
        for field in self.fields:
            if 0:
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    'autocomplete': 'off'
                })

    class Meta:
        model = StudentSettingModel
        fields = '__all__'

        widgets = {

        }


class StudentSettingEditForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        division = False
        if 'type' in kwargs.keys():
            division = kwargs.pop('type')

        super().__init__(*args, **kwargs)
        if division:
            pass
        for field in self.fields:
            if 0:
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    'autocomplete': 'off'
                })

    class Meta:
        model = StudentSettingModel
        exclude = ['type', 'user']

        widgets = {

        }

