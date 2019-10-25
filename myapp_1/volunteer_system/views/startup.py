from django.shortcuts import render, redirect
from django.views.generic import TemplateView


def signup(request):
	return render(request, 'volunteer_system/signup.html')

def home(request):
	if request.user.is_authenticated:
		if request.user.is_org:
			return redirect('orgs:events')
		else:
			return redirect('volunteers:eventsearch')
	return render(request, 'volunteer_system/home.html')





