from django.urls import path, include
from user_management.views import *

urlpatterns = [

    path('sign-in', user_sign_in_view, name='login'),
    path('sign-out', user_sign_out_view, name='logout'),
    path('reset-password', user_reset_password_view, name='reset_password'),
    path('change-password', user_change_password_view, name='change_password'),
    path('user-profile', user_profile_view, name='user_profile'),

]
