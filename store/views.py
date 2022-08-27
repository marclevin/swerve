from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from .forms import newCustomer
from .models import Customer
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages


# Create your views here.


def index(request):
    context = {}
    return render(request, 'pages/index.html')


def store(request):
    return render(request, 'pages/store.html')


def logout_request(request):
    logout(request)
    messages.info(request, 'Logged out successfully!')
    return redirect('index')


def register_request(request):
    if request.method == 'POST':
        form = newCustomer(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            customer = Customer.objects.create(
                user=request.user,
                email=form.cleaned_data['email'],
                address=form.cleaned_data['address']
            )
            messages.success(request, 'Account created successfully')
            return redirect('index')
        messages.error(request, 'Error creating account')
    form = newCustomer()
    return render(request, 'pages/register.html', {'register_form': form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f'You are now logged in as {user.get_username()}.')
                return redirect('index')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    form = AuthenticationForm()
    return render(request=request, template_name="pages/login.html", context={"login_form": form})
