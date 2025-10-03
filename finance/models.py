from django.db import models
from django.contrib.auth.models import User
from cryptography.fernet import Fernet
from django.db.models import Sum
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from datetime import date
from django.utils import timezone
from school_setting.models import SchoolSettingModel, SessionModel
from student.models import StudentsModel
from academic.models import *
from school_setting.models import SchoolAcademicInfoModel, SchoolGeneralInfoModel
from admin_dashboard.storage_backends import MediaStorage


def generate_payment_id(type):
    setting = SchoolGeneralInfoModel.objects.first()
    if setting.school_type == 'mix' and setting.separate_school_section:
        last_payment = PaymentIDGeneratorModel.objects.filter(type=type).last()
    else:
        last_payment = PaymentIDGeneratorModel.objects.filter().last()
    if last_payment:
        payment_id = str(int(last_payment.last_id) + 1)
    else:
        payment_id = str(1)
    while True:
        gen_id = payment_id
        if setting.school_type == 'mix':
            payment_id = type[0] + 'trn' + '-' + payment_id.rjust(8, '0')
        else:
            payment_id = 'trn' + '-' + payment_id.rjust(8, '0')
        payment_exist = FeePaymentModel.objects.filter(reference=payment_id).first()
        if not payment_exist:
            break
        else:
            payment_id = str(int(gen_id) + 1)

    generate_id = PaymentIDGeneratorModel.objects.create(last_id=gen_id, last_payment_id=payment_id,
                                                         status='f', type=type)
    generate_id.save()

    return payment_id


class FeeModel(models.Model):
    name = models.CharField(max_length=250)
    code = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    FEE_OCCURRENCE = (
        ('termly', 'TERMLY'), ('annually', 'ANNUALLY'), ('one time', 'ONE TIME')
    )
    fee_occurrence = models.CharField(max_length=50, choices=FEE_OCCURRENCE)

    PAYMENT_TERM = (
        ('1st term', 'FIRST TERM'), ('2nd term', 'SECOND TERM'), ('3rd term', 'THIRD TERM'),
        ('any term', 'ANY TERM'),
    )
    payment_term = models.CharField(max_length=50, choices=PAYMENT_TERM, null=True, blank=True, default='first term')

    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY'), ('mix', 'GENERAL')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='fee_updated_by')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'type'],
                name='unique_fee_name_type_combo',
            )
        ]

    def __str__(self):
        return self.name.upper()

    def fee_paid(self):
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            academic_setting = SchoolAcademicInfoModel.objects.filter(type=self.type).first()
        else:
            academic_setting = SchoolAcademicInfoModel.objects.first()
        session = academic_setting.session
        term = academic_setting.term
        fee_payment = FeePaymentModel.objects.filter(fee__fee=self, session=session, term=term)
        amount_paid = fee_payment.aggregate(total_sum=Sum('amount'))['total_sum']

        if not amount_paid:
            return 0.0
        return amount_paid

    def save(self, *args, **kwargs):
        if self.fee_occurrence == 'termly':
            self.payment_term = None
        super(FeeModel, self).save(*args, **kwargs)


class FeeGroupModel(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)

    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY'), ('mix', 'GENERAL')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='fee_group_updated_by')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'type'],
                name='unique_fee_group_type_combo',
            )
        ]

    def __str__(self):
        return self.name.upper()


class FeeMasterModel(models.Model):
    group = models.ForeignKey(FeeGroupModel, on_delete=models.CASCADE)
    fee = models.ForeignKey(FeeModel, on_delete=models.CASCADE)
    student_class = models.ManyToManyField(ClassesModel, blank=True)
    class_section = models.ManyToManyField(ClassSectionModel, blank=True)
    same_termly_price = models.BooleanField(blank=True, null=True, default=True)
    amount = models.FloatField(null=True, blank=True, default=0)
    first_term_amount = models.FloatField(null=True, blank=True)
    second_term_amount = models.FloatField(null=True, blank=True)
    third_term_amount = models.FloatField(null=True, blank=True)
    is_new = models.BooleanField(default=False, blank=True)
    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY'), ('mix', 'GENERAL')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='fee_master_updated_by')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return "{} for {}".format(self.fee.name.title(), self.group.name.title())

    def save(self, *args, **kwargs):
        if self.fee.fee_occurrence != 'termly':
            self.same_termly_price = False
        super(FeeMasterModel, self).save(*args, **kwargs)

    def amount_paid(self, student_id):
        return student_id


