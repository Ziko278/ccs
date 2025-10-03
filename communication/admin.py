from django.contrib import admin
from communication.models import CommunicationSettingModel, RecentActivityModel

admin.site.register(CommunicationSettingModel)
admin.site.register(RecentActivityModel)
