from django import forms
from django.contrib.auth.models import User
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import StrictButton
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from crispy_forms.layout import Field, Layout


class newCustomer(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Email"}
        ),
        label="Email",
    )
    address = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Address"}
        ),
        label="Address",
    )
    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        ),
        label="Password",
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirm Password"}
        ),
        label="Confirm Password",
    )

    class Meta:
        model = User
        fields = ["username", "address", "email", "password1", "password2"]
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Username"}
            ),
            "address": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Address"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Email"}
            ),
            "password1": forms.PasswordInput(
                attrs={"class": "form-control", "placeholder": "Password"}
            ),
            "password2": forms.PasswordInput(
                attrs={"class": "form-control", "placeholder": "Password Again"}
            ),
        }

    def save(self, commit=True):
        user = super(newCustomer, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class EditProfileForm(forms.ModelForm):
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    email = forms.EmailField(
        required=True, widget=forms.TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        username = forms.CharField(
            max_length=100,
            required=True,
            widget=forms.TextInput(
                attrs={"class": "form-control", "placeholder": "username"}
            ),
        )
        email = forms.EmailField(
            required=True,
            widget=forms.TextInput(
                attrs={"class": "form-control", "placeholder": "email"}
            ),

        )


        model = User
        fields = ["username", "email", "password"]

        widgets = {
            "username": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Username"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Email"}
            ),
            "password": forms.PasswordInput(
                attrs={"class": "form-control", "placeholder": "Password"}
            ),
        }


class EditCustomerAddress(forms.ModelForm):
    class Meta:
        address = forms.CharField(
            max_length=100,
            required=True,
            widget=forms.TextInput(attrs={"class": "form-control"}),
        )
        model = Customer
        fields = ["address"]

        widgets = {
            "address": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Address"}
            ),
        }


vehicle_frequency_choices = (
    ("Once a week", "Once a week"),
    ("Once a month", "Once a month"),
    ("Once a day", "Once a day"),
    ("More than once a day", "More than once a day"),
)


class VehicleCalculatorForm(forms.Form):
    vehicle_type = forms.ChoiceField(
        choices=Category.objects.all().values_list("id", "name"),
        label="Vehicle Type",
        widget=forms.Select(attrs={"class": "form-control float-left"}),
    )
    vehicle_drive_dist = forms.IntegerField(
        label="How many kilometers do you drive per day on average?",
        min_value=0,
        max_value=1000,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    vehicle_people_count = forms.IntegerField(
        label="How many people are typically in your vehicle?",
        min_value=0,
        max_value=10,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    vehicle_frequency = forms.ChoiceField(
        choices=vehicle_frequency_choices,
        label="How often do you drive your vehicle?",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    def __init__(self, *args, **kwargs):
        super(VehicleCalculatorForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "id-vehicleCalculatorForm"
        self.helper.form_method = "post"
        self.helper.add_input(
            StrictButton("Calculate", type="submit", css_class="form-control")
        )