class FeeDiscountModel(models.Model):
    fee_master = models.ForeignKey(FeeMasterModel, on_delete=models.CASCADE)
    METHOD = (
        ('amount', 'AMOUNT'), ('percentage', 'PERCENTAGE')
    )
    method = models.CharField(max_length=20, choices=METHOD)
    percentage = models.FloatField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)

    STATUS = (
        ('active', 'ACTIVE'), ('inactive', 'INACTIVE')
    )
    status = models.CharField(max_length=20, choices=STATUS)
    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY'), ('mix', 'GENERAL')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='fee_discount_updated_by')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return "{} for {}".format(self.fee_master.fee.name.title(), self.fee_master.group.name.title())


class FeeDiscountGroupModel(models.Model):
    name = models.CharField(max_length=250)
    discounts = models.ManyToManyField(FeeDiscountModel, blank=True)
    students = models.ManyToManyField(StudentsModel, blank=True)
    STATUS = (
        ('active', 'ACTIVE'), ('inactive', 'INACTIVE')
    )
    status = models.CharField(max_length=20, choices=STATUS)
    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY'), ('mix', 'GENERAL')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='fee_discount_group_updated_by')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.name.title()


class FeePenaltyModel(models.Model):
    fee_master = models.ForeignKey(FeeMasterModel, on_delete=models.CASCADE)
    METHOD = (
        ('amount', 'AMOUNT'), ('percentage', 'PERCENTAGE')
    )
    method = models.CharField(max_length=20, choices=METHOD)
    amount = models.FloatField(blank=True, null=True)
    percentage = models.FloatField(blank=True, null=True)
    DATE_REFERENCE = (
        ('days', 'DAYS FROM RESUMPTION'), ('date', 'SELECTED DATE')
    )
    date_reference = models.CharField(max_length=20, choices=DATE_REFERENCE)
    days_from_resumption = models.IntegerField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)

    STATUS = (
        ('active', 'ACTIVE'), ('inactive', 'INACTIVE')
    )
    status = models.CharField(max_length=20, choices=STATUS)
    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY'), ('mix', 'GENERAL')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='fee_penalty_updated_by')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return "{} for {}".format(self.fee_master.fee.name.title(), self.fee_master.group.name.title())


class FeeReminderModel(models.Model):
    fee = models.ForeignKey(FeeModel, on_delete=models.CASCADE)
    time = models.TimeField()
    days_after_resumption = models.IntegerField(default=0)
    number_of_reminders = models.IntegerField(default=0)
    interval_in_days = models.IntegerField(default=0)
    FORMAT = (
        ('sms', 'SMS'), ('email', 'EMAIL'), ('both', 'BOTH')
    )
    format = models.CharField(max_length=20, choices=FORMAT)
    METHOD = (
        ('manual', 'MANUAL'), ('automatic', 'AUTOMATIC'), ('any', 'ANY')
    )
    method = models.CharField(max_length=20, choices=METHOD)
    RECIPIENT = (
        ('student', 'STUDENT'), ('parent', 'PARENT'), ('both', 'BOTH')
    )
    recipient = models.CharField(max_length=20, choices=RECIPIENT)
    STATUS = (
        ('active', 'ACTIVE'), ('inactive', 'INACTIVE')
    )
    status = models.CharField(max_length=20, choices=STATUS)
    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY'), ('mix', 'GENERAL')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='fee_reminder_updated_by')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


