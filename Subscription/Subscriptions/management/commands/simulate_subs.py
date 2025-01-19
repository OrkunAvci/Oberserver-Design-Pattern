from django.core.management.base import BaseCommand
from Subscriptions.models import Profile, Subscription
import random

class Command(BaseCommand):
    help = 'Simulate random subscriptions between users'

    def handle(self, *args, **kwargs):
        # Fetch profiles excluding the current logged-in user
        profiles = Profile.objects.all()

        for subscriber_profile in profiles:
            available_profiles = [profile for profile in profiles if profile != subscriber_profile]

            for _ in range(random.randint(1, 3)):
                publisher_profile = random.choice(available_profiles)
                
                subscriber = subscriber_profile.subscriber
                publisher = publisher_profile.publisher

                subscription, created = Subscription.objects.get_or_create(
                    subscriber=subscriber,
                    publisher=publisher
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f'Successfully created subscription: {subscriber_profile.user.username} -> {publisher_profile.user.username}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Subscription already exists: {subscriber_profile.user.username} -> {publisher_profile.user.username}'))

        self.stdout.write(self.style.SUCCESS('Successfully simulated subscriptions between users!'))
