from django import forms
from django.contrib.auth.models import User
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import StrictButton
from django.contrib.auth.forms import UserCreationForm
from django_filters.fields import RangeField
from crispy_forms.layout import Field, Layout

class newCustomer(UserCreationForm):
    email = forms.EmailField(required=True)
    address = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ['username', 'address', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(newCustomer, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
