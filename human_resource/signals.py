from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from human_resource.models import StaffModel, StaffIDGeneratorModel
from django.contrib.auth.models import User
from user_management.models import UserProfileModel
from django.utils.crypto import get_random_string


@receiver(post_save, sender=StaffModel)
def create_staff_account(sender, instance, created, **kwargs):
    if created:
        staff = instance
        email = staff.email
        username = email if email else staff.staff_id
        password = staff.password if staff.password else get_random_string(8)

        user = User.objects.create_user(username=username, email=email, password=password, is_active=True, is_staff=True)
        user_profile = UserProfileModel.objects.create(user=user, reference_id=staff.id, staff=staff, reference='staff',
                                                       default_password=password, type=staff.type)
        user_profile.save()

        if staff.group:
            staff.group.user_set.add(user)

        id_generator = StaffIDGeneratorModel.objects.filter(last_staff_id=staff.staff_id).last()
        id_generator.status = 's'
        id_generator.save()