class FeeReminderRecordModel(models.Model):
    reminder = models.ForeignKey(FeeReminderModel, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    session = models.ForeignKey(SessionModel, on_delete=models.CASCADE)
    TERM = (
        ('1st term', '1st Term'), ('2nd term', '2ndTerm'), ('3rd term', '3rd Term')
    )
    term = models.CharField(max_length=20, choices=TERM)
    number_of_text_recipient = models.IntegerField(default=0)
    number_of_email_recipient = models.IntegerField(default=0)
    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY'), ('mix', 'GENERAL')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, blank=True)


class FeePaymentModel(models.Model):
    fee = models.ForeignKey(FeeMasterModel, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentsModel, on_delete=models.CASCADE)
    session = models.ForeignKey(SessionModel, on_delete=models.CASCADE)
    TERM = (
        ('1st term', '1st Term'), ('2nd term', '2ndTerm'), ('3rd term', '3rd Term')
    )
    term = models.CharField(max_length=20, choices=TERM)
    PAYMENT_MODE = (
        ('cash', 'CASH'), ('pos', 'POS'), ('bank', 'BANK TELLER'), ('transfer', 'BANK TRANSFER')
    )
    payment_mode = models.CharField(max_length=20, choices=PAYMENT_MODE)
    METHOD = (('paystack', 'PAYSTACK'), ('flutterwave', 'FLUTTERWAVE'))
    online_payment_method = models.CharField(max_length=100, choices=METHOD, null=True, blank=True)
    vat = models.FloatField(default=0, blank=True, null=True)
    date = models.DateField(default=date.today(), blank=True)
    payment_proof = models.FileField(blank=True, null=True, storage=MediaStorage(), upload_to='finance/fee_payment')
    amount = models.FloatField()
    reference = models.CharField(max_length=100, blank=True, null=True)
    STATUS = (
        ('pending', 'PENDING'), ('confirmed', 'CONFIRMED')
    )
    status = models.CharField(max_length=20, choices=STATUS, default='pending', blank=True)
    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY'), ('mix', 'GENERAL')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = generate_payment_id(self.type)
        super(FeePaymentModel, self).save(*args, **kwargs)


class FeePaymentSummaryModel(models.Model):
    fees = models.ManyToManyField(FeePaymentModel, related_name='payment_summary')
    student = models.ForeignKey(StudentsModel, on_delete=models.CASCADE)
    session = models.ForeignKey(SessionModel, on_delete=models.CASCADE)
    TERM = (
        ('1st term', '1st Term'), ('2nd term', '2ndTerm'), ('3rd term', '3rd Term')
    )
    term = models.CharField(max_length=20, choices=TERM)
    PAYMENT_MODE = (
        ('cash', 'CASH'), ('cheque', 'CHEQUE'), ('bank', 'BANK TELLER'), ('transfer', 'BANK TRANSFER')
    )
    payment_mode = models.CharField(max_length=20, choices=PAYMENT_MODE)
    METHOD = (('paystack', 'PAYSTACK'), ('flutterwave', 'FLUTTERWAVE'), ('quickteller', 'QUICKTELLER'),
              ('interswitch', 'INTERSWITCH'))
    online_payment_method = models.CharField(max_length=100, choices=METHOD, null=True, blank=True)
    vat = models.FloatField(default=0)
    date = models.DateField(default=date.today(), blank=True)
    payment_proof = models.FileField(blank=True, null=True, storage=MediaStorage(), upload_to='finance/fee_payment')
    amount = models.FloatField()
    reference = models.CharField(max_length=100, blank=True, null=True)
    STATUS = (
        ('pending', 'PENDING'), ('confirmed', 'CONFIRMED')
    )
    status = models.CharField(max_length=20, choices=STATUS, default='pending', blank=True)
    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY'), ('mix', 'GENERAL')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = generate_payment_id(self.type)
        super(FeePaymentSummaryModel, self).save(*args, **kwargs)

    def fee_list(self):
        if len(self.fees.all()) == 0:
            return '---------'
        if len(self.fees.all()) == 1:
            return self.fees.first().fee.fee.name.title()
        if len(self.fees.all()) > 2:
            s = 's'
        else:
            s = ''
        return "{} & {} other fee{}".format(self.fees.first().fee.fee.name.title(), len(self.fees.all())-1, s)


class OutstandingFeeModel(models.Model):
    student = models.ForeignKey(StudentsModel, on_delete=models.CASCADE)
    session = models.ForeignKey(SessionModel, on_delete=models.CASCADE)
    term = models.CharField(max_length=20)
    fee_master = models.ForeignKey(FeeMasterModel, on_delete=models.CASCADE)
    total_amount = models.FloatField()
    outstanding_amount = models.FloatField()
    paid = models.FloatField(default=0)
    balance = models.FloatField(null=True)
    STATUS = (
        ('active', 'ACTIVE'), ('inactive', 'INACTIVE')
    )
    status = models.CharField(max_length=20, choices=STATUS, default='active')

    def save(self, *args, **kwargs):
        self.balance = self.outstanding_amount - self.paid
        super(OutstandingFeeModel, self).save(*args, **kwargs)


class OnlinePaymentModel(models.Model):
    METHOD = (('paystack', 'PAYSTACK'), ('flutterwave', 'FLUTTERWAVE'))

    name = models.CharField(max_length=250, choices=METHOD)
    public_key = models.CharField(max_length=250)
    private_key = models.CharField(max_length=250)
    email = models.EmailField()
    vat = models.FloatField(default=0.0)
    callback_url = models.URLField(blank=True, null=True)
    webhook_url = models.URLField(blank=True, null=True)
    key = models.CharField(max_length=250, blank=True, null=True)
    STATUS = (
        ('active', 'ACTIVE'), ('inactive', 'INACTIVE')
    )
    status = models.CharField(max_length=20, choices=STATUS, default='active', blank=True)

    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY'), ('mix', 'GENERAL')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='online_payment_method_updated_by')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.name.upper()

    def save(self, *args, **kwargs):
        key = Fernet.generate_key().decode()
        fernet = Fernet(key)
        self.key = key
        self.public_key = fernet.encrypt(self.public_key.encode()).decode()
        self.private_key = fernet.encrypt(self.private_key.encode()).decode()
        super(OnlinePaymentModel, self).save(*args, **kwargs)


class FinanceSettingModel(models.Model):
    use_discount = models.BooleanField(default=False)
    use_penalty = models.BooleanField(default=False)
    use_2fa_manual = models.BooleanField(default=False)
    use_2fa_online = models.BooleanField(default=False)
    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY'), ('mix', 'GENERAL')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='finance_setting_updated_by')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


class ExpenseCategoryModel(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY'), ('mix', 'GENERAL')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='expense_category_updated_by')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'type'],
                name='unique_expense_source_type_combo',
                violation_error_message='Expense Category Already Exists'
            )
        ]

    def __str__(self):
        return self.name.upper()

    def no_of_expenses(self):
        return ExpenseModel.objects.filter(category=self).count()


