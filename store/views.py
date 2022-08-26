from django.shortcuts import render, redirect
from .forms import newCustomer
from django.contrib.auth import login
from django.contrib import messages
# Create your views here.

def index(request):
    context = {}
    return render(request, 'pages/index.html')


def store(request):
    return render(request, 'pages/store.html')


def register_request(request):
    if (request.method == 'POST'):
        form = newCustomer(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully')
            return redirect('index')
        messages.error(request, 'Error creating account')
    form = newCustomer()
    return render(request, 'pages/register.html', {'register_form': form})
