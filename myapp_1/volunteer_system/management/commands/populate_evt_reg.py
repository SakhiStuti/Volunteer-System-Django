import datetime
import random
from django.core.management.base import BaseCommand
from volunteer_system.models import Cause, User, Volunteer, Organisation, Interest, Event, Registration


event_n = 2000


cause_qs = Cause.objects.all()
volunteer_qs = Volunteer.objects.all()
volunteer_id = list(Volunteer.objects.values_list('user_id', flat=True))
org_qs = Organisation.objects.all()
cause_n = len(cause_qs)
volunteer_n = len(volunteer_qs)
org_n = len(org_qs)

description = "Operational NGO's have to mobilize resources in the form\
 of financial donations, materials, and volunteer labor in order to sustain\
 their projects and programs.  This is a complex process, and these NGOs usually\
 possess a headquarters bureaucracy and field staff."

def get_random_cause():
    idx = random.randint(0, cause_n-1)
    return cause_qs[idx]

def get_random_org():
    idx = random.randint(0, org_n-1)
    return org_qs[idx]

def get_random_volunteers(reg_n):
    random_id = random.sample(volunteer_id, reg_n)
    return volunteer_qs.filter(user_id__in = random_id)

def generate_date():
    year = random.randint(2010, 2030)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return datetime.date(year, month, day)

class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        city_state = '../dataset/city_state.csv' 
        event_title = '../dataset/event_title.csv'


        #Populating Events (Event, Register)
        with open(city_state) as file:
            event_city_state = file.read().splitlines()
        with open(event_title) as file:
            event_title = file.read().splitlines()

        for i in range(event_n):

            org = get_random_org()
            title = random.choice(event_title).capitalize()
            cause = get_random_cause()
            [city, state] = random.choice(event_city_state).split(',')
            num_req = random.randint(5, 20)
            date = generate_date()

            event = Event.objects.create(org = org,
                                         title = title,
                                         description = description,
                                         cause = cause,
                                         city = city,
                                         state = state,
                                         num_req = num_req,
                                         date = date)

            #Populate Register Table
            if i%100 == 0:
                reg_n = num_req
            else:
                reg_n = random.randint(0, num_req-1)

            volunteer_list = get_random_volunteers(reg_n)
            for j in range(reg_n):
                register = Registration.objects.create(volunteer = volunteer_list[j],
                                                       event = event)

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))