from django.urls import include, path
from .views import startup, volunteer, org

urlpatterns = [
	path('', startup.home, name = 'home'),
	path('signup/', startup.signup, name='signup'),
	path('volunteer/', include(([
			path('signup/', volunteer.VolunteerSignUpView.as_view(), name = 'signup'),
			path('events/', volunteer.EventListView.as_view(), name = 'events'),
			path('events/search/', volunteer.filter_view, name = 'eventsearch'),
			path('events/<int:pk>', volunteer.EventDetailView.as_view(), name = 'detail_event'),
			path('events/register/<int:pk>', volunteer.RegistrationCreateView.as_view(), name = 'register'),
			path('events/deregister/<int:pk>', volunteer.delete_registration, name = 'deregister'),
		], 'volunteer_system'), namespace = 'volunteers')),

	path('org/', include(([
			path('signup/', org.OrgSignUpView.as_view(), name = 'signup'),
			path('events/', org.EventListView.as_view(), name = 'events'),
			path('events/create/', org.EventCreateView.as_view(), name = 'create_event'),
			path('events/<int:pk>', org.EventDetailView.as_view(), name='detail_event'),
			path('events/delete/<int:pk>', org.EventDeleteView.as_view(), name = 'delete_event'),
			path('events/update/<int:pk>', org.EventUpdateView.as_view(), name = 'update_event'),
		], 'volunteer_system'), namespace = 'orgs'))

]