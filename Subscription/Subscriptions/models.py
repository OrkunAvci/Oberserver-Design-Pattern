from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    def __str__(self):
        return self.user.username

class Publisher(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name="publisher")

    def __str__(self):
        return f"Publisher: {self.profile.user.username}"

class Subscriber(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name="subscriber")

    def __str__(self):
        return f"Subscriber: {self.profile.user.username}"

class Subscription(models.Model):
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE, related_name="subscriptions")
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, related_name="subscriptions")
    subscribed_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.subscriber.profile.user.username} subscribed to {self.publisher.profile.user.username}"

class Notification(models.Model):
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    receiver = models.ForeignKey(Subscriber, on_delete=models.CASCADE, related_name="notifications")
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, related_name="notifications")

    def __str__(self):
        return (f"Notification to {self.receiver.name} from {self.publisher.profile.user.username}")
