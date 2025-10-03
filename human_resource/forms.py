from django.forms import ModelForm, Select, TextInput, DateInput, CheckboxInput
from human_resource.models import *

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
