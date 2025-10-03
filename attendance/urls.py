from django.urls import path
from attendance.views import *

urlpatterns = [
    path('take-daily-attendance', DailyAttendanceView.as_view(), name='take_daily_attendance'),
    path('select-attendance-check', check_general_attendance_select_date, name='check_general_attendance_select_date'),
    path('check/<str:date>', check_general_attendance, name='check_general_attendance'),

    path('select-class-attendance', daily_attendance_select_class, name='class_attendance_select_class'),
    path('<int:pk>/<str:date>/take-class-attendance', daily_class_attendance, name='class_attendance'),

    path('select-class-attendance-check', check_attendance_select_class, name='check_class_attendance_select_class'),
    path('<int:pk>/<str:date>/check-class-attendance', check_class_attendance, name='check_class_attendance'),

    path('daily-attendance-api', daily_attendance_api, name='daily_attendance_api'),

]

