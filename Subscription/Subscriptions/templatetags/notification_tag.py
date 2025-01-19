from django import template
from Subscriptions.models import Notification

register = template.Library()

@register.inclusion_tag('notification_content.html')
def show_notifications(user):
    notifications = Notification.objects.filter(receiver=user.profile.subscriber, is_read=False).order_by('-timestamp')
    return {'notifications': notifications}
