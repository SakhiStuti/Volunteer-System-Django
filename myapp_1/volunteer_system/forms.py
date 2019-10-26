from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from .widgets import BootstrapDateTimePickerInput

from volunteer_system.models import User, Volunteer, Cause, Interest, Organisation, Event


class OrgSignupForm(UserCreationForm):
    name = forms.CharField(label = 'Name of Organisation')
    causes = forms.ModelMultipleChoiceField(
        queryset=Cause.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save()
        user.is_org = True
        user.save()
        name = self.cleaned_data.get('name')
        causes = self.cleaned_data.get('causes')
        organisation = Organisation.objects.create(user=user, name = name)
        for cause in causes:
            interest = Interest.objects.create(user=user, cause=cause)
        return user

class VolunteerSignupForm(UserCreationForm):
    last_name = forms.CharField(label = 'Last Name')
    first_name = forms.CharField(label = 'First Name')
    causes = forms.ModelMultipleChoiceField(
        queryset=Cause.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save()
 		#user.is_org is False by default. 
        user.save()
        last_name = self.cleaned_data.get('last_name')
        first_name = self.cleaned_data.get('first_name')
        causes = self.cleaned_data.get('causes')
        volunteer = Volunteer.objects.create(user=user, last_name = last_name, first_name = first_name)
        for cause in causes:
        	interest = Interest.objects.create(user=user, cause=cause)
        return user


class EventCreationForm(ModelForm):

    description = forms.CharField(widget=forms.Textarea)
    date = forms.DateField(
    widget=forms.TextInput(     
        attrs={'type': 'date'} 
    )
)  

    def __init__(self, *args, **kwargs):
        super(EventCreationForm, self).__init__(*args, **kwargs)
        num_req_field = self.fields['num_req']
        num_req_field.validators.append(MinValueValidator(1))

    class Meta(UserCreationForm.Meta):
        model = Event
        fields = ['title', 'description', 'cause', 'city', 'state', 'num_req', 'date']


