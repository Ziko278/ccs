from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from cryptography.fernet import Fernet
from num2words import num2words
from django.http import HttpResponse
from school_setting.models import SchoolAcademicInfoModel, SchoolGeneralInfoModel, SchoolSettingModel
from finance.models import OnlinePaymentModel, PaymentIDGeneratorModel, FeePaymentModel


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


def select_payment_method(request, student, fee, amount, amount_in_word, method, session, term):
    method = method.lower()
    school_setting = SchoolGeneralInfoModel.objects.first()
    if school_setting.separate_school_section:
        academic_setting = SchoolAcademicInfoModel.objects.filter(type=student.type).first()
        if method == 'paystack':
            secret_key = OnlinePaymentModel.objects.filter(type=student.type, name='paystack').first()
        elif method == 'flutterwave':
            secret_key = OnlinePaymentModel.objects.filter(type=student.type, name='flutterwave').first()
    else:
        academic_setting = SchoolAcademicInfoModel.objects.first()
        if method == 'paystack':
            secret_key = OnlinePaymentModel.objects.filter(name='paystack').first()
        elif method == 'flutterwave':
            secret_key = OnlinePaymentModel.objects.filter(name='flutterwave').first()

    key = secret_key.key
    fernet = Fernet(key)
    vat = round(secret_key.vat/100*float(amount), 2)
    total = float(amount) + vat
    callback_url = ''
    if method == 'paystack':
        callback_url = reverse('verify_paystack_payment')
    elif method == 'flutterwave':
        callback_url = reverse('verify_flutterwave_payment')

    if request.method == 'POST':
        pass
    context = {
        'secret_key': fernet.decrypt(secret_key.public_key.encode()).decode(),
        'student': student,
        'fee': fee,
        'amount': amount,
        'amount_in_word': amount_in_word,
        'vat': vat,
        'percentage_vat': secret_key.vat,
        'total': total,
        'total_in_word': num2words(total),
        'email': secret_key.email,
        'method': method,
        'session': session,
        'term': term,
        'academic_setting': academic_setting,
        'reference': generate_payment_id(student.type),
        'callback_url': callback_url
    }
    return render(request, 'finance/online_payment/online_payment.html', context)