class ExpenseTypeModel(models.Model):
    name = models.CharField(max_length=250)
    category = models.ForeignKey(ExpenseCategoryModel, on_delete=models.CASCADE, related_name='category_types')
    description = models.TextField(null=True, blank=True)
    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY'), ('mix', 'GENERAL')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='expense_type_updated_by')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.name.upper()

    def no_of_expenses(self):
        return ExpenseModel.objects.filter(expense_type=self).count()


class ExpenseModel(models.Model):
    expense_type = models.ForeignKey(ExpenseTypeModel, on_delete=models.CASCADE)
    category = models.ForeignKey(ExpenseCategoryModel, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    amount = models.FloatField()
    date = models.DateTimeField(blank=True, default=date.today())
    expense_proof = models.FileField(upload_to='finance/expense', storage=MediaStorage(), blank=True, null=True)
    session = models.ForeignKey(SessionModel, on_delete=models.CASCADE, blank=True)
    TERM = (
        ('1st term', '1st Term'), ('2nd term', '2nd Term'), ('3rd term', '3rd Term')
    )
    term = models.CharField(max_length=20, choices=TERM, blank=True)
    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY'), ('mix', 'GENERAL')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='expense_updated_by')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            academic_info = SchoolAcademicInfoModel.objects.filter(type=self.type).first()
        else:
            academic_info = SchoolAcademicInfoModel.objects.first()
        self.session = academic_info.session
        self.term = academic_info.term
        if not self.invoice_number:
            self.invoice_number = generate_payment_id(self.type)
        super(ExpenseModel, self).save(*args, **kwargs)


class IncomeCategoryModel(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY'), ('mix', 'GENERAL')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='income_category_updated_by')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'type'],
                name='unique_income_category_type_combo',
                violation_error_message='Income Category Already Exists'
            )
        ]

    def __str__(self):
        return self.name.upper()

    def no_of_incomes(self):
        return IncomeModel.objects.filter(category=self).count()


