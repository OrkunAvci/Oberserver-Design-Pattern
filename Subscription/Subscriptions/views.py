from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, LoginForm
from .models import Notification, Profile, Subscription

def index(request):
	context = {}
	if request.user.is_authenticated:
		# Exclude the current user's profile from the list
		context["profiles"] = Profile.objects.exclude(id=request.user.profile.id).exclude(
		id__in=Subscription.objects.filter(subscriber=request.user.profile.subscriber).values('publisher__profile_id')
	)
	else:
		# If not authenticated, send an empty profile list or show a message
		context["profiles"] = Profile.objects.all()
	

	if request.method == 'POST':
		target_profile_id = request.POST.get('target_profile_id')
		action = request.POST.get('action')

		if target_profile_id and action:
			target_profile = Profile.objects.get(id=target_profile_id)
			subscription, created = Subscription.objects.get_or_create(
				subscriber=request.user.profile.subscriber, publisher=target_profile.publisher
			)

			if action == 'subscribe' and created:
				subscription.save()

			return redirect('Subscriptions:index')

	return render(request=request, template_name="index.html", context=context)


def register(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			user = form.register()
			auth_login(request, user)
			return redirect('Subscriptions:index')
		else:
			print(form.errors)
			return render(request, 'register.html')
	else:
		return render(request, 'register.html')

def login(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			if form.login(request):
				return redirect('Subscriptions:profile')
			else:
				return render(request, 'login.html', {'error': 'Invalid username or password'})
		else:
			return render(request, 'login.html')
	else:
		return render(request, 'login.html')

@login_required
def logout(request):
	auth_logout(request)
	return redirect('Subscriptions:index')

@login_required
def profile(request):
	user_profile = request.user.profile

	subscriptions = Subscription.objects.filter(subscriber=user_profile.subscriber)
	publishers = [sub.publisher.profile for sub in subscriptions]

	subscribers = Subscription.objects.filter(publisher=user_profile.publisher)
	subscriber_profiles = [sub.subscriber.profile for sub in subscribers]

	context = {
		'profile': user_profile,
		'publishers': publishers,
		'subscribers': subscriber_profiles
	}

	if request.method == 'POST':
		target_profile_id = request.POST.get('target_profile_id')
		action = request.POST.get('action')
		if target_profile_id and action == 'unsubscribe':
			target_profile = Profile.objects.get(id=target_profile_id)
			subscription = Subscription.objects.filter(
				subscriber=user_profile.subscriber, publisher=target_profile.publisher
			).first()
			if subscription:
				subscription.delete()
			return redirect('Subscriptions:profile')
	return render(request=request, template_name="profile.html", context=context)

@login_required
def notify(request):
	subscribers = Subscription.objects.filter(publisher=request.user.profile.publisher)
	context = {
		'subscribers': [sub.subscriber.profile.user.username for sub in subscribers],
	}

	if request.method == 'POST':
		content = request.POST.get('content')

		if content:
			for sub in subscribers:
				Notification.objects.create(
					content=content,
					publisher=request.user.profile.publisher,
					receiver=sub.subscriber.profile.subscriber,
				)
			return redirect('Subscriptions:notify')

	return render(request, 'notify.html', context)

@login_required
def notification(request):
	notifications = Notification.objects.filter(receiver=request.user.profile.subscriber, is_read=False).order_by('-timestamp')
	context = {'notifications': notifications}
	return render(request, 'notification.html', context=context)