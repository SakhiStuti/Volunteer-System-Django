from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView, DeleteView
from django.contrib.auth import login
from django.http import HttpResponseRedirect

from datetime import date
from django.db.models import F
from django.db.models import Count
from django.urls import reverse, reverse_lazy

from ..forms import VolunteerSignupForm
from ..models import User, Event, Registration, Volunteer, Cause

def filter_view(request):
	qs = filter(request)
	context = {
		#'queryset': qs,
		'causes': Cause.objects.all(),
		'status': ['Requires Volunteers', 'Registration Full'],
		'city': Event.objects.values_list('city', flat=True).distinct(),
		'states': Event.objects.values_list('state', flat=True).distinct(),
		'events': qs
	}
	return render(request, 'volunteer_system/volunteer/filter_view.html', context)

def is_valid_queryparam(param):
    return param != '' and param is not None

def filter(request):
    qs = Event.objects.all()

    title_contains_query = request.GET.get('title_contains')
    org_exact_query = request.GET.get('org_exact')
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')
    city = request.GET.get('city')
    state = request.GET.get('state')
    cause = request.GET.get('cause')
    status = request.GET.get('status')
    my_registration = request.GET.get('my_registration')


    if is_valid_queryparam(title_contains_query):
        qs = qs.filter(title__icontains=title_contains_query)

    if is_valid_queryparam(org_exact_query):
      	qs = qs.filter(org__name=org_exact_query)

    if is_valid_queryparam(date_min):
        qs = qs.filter(date__gte=date_min)

    if is_valid_queryparam(date_max):
        qs = qs.filter(date__lt=date_max)

    if is_valid_queryparam(city) and city != 'Choose...':
        qs = qs.filter(city=city)

    if is_valid_queryparam(state) and state != 'Choose...':
        qs = qs.filter(state=state)

    if is_valid_queryparam(cause) and cause != 'Choose...':
        qs = qs.filter(cause__category=cause)

    if status == 'on':
    	qs = qs
        #qs = qs.annotate(rem= F('num_req') - Count(Registration.objects.filter(event='id')))
        #qs = qs.filter(rem__gt=0)

    if my_registration == 'on':
    	volunteer = Volunteer.objects.get(user = request.user)
    	my_events = Registration.objects.filter(volunteer = volunteer).values_list('event', flat=True)
    	qs = qs.filter(id__in=my_events)

    return qs

class EventListView(ListView):
	model = Event
	ordering = ('title')
	template_name = 'volunteer_system/volunteer/events.html'
	context_object_name = 'events'

	def get_queryset(self):
		queryset = Event.objects.all()
		return queryset

class EventDetailView(DetailView):
	model = Event
	template_name = 'volunteer_system/volunteer/detail_events.html'
	def get_context_data(self, **kwargs):
	    event = self.object
	    volunteer = Volunteer.objects.get(user = self.request.user)
	    context = super().get_context_data(**kwargs)
	    context['num_registered'] = Registration.objects.filter(event=event).count()
	    context['people_req'] = event.num_req > context['num_registered']
	    context['future_date'] = event.date >= date.today()
	    context['not_registered'] = Registration.objects.filter(event = event, volunteer = volunteer).count() == 0
	    return context

class VolunteerSignUpView(CreateView):
    model = User
    form_class = VolunteerSignupForm
    template_name = 'volunteer_system/signup_form.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('volunteers:events')

    def get_context_data(self, **kwargs):
	    context = super().get_context_data(**kwargs)
	    context['is_org'] = False
	    return context

class RegistrationCreateView(CreateView):
	model = Registration
	fields = []
	template_name = 'volunteer_system/volunteer/register_events.html'

	def form_valid(self, form):
		registration = form.save(commit=False)
		registration.volunteer = Volunteer.objects.get(user = self.request.user)
		registration.event = Event.objects.get(pk = self.kwargs['pk'])
		registration.save()
		#messages.success(self.request, 'The quiz was created with success! Go ahead and add some questions now.')
		return redirect('volunteers:detail_event', pk = self.kwargs['pk'])

	def get_context_data(self, **kwargs):
	    context = super().get_context_data(**kwargs)
	    context['pk'] = self.kwargs['pk']
	    return context

def delete_registration(request, pk=None):
	volunteer = Volunteer.objects.get(user = request.user)
	event = Event.objects.get(pk = pk)
	registration = Registration.objects.get(volunteer = volunteer, event = event)
	context = {'pk':pk}
	if request.method == "POST":
		registration.delete()
		return redirect('volunteers:detail_event', pk = pk)
	
	return render(request,'volunteer_system/volunteer/deregister_events.html',context)
	
		
		
