from django.core.management.base import BaseCommand
from Subscriptions.forms import RegisterForm
from faker import Faker

class Command(BaseCommand):
    help = 'Generate 5 random users and register them with profiles'

    def handle(self, *args, **kwargs):
        fake = Faker()
        
        for _ in range(5):
            # Generate random data using Faker
            username = fake.user_name()
            email = fake.email()
            password = fake.password()

            data = {
                'username': username,
                'email': email,
                'password1': password,
                'password2': password,  # Passwords must match
            }

            # Create the RegisterForm instance
            form = RegisterForm(data=data)

            # Check if the form is valid
            if form.is_valid():
                user = form.register(commit=True)  # This will call the register() method
                self.stdout.write(self.style.SUCCESS(f'Successfully created user: {user.username}'))
            else:
                self.stdout.write(self.style.ERROR(f'Failed to create user: {username}'))
