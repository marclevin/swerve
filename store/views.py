from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from .forms import newCustomer, VehicleCalculatorForm
from .models import *
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages


# Create your views here.


def index(request):
    # Picking a random item to be featured, for now it will be ID 1 of product
    featured_product = Product.objects.get(id=1)
    # Pick 6 products to be displayed on the home page at random
    products = Product.objects.all().order_by('?')[:6]
    context = {'featured_product': featured_product, 'products': products}
    return render(request, 'pages/index.html', context)


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
    isValid = True
    error_out = ''
    if request.method == 'POST':
        form = newCustomer(request.POST)
        if form.is_valid():
            isValid = True
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
            isValid = False
            error_out = form.errors
    form = newCustomer()
    return render(request, 'pages/register.html', {'register_form': form, 'valid': isValid, 'error': error_out})


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



def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart, created = Cart.objects.get_or_create(customer=request.user)
    cart_item, created = CartItem.objects.get_or_create(customer=request.user, order=cart, product=product)
    cart_item.quantity += 1
    cart_item.save()
    messages.success(request, f"Successfully added {product.name} to your cart")
    return redirect("pages/index.html")



def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart = Cart.objects.get(customer=request.user)
    cart_item = CartItem.objects.get(Order=cart, product=product)
    cart_item.quantity -= 1
    messages.success(request, f"Successfully removed one {product.name} from your cart")
    if cart_item.quantity == 0:
        cart_item.delete()
    else:
        cart_item.save()

    cart_not_empty = delete_cart_if_empty(request)
    if cart_not_empty:
        return redirect("pages/index.html")
    else:
        return redirect("pages/index.html")


def delete_cart_if_empty(request):
    cart = Cart.objects.get(customer=request.user)
    any_cart_items = CartItem.objects.filter(cart=cart)
    if any_cart_items.exists():
        return True
    else:
        cart.delete()

def get_cart(request):
    if ( not request.user.is_authenticated):
        messages.info(request, 'You must be logged in to view your cart')
        return redirect('/login')
    context = {}
    try:
         cart = Cart.objects.get(customer__user=request.user)
         items_in_cart = CartItem.objects.filter(cart=cart)
         context = {'products': items_in_cart, 'empty': False}
    except Cart.DoesNotExist:
        context = {'products': None, 'empty': True}
        pass

    return render(request, 'pages/cart.html', context)


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
    curtain_check = True
    if request.method == "POST":
        form = VehicleCalculatorForm(request.POST)
        if form.is_valid():
            curtain_check = False
            vehicle_type = form.cleaned_data['vehicle_type']
    else:
        curtain_check = True

    form = VehicleCalculatorForm()
    context={"calculator_form": form, 'curtain_check': curtain_check}
    return render(request, 'pages/calculator.html', context=context)
