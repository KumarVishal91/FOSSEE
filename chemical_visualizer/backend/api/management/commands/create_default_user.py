"""
Management command to create a default admin user for quick setup.
Usage: python manage.py create_default_user
"""
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Creates a default admin user (username: admin, password: admin123)"

    def handle(self, *args, **options):
        if User.objects.filter(username="admin").exists():
            self.stdout.write(self.style.WARNING("User 'admin' already exists."))
        else:
            User.objects.create_superuser(
                username="admin",
                email="admin@example.com",
                password="admin123",
            )
            self.stdout.write(self.style.SUCCESS("Successfully created admin user."))
            self.stdout.write("Username: admin")
            self.stdout.write("Password: admin123")
