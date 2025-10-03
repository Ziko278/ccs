from school_setting.models import SchoolGeneralInfoModel, SchoolAcademicInfoModel
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from django.shortcuts import redirect


def school_info(request):
    info = SchoolGeneralInfoModel.objects.first()
    academic_info = None
    if not info:
        return {}
    try:
        user_type = request.user.profile.type
    except AttributeError:
        user_type = None

    if info.separate_school_section and not request.user.is_anonymous:
        academic_info = SchoolAcademicInfoModel.objects.filter(type=user_type).first()
    else:
        academic_info = SchoolAcademicInfoModel.objects.first()

    return {
        'school_info': info,
        'academic_info': academic_info
    }
