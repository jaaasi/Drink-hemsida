from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm



# model for registration
# Username and password fields are created with the existing django form UserCreationForm
class MyRegistrationForm(UserCreationForm):
    email = forms.EmailField(required = True)
    first_name = forms.CharField(required = True)
    last_name = forms.CharField(required = True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(MyRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.is_active = False

        if commit:
            user.save()
        return user


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length=40)
    is_developer = models.NullBooleanField(default=False)


class Drink(models.Model):
    namn = models.CharField(max_length=255)
    bildurl = models.URLField(unique=False)
    hv = models.DecimalField(default=0, decimal_places=1, max_digits=3)
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    type = models.CharField(max_length=20)
    instructions = models.CharField(max_length=255)
    ingredient1 = models.CharField(max_length=255)
    ingredient2 = models.CharField(max_length=255)
    ingredient3 = models.CharField(max_length=255)
    ingredient4 = models.CharField(max_length=255)
    ingredient5 = models.CharField(max_length=255)
    ingredient6 = models.CharField(max_length=255)
    ingredient7 = models.CharField(max_length=255)
    ingredient8 = models.CharField(max_length=255)


class Event(models.Model):
    title = models.CharField(max_length=255)
    longText = models.CharField(max_length=255)
    shortText = models.CharField(max_length=255)
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    imgUrl = models.URLField(unique=False)
