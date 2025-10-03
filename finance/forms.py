from django.forms import ModelForm, Select, TextInput, DateInput, CheckboxSelectMultiple
from finance.models import *


class FeeForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = FeeModel
        fields = '__all__'
        widgets = {

        }


class FeeEditForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = FeeModel
        exclude = ['type', 'user']
        widgets = {

        }


class FeeGroupForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = FeeGroupModel
        fields = '__all__'
        widgets = {

        }


class FeeGroupEditForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = FeeGroupModel
        exclude = ['type', 'user']
        widgets = {

        }


class FeeMasterForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        division = False
        if 'type' in kwargs.keys():
            division = kwargs.pop('type')

        super().__init__(*args, **kwargs)
        if division:
            self.fields['class_section'].queryset = ClassSectionModel.objects.filter(type=division).order_by('name')
            self.fields['student_class'].queryset = ClassesModel.objects.filter(type=division).order_by('name')
            self.fields['group'].queryset = FeeGroupModel.objects.filter(type=division).order_by('name')
            self.fields['fee'].queryset = FeeModel.objects.filter(type=division).order_by('name')
        boolean_fields = ['is_new', 'class_section', 'student_class']
        for field in self.fields:
            if field not in boolean_fields:
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    'autocomplete': 'off'
                })

    class Meta:
        model = FeeMasterModel
        fields = '__all__'
        widgets = {
            'class_section': CheckboxSelectMultiple(attrs={

            }),

            'student_class': CheckboxSelectMultiple(attrs={

            })
        }


class FeeMasterEditForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        division = False
        if 'type' in kwargs.keys():
            division = kwargs.pop('type')

        super().__init__(*args, **kwargs)
        if division:
            self.fields['class_section'].queryset = ClassSectionModel.objects.filter(type=division).order_by('name')
            self.fields['student_class'].queryset = ClassesModel.objects.filter(type=division).order_by('name')
            self.fields['group'].queryset = FeeGroupModel.objects.filter(type=division).order_by('name')
            self.fields['fee'].queryset = FeeModel.objects.filter(type=division).order_by('name')

        boolean_fields = ['is_new', 'class_section', 'student_class']
        for field in self.fields:
            if field not in boolean_fields:
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    'autocomplete': 'off'
                })

    class Meta:
        model = FeeMasterModel
        exclude = ['type', 'user']
        widgets = {
            'class_section': CheckboxSelectMultiple(attrs={

            }),

            'student_class': CheckboxSelectMultiple(attrs={

            })
        }


class FeeDiscountForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        division = False
        if 'type' in kwargs.keys():
            division = kwargs.pop('type')

        super().__init__(*args, **kwargs)
        if division:
            self.fields['fee_master'].queryset = FeeMasterModel.objects.filter(type=division).order_by('fee__name')

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = FeeDiscountModel
        fields = '__all__'
        widgets = {

        }


class FeeDiscountEditForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        division = False
        if 'type' in kwargs.keys():
            division = kwargs.pop('type')

        super().__init__(*args, **kwargs)
        if division:
            self.fields['fee_master'].queryset = FeeMasterModel.objects.filter(type=division).order_by('fee__name')

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = FeeDiscountModel
        exclude = ['type', 'user']
        widgets = {

        }


class FeeDiscountGroupForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        division = False
        if 'type' in kwargs.keys():
            division = kwargs.pop('type')

        super().__init__(*args, **kwargs)
        if division:
            self.fields['discounts'].queryset = FeeDiscountModel.objects.filter(type=division)
        for field in self.fields:
            if field != 'discounts':
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    'autocomplete': 'off'
                })

    class Meta:
        model = FeeDiscountGroupModel
        fields = '__all__'
        widgets = {
            'discounts': CheckboxSelectMultiple(attrs={

            })
        }


class FeeDiscountGroupAddBenefactorForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

    class Meta:
        model = FeeDiscountGroupModel
        fields = ['students']
        widgets = {

        }


class FeeDiscountGroupEditForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        division = False
        if 'type' in kwargs.keys():
            division = kwargs.pop('type')

        super().__init__(*args, **kwargs)
        if division:
            self.fields['discounts'].queryset = FeeDiscountModel.objects.filter(type=division)

        for field in self.fields:
            if field != 'discounts':
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    'autocomplete': 'off'
                })

    class Meta:
        model = FeeDiscountGroupModel
        exclude = ['type', 'user', 'students']
        widgets = {
            'discounts': CheckboxSelectMultiple(attrs={

            })
        }


class FeePenaltyForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        division = False
        if 'type' in kwargs.keys():
            division = kwargs.pop('type')

        super().__init__(*args, **kwargs)
        if division:
            self.fields['fee_master'].queryset = FeeMasterModel.objects.filter(type=division).order_by('fee__name')

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = FeePenaltyModel
        fields = '__all__'
        widgets = {

        }


class FeePenaltyEditForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        division = False
        if 'type' in kwargs.keys():
            division = kwargs.pop('type')

        super().__init__(*args, **kwargs)
        if division:
            self.fields['fee_master'].queryset = FeeMasterModel.objects.filter(type=division).order_by('fee__name')

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = FeePenaltyModel
        exclude = ['type', 'user']
        widgets = {

        }


class FeePaymentForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = FeePaymentModel
        fields = '__all__'
        widgets = {
            'date': DateInput(attrs={
                'type': 'date'
            }),
        }


class FeePaymentEditForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = FeePaymentModel
        exclude = ['type', 'user']
        widgets = {
            'date': DateInput(attrs={
                'type': 'date'
            }),
        }


class OnlinePaymentForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = OnlinePaymentModel
        fields = '__all__'
        widgets = {

        }


class OnlinePaymentEditForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = OnlinePaymentModel
        exclude = ['type', 'user']
        widgets = {

        }


class FeeReminderForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = FeeReminderModel
        fields = '__all__'
        widgets = {

        }


class FeeReminderEditForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = FeeReminderModel
        exclude = ['type', 'user']
        widgets = {

        }


class ExpenseCategoryForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = ExpenseCategoryModel
        fields = '__all__'
        widgets = {

        }


class ExpenseCategoryEditForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = ExpenseCategoryModel
        exclude = ['type', 'user']
        widgets = {

        }


class ExpenseTypeForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        division = False
        if 'type' in kwargs.keys():
            division = kwargs.pop('type')

        super().__init__(*args, **kwargs)
        if division:
            self.fields['category'].queryset = ExpenseCategoryModel.objects.filter(type=division).order_by('name')
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = ExpenseTypeModel
        fields = '__all__'
        widgets = {

        }


class ExpenseTypeEditForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        division = False
        if 'type' in kwargs.keys():
            division = kwargs.pop('type')

        super().__init__(*args, **kwargs)
        if division:
            self.fields['category'].queryset = ExpenseCategoryModel.objects.filter(type=division).order_by('name')
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = ExpenseTypeModel
        exclude = ['type', 'user']
        widgets = {

        }


class ExpenseForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        division = False
        if 'type' in kwargs.keys():
            division = kwargs.pop('type')

        super().__init__(*args, **kwargs)
        if division:
            self.fields['category'].queryset = ExpenseCategoryModel.objects.filter(type=division).order_by('name')
            self.fields['expense_type'].queryset = ExpenseTypeModel.objects.filter(type=division).order_by('name')
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = ExpenseModel
        fields = '__all__'
        widgets = {
            'date': TextInput(attrs={
                'type': 'date'
            })
        }


class ExpenseEditForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        division = False
        if 'type' in kwargs.keys():
            division = kwargs.pop('type')

        super().__init__(*args, **kwargs)
        if division:
            self.fields['category'].queryset = ExpenseCategoryModel.objects.filter(type=division).order_by('name')
            self.fields['expense_type'].queryset = ExpenseTypeModel.objects.filter(type=division).order_by('name')
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = ExpenseModel
        exclude = ['type', 'user', 'invoice_number']
        widgets = {
            'date': TextInput(attrs={
                'type': 'date'
            })
        }


class IncomeCategoryForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = IncomeCategoryModel
        fields = '__all__'
        widgets = {

        }


class IncomeCategoryEditForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = IncomeCategoryModel
        exclude = ['type', 'user']
        widgets = {

        }


class IncomeSourceForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = IncomeSourceModel
        fields = '__all__'
        widgets = {

        }


class IncomeSourceEditForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = IncomeSourceModel
        exclude = ['type', 'user']
        widgets = {

        }


class IncomeForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        division = False
        if 'type' in kwargs.keys():
            division = kwargs.pop('type')

        super().__init__(*args, **kwargs)
        if division:
            self.fields['category'].queryset = IncomeCategoryModel.objects.filter(type=division).order_by('name')
            self.fields['source'].queryset = IncomeSourceModel.objects.filter(type=division).order_by('name')
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = IncomeModel
        fields = '__all__'
        widgets = {
            'date': TextInput(attrs={
                'type': 'date'
            })
        }


class IncomeEditForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        division = False
        if 'type' in kwargs.keys():
            division = kwargs.pop('type')

        super().__init__(*args, **kwargs)
        if division:
            self.fields['category'].queryset = IncomeCategoryModel.objects.filter(type=division).order_by('name')
            self.fields['source'].queryset = IncomeSourceModel.objects.filter(type=division).order_by('name')
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = IncomeModel
        exclude = ['type', 'user', 'invoice_number']
        widgets = {
            'date': TextInput(attrs={
                'type': 'date'
            })
        }


class FinanceSettingCreateForm(ModelForm):
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
        model = FinanceSettingModel
        fields = '__all__'

        widgets = {

        }


class FinanceSettingEditForm(ModelForm):
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
        model = FinanceSettingModel
        exclude = ['type', 'user']

        widgets = {

        }
