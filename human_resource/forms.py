from django.forms import ModelForm, Select, TextInput, DateInput, CheckboxInput
from human_resource.models import *
from django import forms


class DepartmentForm(ModelForm):
    """  """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = DepartmentModel
        fields = '__all__'
        widgets = {

        }


class DepartmentEditForm(ModelForm):
    """  """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = DepartmentModel
        fields = ['name', 'description', 'updated_by']
        widgets = {

        }


class PositionForm(ModelForm):
    """  """
    def __init__(self, *args, **kwargs):
        division = False
        if 'type' in kwargs.keys():
            division = kwargs.pop('type')

        super().__init__(*args, **kwargs)
        if division:
            self.fields['department'].queryset = DepartmentModel.objects.filter(type=division).order_by('name')
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = PositionModel
        fields = '__all__'
        widgets = {

        }


class PositionEditForm(ModelForm):
    """  """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = PositionModel
        fields = ['name', 'department', 'description', 'updated_by']
        widgets = {

        }


class StaffForm(ModelForm):
    """  """
    def __init__(self, *args, **kwargs):
        division = False
        if 'type' in kwargs.keys():
            division = kwargs.pop('type')

        super().__init__(*args, **kwargs)
        if division:
            self.fields['department'].queryset = DepartmentModel.objects.filter(type=division).order_by('name')
            self.fields['position'].queryset = PositionModel.objects.filter(type=division).order_by('name')

        self.fields['group'].queryset = Group.objects.exclude(name='student').exclude(name='parent').order_by('name')
        for field in self.fields:
            if field != 'can_teach':
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    'autocomplete': 'off'
                })

    class Meta:
        model = StaffModel
        fields = '__all__'
        widgets = {
            'date_of_birth': DateInput(attrs={
                'type': 'date'
            }),
            'employment_date': DateInput(attrs={
                'type': 'date'
            }),
            'can_teach': CheckboxInput(attrs={

            })
        }


class StaffEditForm(ModelForm):
    """  """
    def __init__(self, *args, **kwargs):
        division = False
        if 'type' in kwargs.keys():
            division = kwargs.pop('type')

        super().__init__(*args, **kwargs)
        if division:
            self.fields['department'].queryset = DepartmentModel.objects.filter(type=division).order_by('name')
            self.fields['position'].queryset = PositionModel.objects.filter(type=division).order_by('name')

        self.fields['group'].queryset = Group.objects.exclude(name='student').order_by('name')
        for field in self.fields:
            if field != 'can_teach':
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    'autocomplete': 'off'
                })

    class Meta:
        model = StaffModel
        exclude = ['user', 'type', 'barcode']
        widgets = {
            'date_of_birth': DateInput(attrs={
                'type': 'date'
            }),
            'employment_date': DateInput(attrs={
                'type': 'date'
            }),
            'staff_id': TextInput(attrs={
                'readonly': True
            })
        }


class StaffProfileUpdateForm(forms.ModelForm):
    """
    Form for staff members to update their own profile information.
    The 'group' (position) is excluded as requested.
    """
    class Meta:
        model = StaffModel
        fields = ['title', 'surname', 'middle_name', 'last_name', 'mobile', 'email', 'signature']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'surname': forms.TextInput(attrs={'class': 'form-control'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'signature': forms.FileInput(attrs={'class': 'form-control'}),
        }


class HRSettingCreateForm(ModelForm):
    """  """
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
        model = HRSettingModel
        fields = '__all__'

        widgets = {

        }


class HRSettingEditForm(ModelForm):
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
        model = HRSettingModel
        exclude = ['type', 'user']

        widgets = {

        }
