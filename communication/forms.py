from django.forms import ModelForm, Select, TextInput, DateInput, CheckboxSelectMultiple
from communication.models import *


class SMTPConfigurationForm(ModelForm):
    """  """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = SMTPConfigurationModel
        fields = '__all__'
        widgets = {
            'password': TextInput(attrs={
                'type': 'password'
            })
        }


class SMTPConfigurationEditForm(ModelForm):
    """  """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = SMTPConfigurationModel
        exclude = ['type', 'user']
        widgets = {
            'password': TextInput(attrs={
                'type': 'password'
            })
        }


class SMSConfigurationForm(ModelForm):
    """  """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = SMSConfigurationModel
        fields = '__all__'
        widgets = {

        }


class SMSConfigurationEditForm(ModelForm):
    """  """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = SMSConfigurationModel
        exclude = ['type', 'user']
        widgets = {

        }


class CommunicationSettingCreateForm(ModelForm):
    """  """
    def __init__(self, *args, **kwargs):
        division = False
        if 'type' in kwargs.keys():
            division = kwargs.pop('type')

        super().__init__(*args, **kwargs)
        if division:
            pass
        for field in self.fields:
            if field != 'auto_save_sent_message':
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    'autocomplete': 'off'
                })

    class Meta:
        model = CommunicationSettingModel
        fields = '__all__'

        widgets = {

        }


class CommunicationSettingEditForm(ModelForm):
    """  """
    def __init__(self, *args, **kwargs):
        division = False
        if 'type' in kwargs.keys():
            division = kwargs.pop('type')

        super().__init__(*args, **kwargs)
        if division:
            pass
        for field in self.fields:
            if field != 'auto_save_sent_message':
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    'autocomplete': 'off'
                })

    class Meta:
        model = CommunicationSettingModel
        exclude = ['type', 'user']

        widgets = {

        }

