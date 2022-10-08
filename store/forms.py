from django import forms
from django.contrib.auth.models import User
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import StrictButton
from django.contrib.auth.forms import UserCreationForm
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

class VehicleCalculatorForm(forms.Form):
    vehicle_type = forms.ChoiceField(choices=Category.objects.all().values_list('id', 'name'), label='Vehicle Type')
    vehicle_weight = forms.IntegerField()
    vehicle_length = forms.IntegerField()
    vehicle_width = forms.IntegerField()
    vehicle_height = forms.IntegerField()
    vehicle_distance = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super(VehicleCalculatorForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'calculate'
        self.helper.add_input(StrictButton('Calculate', type='submit', css_class='btn-primary'))
