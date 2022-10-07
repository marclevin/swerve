from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
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


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart, created = Cart.objects.get_or_create(customer=request.user)
    cart_item, created = CartItem.objects.get_or_create(customer=request.user, order=cart, product=product)
    cart_item.quantity += 1
    cart_item.save()
    messages.success(request, f"Successfully added {product.name} to your cart")
    return redirect("pages/index.html")


@login_required
def remove_from_cart(request, product_id, cart_id):
    product = get_object_or_404(Product, pk=product_id)
    cart = get_object_or_404(Cart, pk=cart_id)
    cart_item = CartItem.objects.get(Order=cart, product=product)
    cart_item.quantity -= 1
    cart_item.save()
    messages.success(request, f"Successfully removed one {product.name} from your cart")


def contact(request):
    if request.method == "POST":
        message_name = request.POST["message-name"]
        message_email = request.POST["message-email"]
        message_phone = request.POST["message-phone"]
        message = request.POST["message"]
        # send email
        send_mail(
            subject="Website Contact Form",
            message=f"From: {message_name}   {message} Phone Number: {message_phone}",
            from_email=message_email,
            recipient_list=["@gmail.com"],
        )
    return render(request, "pages/index.html")


def product_by_category(request, category):
    category_selected = Category.objects.get(name=category)
    products = Product.objects.filter(category=category_selected)
    context = {'products': products, 'category': category_selected}
    return render(request, 'pages/product_page.html', context)


def calculator(request):
    return render(request, 'pages/calculator.html')

 
