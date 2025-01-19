import random
from django.core.management.base import BaseCommand
from Subscriptions.models import Notification, Publisher, Subscriber

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        LOREM_IPSUM_TEXTS = [
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
    "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
    "Ut enim ad minim veniam, quis nostrud exercitation ullamco.",
    "Duis aute irure dolor in reprehenderit in voluptate velit esse.",
    "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia.",
    "Curabitur pretium tincidunt lacus. Nulla gravida orci a odio.",
    "Pellentesque in ipsum id orci porta dapibus.",
    "Vivamus magna justo, lacinia eget consectetur sed, convallis at tellus.",
    "Proin eget tortor risus. Nulla porttitor accumsan tincidunt.",
    "Mauris blandit aliquet elit, eget tincidunt nibh pulvinar a."
]
        count = 50

        publishers = list(Publisher.objects.all())
        subscribers = list(Subscriber.objects.all())

        if not publishers or not subscribers:
            self.stdout.write(self.style.ERROR('No publishers or subscribers found.'))
            return

        for notification in range(count):
            publisher = random.choice(publishers)
            subscriber = random.choice(subscribers)
            content = random.choice(LOREM_IPSUM_TEXTS)

            Notification.objects.create(
                content=content,
                receiver=subscriber,
                publisher=publisher,
                is_read=False
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully created {count} notifications.'))
