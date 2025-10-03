from django.urls import path
from communication.views import *

urlpatterns = [

    path('smtp-configuration/create', SMTPConfigurationCreateView.as_view(), name='smtp_configuration_create'),
    path('smtp-configuration/index', SMTPConfigurationListView.as_view(), name='smtp_configuration_index'),
    path('smtp-configuration/<int:pk>/edit', SMTPConfigurationUpdateView.as_view(), name='smtp_configuration_edit'),
    path('smtp-configuration/<int:pk>/delete', SMTPConfigurationDeleteView.as_view(), name='smtp_configuration_delete'),

    path('email/send', send_email, name='send_email'),
    path('email/user-account-auto-send', send_user_account_auto_mail, name='user_account_auto_mail'),

    path('communication-info', CommunicationSettingView.as_view(), name='communication_info'),
    path('communication-info/create', CommunicationSettingCreateView.as_view(), name='communication_info_create'),
    path('communication-info/<int:pk>/update', CommunicationSettingUpdateView.as_view(), name='communication_info_update'),

]

