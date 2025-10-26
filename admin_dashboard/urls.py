from django.urls import path
from admin_dashboard.views import *

urlpatterns = [
    path('', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('site-is-under-maintenance', AdminMaintenanceView.as_view(), name='maintenance_view'),
    path('send-fee-mail', send_fee_summary_email, name='send_fee_summary_email'),
    path('fix-issue', fix_issue, name='fix_issue'),
    path('fix', fix_missing_student_profiles, name='fix'),

]

