from django import template
from student.models import StudentsModel
from datetime import date, timedelta
from finance.models import *
from django.db.models import Sum
from school_setting.models import SchoolGeneralInfoModel

register = template.Library()


@register.filter
def get_amount_paid(fee_master, student_id):
    student = StudentsModel.objects.get(pk=student_id)
    type = student.type
    school_setting = SchoolGeneralInfoModel.objects.first()
    if school_setting.separate_school_section:
        finance_setting = FinanceSettingModel.objects.filter(type=type).first()
        academic_info = SchoolAcademicInfoModel.objects.filter(type=type).first()
    else:
        finance_setting = FinanceSettingModel.objects.first()
        academic_info = SchoolAcademicInfoModel.objects.first()

    if fee_master.fee.fee_occurrence == 'termly':
        payments = FeePaymentModel.objects.filter(fee=fee_master, student=student, session=academic_info.session,
                                                  term=academic_info.term, status='confirmed')
    else:
        payments = FeePaymentModel.objects.filter(fee=fee_master, session=academic_info.session, student=student,
                                                  status='confirmed')
    amount_paid = payments.aggregate(total_sum=Sum('amount'))['total_sum']

    if not amount_paid:
        return 0.0
    return amount_paid


@register.filter
def get_fee_discount(fee_master, student_id):
    student = StudentsModel.objects.get(pk=student_id)
    type = student.type
    school_setting = SchoolGeneralInfoModel.objects.first()
    if school_setting.separate_school_section:
        finance_setting = FinanceSettingModel.objects.filter(type=type).first()
        academic_info = SchoolAcademicInfoModel.objects.filter(type=type).first()
    else:
        finance_setting = FinanceSettingModel.objects.first()
        academic_info = SchoolAcademicInfoModel.objects.first()

    if not finance_setting.use_discount:
        return 0.0
    discount_group_list = FeeDiscountGroupModel.objects.filter(students__in=[student], status='active')
    discount_found = False
    discount = False

    for discount_group in discount_group_list:
        if discount_found:
            break
        for discount in discount_group.discounts.all():
            if discount.fee_master == fee_master:
                discount = discount
                discount_found = True
                break
    if not discount_found:
        return 0.0
    if discount.method == 'amount':
        return discount.amount
    if discount.method == 'percentage':
        if fee_master.fee.fee_occurrence != 'termly':
            amount = fee_master.amount
        else:
            if fee_master.same_termly_price:
                amount = fee_master.amount
            else:
                if academic_info.term == '1st term':
                    amount = fee_master.first_term_amount
                elif academic_info.term == '2nd term':
                    amount = fee_master.second_term_amount
                elif academic_info.term == '3rd term':
                    amount = fee_master.third_term_amount
        return round((discount.percentage/100 * amount), 1)


@register.filter
def get_fee_penalty(fee_master, student_id):
    student = StudentsModel.objects.get(pk=student_id)
    type = student.type
    school_setting = SchoolGeneralInfoModel.objects.first()
    if school_setting.separate_school_section:
        finance_setting = FinanceSettingModel.objects.filter(type=type).first()
        academic_info = SchoolAcademicInfoModel.objects.filter(type=type).first()
    else:
        finance_setting = FinanceSettingModel.objects.first()
        academic_info = SchoolAcademicInfoModel.objects.first()

    if not finance_setting.use_penalty:
        return 0.0

    total_penalty = 0.0
    penalty_list = FeePenaltyModel.objects.filter(fee_master=fee_master, status='active')
    for penalty in penalty_list:
        today = date.today()
        if penalty.date_reference == 'date':
            if not today >= penalty.due_date:
                continue
        elif penalty.date_reference == 'days':
            if academic_info.current_resumption_date and today >= academic_info.current_resumption_date:
                days_past = (today - academic_info.current_resumption_date).days
                if not days_past >= penalty.days_from_resumption:
                    continue
            else:
                continue
        if penalty.method == 'amount':
            total_penalty += penalty.amount
        if penalty.method == 'percentage':
            if fee_master.fee.fee_occurrence != 'termly':
                amount = fee_master.amount
            else:
                if fee_master.same_termly_price:
                    amount = fee_master.amount
                else:
                    if academic_info.term == '1st term':
                        amount = fee_master.first_term_amount
                    elif academic_info.term == '2nd term':
                        amount = fee_master.second_term_amount
                    elif academic_info.term == '3rd term':
                        amount = fee_master.third_term_amount
            total_penalty += round((penalty.percentage/100 * amount), 1)
    return total_penalty


@register.filter
def get_fee_balance(fee_master, student_id):
    student = StudentsModel.objects.get(pk=student_id)
    type = student.type
    school_setting = SchoolGeneralInfoModel.objects.first()
    if school_setting.separate_school_section:
        finance_setting = FinanceSettingModel.objects.filter(type=type).first()
        academic_info = SchoolAcademicInfoModel.objects.filter(type=type).first()
    else:
        finance_setting = FinanceSettingModel.objects.first()
        academic_info = SchoolAcademicInfoModel.objects.first()
    if fee_master.fee.fee_occurrence == 'termly':
        if not fee_master.same_termly_price:
            if academic_info.term == '1st term':
                total = fee_master.first_term_amount
            elif academic_info.term == '2nd term':
                total = fee_master.second_term_amount
            elif academic_info.term == '3rd term':
                total = fee_master.third_term_amount
        else:
            total = fee_master.amount
    else:
        total = fee_master.amount
    paid = get_amount_paid(fee_master, student_id)
    discount = get_fee_discount(fee_master, student_id)
    penalty = get_fee_penalty(fee_master, student_id)

    return total - paid - discount + penalty
