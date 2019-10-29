import datetime
import random
from django.core.management.base import BaseCommand
from volunteer_system.models import Cause, User, Volunteer, Organisation, Interest, Event, Registration


volunteer_n = 500
org_n = 500

causes = [
'Poverty',
'Social Injustice',
'Environment',
'Human Rights',
'Elderly people',
'Women Empowerment',
'Wildlife Conservation',
'Animal Rights',
'Sanitation and Hygiene',
'Humanitarian Relief',
'Health and Nutrition',
'Literacy and Education',
'Refugee Crisis',
'Disease Control',
'Natural Disaster'
]

class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        volunteer_names = '../dataset/first_names.csv.txt' 
        org_names = '../dataset/ngo_names.csv'
        #Populate Causes Table
        for cause in causes:
            created_obj = Cause.objects.create(category=cause)

        #Populating Volunteers (Volunteers, User, Interest)
        with open(volunteer_names) as file:
            content = file.read().splitlines()
        for i in range(volunteer_n):
            username = 'v_{}'.format(str(i))
            password = '123'
            user = User.objects.create_user(username= username, 
                                            password = password, 
                                            is_org = False)

            last_name = random.choice(content)
            first_name = random.choice(content)
            volunteer = Volunteer.objects.create(last_name = last_name,
                                                 first_name = first_name,
                                                 user = user)

            interest_n = random.randint(1, len(causes))
            for cause in random.sample(causes, interest_n):
                cause_obj = Cause.objects.get(category = cause)
                interest = Interest.objects.create(user = user,
                                                   cause = cause_obj)
            if i%50 == 0:
                print(i ,' volunteer records done!')

        #Populating Orgs (Organisation, User, Interest)
        with open(org_names) as file:
            content = file.read().splitlines()
        for i in range(org_n):
            username = 'o_{}'.format(str(i))
            password = '123'
            user = User.objects.create_user(username= username, 
                                            password = password, 
                                            is_org = True)

            name = random.choice(content)
            org = Organisation.objects.create(name = name,
                                              user = user)

            interest_n = random.randint(1, len(causes))
            for cause in random.sample(causes, interest_n):
                cause_obj = Cause.objects.get(category = cause)
                interest = Interest.objects.create(user = user,
                                                   cause = cause_obj)
            if i%50 == 0:
                print(i ,' org records done!')

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))