class IncomeSourceModel(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY'), ('mix', 'GENERAL')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='income_source_updated_by')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'type'],
                name='unique_income_source_type_combo',
                violation_error_message='Income Source Already Exists'
            )
        ]

    def __str__(self):
        return self.name.upper()

    def no_of_incomes(self):
        return IncomeModel.objects.filter(source=self).count()


class IncomeModel(models.Model):
    category = models.ForeignKey(IncomeCategoryModel, on_delete=models.CASCADE)
    source = models.ForeignKey(IncomeSourceModel, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    amount = models.FloatField()
    date = models.DateTimeField(blank=True, default=date.today())
    income_proof = models.FileField(upload_to='finance/income', storage=MediaStorage(), blank=True, null=True)
    session = models.ForeignKey(SessionModel, on_delete=models.CASCADE, blank=True)
    TERM = (
        ('1st term', '1st Term'), ('2nd term', '2ndTerm'), ('3rd term', '3rd Term')
    )
    term = models.CharField(max_length=20, choices=TERM, blank=True)
    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY'), ('mix', 'GENERAL')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='income_updated_by')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['invoice_number', 'type'],
                name='unique_income_invoice_type_combo',
                violation_error_message='Income Source Already Exists'
            )
        ]

    def __str__(self):
        return self.category.name.upper()

    def save(self, *args, **kwargs):
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            academic_info = SchoolAcademicInfoModel.objects.filter(type=self.type).first()
        else:
            academic_info = SchoolAcademicInfoModel.objects.first()
        self.session = academic_info.session
        self.term = academic_info.term
        if not self.invoice_number:
            self.invoice_number = generate_payment_id(self.type)
        super(IncomeModel, self).save(*args, **kwargs)


class StaffLoanModel(models.Model):
    staff = models.ForeignKey(StaffModel, on_delete=models.CASCADE)
    amount = models.FloatField()
    session = models.ForeignKey(SessionModel, on_delete=models.CASCADE)
    TERM = (
        ('1st term', '1st Term'), ('2nd term', '2ndTerm'), ('3rd term', '3rd Term')
    )
    term = models.CharField(max_length=20, choices=TERM)
    date = models.DateField(blank=True, auto_now_add=True)
    confirmation_date = models.DateField(auto_now=True)
    STATUS = (
        ('pending', 'PENDING'), ('confirmed', 'CONFIRMED')
    )
    status = models.CharField(max_length=20, choices=STATUS, default='pending', blank=True)
    is_refunded = models.BooleanField(default=False)


