from django import forms
from django.contrib.auth.models import User
from .models import Customer
from django.contrib.auth.forms import UserCreationForm


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
