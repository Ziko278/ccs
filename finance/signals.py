from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from finance.models import FeePaymentModel, FinanceSettingModel
from django.contrib.auth.models import User
from user_management.models import UserProfileModel
from communication.models import RecentActivityModel
from school_setting.models import SchoolAcademicInfoModel, SchoolGeneralInfoModel


@receiver(post_save, sender=FeePaymentModel)
def create_parent_account(sender, instance, created, **kwargs):
    if created:
        payment = instance
        school_setting = SchoolGeneralInfoModel.objects.first()
        if school_setting.separate_school_section:
            fee_setting = FinanceSettingModel.objects.filter(type=payment.type).first()
        else:
            fee_setting = FinanceSettingModel.objects.first()
        if payment.payment_mode == 'online':
            if fee_setting.use_2fa_online:
                payment.status = 'pending'
            else:
                payment.status = 'confirmed'
        else:
            if fee_setting.use_2fa_manual:
                payment.status = 'pending'
            else:
                payment.status = 'confirmed'

        payment.save()