class StaffDeductionModel(models.Model):
    staff = models.ForeignKey(StaffModel, on_delete=models.CASCADE)
    amount = models.FloatField()
    purpose = models.TextField(null=True, blank=True)
    session = models.ForeignKey(SessionModel, on_delete=models.CASCADE)
    TERM = (
        ('1st term', '1st Term'), ('2nd term', '2ndTerm'), ('3rd term', '3rd Term')
    )
    term = models.CharField(max_length=20, choices=TERM)
    date = models.DateField(auto_now_add=True)
    STATUS = (
        ('pending', 'PENDING'), ('confirmed', 'CONFIRMED')
    )
    status = models.CharField(max_length=20, choices=STATUS, default='pending', blank=True)


class StaffBonusModel(models.Model):
    staff = models.ForeignKey(StaffModel, on_delete=models.CASCADE)
    amount = models.FloatField()
    subject = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    session = models.ForeignKey(SessionModel, on_delete=models.CASCADE)
    TERM = (
        ('1st term', '1st Term'), ('2nd term', '2ndTerm'), ('3rd term', '3rd Term')
    )
    term = models.CharField(max_length=20, choices=TERM)
    date = models.DateField(auto_now_add=True)
    STATUS = (
        ('pending', 'PENDING'), ('confirmed', 'CONFIRMED')
    )
    status = models.CharField(max_length=20, choices=STATUS, default='pending', blank=True)


class PayrollModel(models.Model):
    staff = models.ForeignKey(StaffModel, on_delete=models.CASCADE)
    salary = models.FloatField()
    loan_deduction = models.FloatField()
    other_deduction = models.FloatField()
    bonus = models.FloatField()
    payable = models.FloatField()
    amount_paid = models.FloatField()
    balance = models.FloatField()
    session = models.ForeignKey(SessionModel, on_delete=models.CASCADE)
    TERM = (
        ('1st term', '1st Term'), ('2nd term', '2ndTerm'), ('3rd term', '3rd Term')
    )
    term = models.CharField(max_length=20, choices=TERM)
    date = models.DateField(auto_now_add=True)
    STATUS = (
        ('pending', 'PENDING'), ('confirmed', 'CONFIRMED')
    )
    status = models.CharField(max_length=20, choices=STATUS, default='pending', blank=True)


class BudgetModel(models.Model):
    category = models.ForeignKey(ExpenseCategoryModel, on_delete=models.CASCADE)
    DURATION = (('w', 'WEEK'), ('m', 'MONTH'), ('t', 'TERM'), ('s', 'SESSION'))
    budget = models.FloatField()
    session = models.ForeignKey(SessionModel, on_delete=models.CASCADE)
    TERM = (
        ('1st term', '1st Term'), ('2nd term', '2ndTerm'), ('3rd term', '3rd Term')
    )
    term = models.CharField(max_length=20, choices=TERM)
    date = models.DateField(blank=True, auto_now_add=True)
    STATUS = (
        ('pending', 'PENDING'), ('confirmed', 'CONFIRMED')
    )
    status = models.CharField(max_length=20, choices=STATUS, default='pending', blank=True)


class PaymentIDGeneratorModel(models.Model):
    last_id = models.IntegerField()
    last_payment_id = models.CharField(max_length=100, null=True, blank=True)
    STATUS = (
        ('s', 'SUCCESS'), ('f', 'FAIL')
    )
    status = models.CharField(max_length=10, choices=STATUS, blank=True, default='f')

    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True)


class FeeRecordModel(models.Model):
    session = models.ForeignKey(SessionModel, on_delete=models.CASCADE)
    TERM = (
        ('1st term', '1st Term'), ('2nd term', '2ndTerm'), ('3rd term', '3rd Term')
    )
    term = models.CharField(max_length=20, choices=TERM)
    total_payable = models.FloatField()
    total_paid = models.FloatField()
    total_discount = models.FloatField(default=0)
    total_penalty = models.FloatField(default=0)
    total_balance = models.FloatField(default=0)
    overall_balance = models.FloatField(default=0)
    class_fee_record = models.JSONField(null=True)
    TYPE = (
        ('pri', 'PRIMARY'), ('sec', 'SECONDARY')
    )
    type = models.CharField(max_length=10, choices=TYPE, blank=True)


