# management/commands/create_student_wallets.py
from django.core.management.base import BaseCommand
from django.db import transaction
from student.models import StudentsModel, StudentWalletModel


class Command(BaseCommand):
    help = 'Create wallets for all students without one'

    def handle(self, *args, **options):
        students_without_wallet = StudentsModel.objects.filter(student_wallet__isnull=True)
        total = students_without_wallet.count()

        if total == 0:
            self.stdout.write(self.style.SUCCESS('All students already have wallets!'))
            return

        self.stdout.write(f'Found {total} students without wallets. Creating...')

        created = 0
        with transaction.atomic():
            for student in students_without_wallet:
                StudentWalletModel.objects.create(student=student)
                created += 1

        self.stdout.write(self.style.SUCCESS(f'✓ Successfully created {created} wallets'))