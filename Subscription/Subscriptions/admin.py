from django.contrib import admin
from .models import Profile, Publisher, Subscriber, Notification

app_name = "Subscriptions"

# Register the models
admin.site.register(Profile)
admin.site.register(Publisher)
admin.site.register(Subscriber)
admin.site.register(Notification)
