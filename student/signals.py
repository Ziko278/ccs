from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from student.models import *
from django.contrib.auth.models import User
from user_management.models import UserProfileModel
from communication.models import RecentActivityModel
from school_setting.models import SchoolAcademicInfoModel
from django.utils.crypto import get_random_string


def assign_class_number(student_class, class_section):
    number = StudentsModel.objects.filter(student_class=student_class, class_section=class_section).count()
    while 1:
        student = StudentsModel.objects.filter(student_class=student_class, class_section=class_section, class_number=number)
        if student:
            number += 1
        else:
            break
    return number


@receiver(post_save, sender=ParentsModel)
def create_parent_account(sender, instance, created, **kwargs):
    if created:
        parent = instance
        username = parent.parent_id
        password = get_random_string(8)
        email = parent.email

        user = User.objects.create_user(username=username, email=email, password=password)
        user_profile = UserProfileModel.objects.create(user=user, reference_id=parent.id, parent=parent,
                                                       reference='parent',
                                                       default_password=password)
        user_profile.save()


# 


@receiver(post_save, sender=StudentsModel)
def create_student_record(sender, instance, created, **kwargs):
    if created:
        student = instance
        academic_info = SchoolAcademicInfoModel.objects.first()
        student_record = StudentAcademicRecordModel.objects.create(student=student, entry_class=student.student_class,
                                                                   entry_class_section=student.class_section,
                                                                   entry_age=student.age,
                                                                   entry_session=academic_info.session,
                                                                   entry_term=academic_info.term)
        student_record.save()


@receiver(post_save, sender=StudentsModel)
def create_registration_notification(sender, instance, created, **kwargs):
    if created:
        category = 'student_registration'
        subject = "<b>{} {}</b> just completed student registration to <b>{} {}</b>".format(instance.surname.title(),
                  instance.last_name.title(), instance.student_class.name.upper(),
                  instance.class_section.name.upper())
        activity = RecentActivityModel.objects.create(category=category, subject=subject, reference_id=instance.id, type=instance.type)
        activity.save()
