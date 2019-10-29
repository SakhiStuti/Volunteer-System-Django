from django.core.management.base import BaseCommand
from volunteer_system.models import Cause, User, Volunteer, Organisation, Interest, Event, Registration

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
    	print('Interest ', print(Interest.objects.all().count()))
    	print('Register ', print(Registration.objects.all().count()))