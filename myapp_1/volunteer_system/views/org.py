from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView, DeleteView
from django.contrib.auth import login
from django.urls import reverse, reverse_lazy

from ..forms import OrgSignupForm, EventCreationForm
from ..models import User, Event, Organisation, Registration


def delete(request):
	return render(request, 'volunteer_system/test.html')

class EventDeleteView(DeleteView):
    model = Event
    template_name = 'volunteer_system/org/delete_events_confirm.html'
    success_url = reverse_lazy('orgs:events')



class EventDetailView(DetailView):
	model = Event
	template_name = 'volunteer_system/org/detail_events.html'
	def get_context_data(self, **kwargs):
	    event = self.object
	    context = super().get_context_data(**kwargs)
	    context['num_registered'] = Registration.objects.filter(event=event).count()
	    return context

class EventListView(ListView):
	model = Event
	ordering = ('title')
	template_name = 'volunteer_system/org/events.html'
	context_object_name = 'events'

	def get_queryset(self):
		org = Organisation.objects.get(user=self.request.user)
		queryset = Event.objects.filter(org = org)
		return queryset

class EventCreateView(CreateView):
	model = Event
	form_class = EventCreationForm
	template_name = 'volunteer_system/org/create_events.html'

	def form_valid(self, form):
		event = form.save(commit=False)
		event.org = Organisation.objects.get(user = self.request.user)
		event.save()
		#messages.success(self.request, 'The quiz was created with success! Go ahead and add some questions now.')
		return redirect('orgs:events')


class OrgSignUpView(CreateView):
    model = User
    form_class = OrgSignupForm
    template_name = 'volunteer_system/signup_form.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('orgs:events')






