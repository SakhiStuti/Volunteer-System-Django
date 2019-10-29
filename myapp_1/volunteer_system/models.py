from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
import datetime

# Create your models here.

class User(AbstractUser):
	is_org = models.BooleanField(default = False)

	def __str__(self):
		return self.username


class Volunteer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, primary_key =True)
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)

    def __str__(self):
        return self.user.username


class Cause(models.Model):
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.category

class Interest(models.Model):
    
    class Meta:
        unique_together = (('user', 'cause'))
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cause = models.ForeignKey(Cause, on_delete= models.CASCADE)

    def __str__(self):
        return 'NOT YET DEFINED'

class Organisation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Event(models.Model):
    org = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=500)
    cause = models.ForeignKey(Cause, on_delete= models.CASCADE)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    num_req = models.IntegerField(validators=[MinValueValidator(1)])
    date = models.DateField()

    def __str__(self):
        return self.title

class Registration(models.Model):
    class Meta:
        unique_together = (('volunteer', 'event'))
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete= models.CASCADE)

    def __str__(self):
        return 'NOT YET DEFINED'
