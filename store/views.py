from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from .forms import newCustomer
from .models import *
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages


# Create your views here.


def index(request):
    context = {}
    return render(request, 'pages/index.html')


def store(request):
    # Retrieve all categories from database
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'pages/store.html', context)


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
        else:
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


def contact(request):
    if request.method == "POST":
        message_name = request.POST["message-name"]
        message_email = request.POST["message-email"]
        message_phone = request.POST["message-phone"]
        message = request.POST["message"]
        # send email
        send_mail(
            subject="Website Contact Form",
            message='From:' + message_name + ': ' + message + '// Phone Number: ' + message_phone,
            from_email=message_email,
            recipient_list=["@gmail.com"],
        )
    return render(request, "pages/index.html")


def product_by_category(request, category):
    products = Product.objects.filter(category=category)
    context = {'products': products, 'category': category}
    return render(request, 'pages/store.html', context)