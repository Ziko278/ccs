from django.contrib import admin
from finance.models import *


admin.site.register(FeePaymentModel)
admin.site.register(FinanceSettingModel)
admin.site.register(FeeDiscountGroupModel)