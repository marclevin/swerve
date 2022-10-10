from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from .forms import newCustomer, VehicleCalculatorForm, EditProfileForm
from .models import *
from .calculator import calculate
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.db.models import Sum, Count
from slick_reporting.views import SlickReportView
from slick_reporting.fields import SlickReportField


# Create your views here.


def index(request):
    # Picking a random item to be featured, for now it will be ID 1 of product
    featured_product = Product.objects.get(id=1)
    # Pick 6 products to be displayed on the home page at random
    products = Product.objects.all().order_by("?")[:6]
    context = {"featured_product": featured_product, "products": products}
    return render(request, "pages/index.html", context)


def store(request):
    # Retrieve all categories from database
    categories = Category.objects.all()
    context = {"categories": categories}
    return render(request, "pages/store.html", context)


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("index")


def register_request(request):
    isValid = True
    error_out = ""
    if request.method == "POST":
        form = newCustomer(request.POST)
        if form.is_valid():
            isValid = True
            user = form.save()
            login(request, user)
            customer = Customer.objects.create(
                user=request.user,
                email=form.cleaned_data["email"],
                address=form.cleaned_data["address"],
            )
            messages.success(request, "Account created successfully")
            return redirect("index")
        else:
            isValid = False
            error_out = form.errors
    form = newCustomer()
    return render(
        request,
        "pages/register.html",
        {"register_form": form, "valid": isValid, "error": error_out},
    )


def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=request.user)
        print(request.POST)
        if form.is_valid:
            form.save()
            messages.success(request, f"success: you have edited your profile")
            return redirect("index")
        else:
            form = EditProfileForm(instance=request.user)
            context = {
                "form": form,
            }
    form = EditProfileForm(instance=request.user)

    return render(request, "pages/edit_profile.html", {"edit_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(
                    request, f"You are now logged in as {user.get_username()}."
                )
                return redirect("index")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    form.fields["username"].widget.attrs["class"] = "form-control"
    form.fields["username"].widget.attrs["placeholder"] = "username"
    form.fields["password"].widget.attrs["class"] = "form-control"
    form.fields["password"].widget.attrs["placeholder"] = "password"
    return render(
        request=request, template_name="pages/login.html", context={"login_form": form}
    )


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    customer, created = Customer.objects.get_or_create(user=request.user)
    cart, created = Cart.objects.get_or_create(customer=customer, active=True)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.quantity += 1
    cart_item.save()
    cart.total_price += product.price
    cart.save()
    print(cart.total_price)
    messages.success(request, f"Successfully added {product.name} to your cart")
    return redirect(request.META["HTTP_REFERER"])


def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart = Cart.objects.get(customer__user=request.user, active=True)
    cart_item = CartItem.objects.get(cart=cart, product=product)
    cart_item.quantity -= 1
    cart.total_price -= product.price
    cart.save()
    messages.success(request, f"Successfully removed one {product.name} from your cart")
    if cart_item.quantity == 0:
        cart_item.delete()
    else:
        cart_item.save()

    cart_not_empty = delete_cart_if_empty(request)
    if cart_not_empty:
        return redirect(request.META["HTTP_REFERER"])
    else:
        return redirect(request.META["HTTP_REFERER"])


def delete_cart_if_empty(request):
    cart = Cart.objects.get(customer__user=request.user, active=True)
    any_cart_items = CartItem.objects.filter(cart=cart)
    if any_cart_items.exists():
        return True
    else:
        cart.delete()


def get_cart(request):
    if not request.user.is_authenticated:
        messages.info(request, "You must be logged in to view your cart")
        return redirect("/login")

    try:
        cart = Cart.objects.get(customer__user=request.user, active=True)
        cart_items = CartItem.objects.filter(cart=cart).select_related("product")
        context = {"cart_items": cart_items, "cart": cart}
    except Cart.DoesNotExist:
        context = {"cart_items": CartItem.objects.none()}

    return render(request, "pages/cart.html", context)


def create_order(request):
    try:
        customer, created = Customer.objects.get_or_create(user=request.user)
        cart = Cart.objects.get(customer__user=request.user, active=True)
        cart_items = CartItem.objects.filter(cart=cart).select_related("product")
        order_number = str(f"OR{cart.customer.pk}:{cart.pk}")
        cart.order_number = order_number
        cart.active = False
        cart.save()
        address = "you need to add an address to your profile"
        if customer.address != None:
            address = customer.address
        order = Order.objects.create(
            customer=customer,
            total_price=cart.total_price,
            order_number=order_number,
            destination=address,
        )
        # order.save()
        context = {"order": order, "cart_items": cart_items, "cart": cart}
    except Cart.DoesNotExist:
        context = {
            "order": Order.objects.none(),
            "cart_items": CartItem.objects.none(),
            "cart": Cart.objects.none(),
        }

    return render(request, "pages/order.html", context)


def get_orders(request):
    if not request.user.is_authenticated:
        messages.info(request, "You must be logged in to view orders")
        return redirect("/login")
    context = {}
    try:

        customer, created = Customer.objects.get_or_create(user=request.user)
        orders = Order.objects.filter(customer=customer)
        context = {"orders": orders}
    except Order.DoesNotExist:
        context = {"order": Order.objects.none()}

    return render(request, "pages/orders.html", context)


def get_receipt(request, order_id):
    order = Order.objects.get(pk=order_id)
    cart = Cart.objects.get(order_number=order.order_number, active=False)
    cart_items = CartItem.objects.filter(cart=cart)
    context = {"order": order, "cart_items": cart_items, "cart": cart}

    return render(request, "pages/receipt.html", context)


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
    context = {"products": products, "category": category_selected}
    return render(request, "pages/product_page.html", context)


def product_filter_search(request, category, filter_products):
    category_selected = Category.objects.get(name=category)
    # context = {'products': products, 'category': category_selected}
    # return render(request, 'pages/product_page.html', context)
    if filter_products == "cheapest":
        print("filtering by cheapest")
        products = Product.objects.filter(category=category_selected).order_by("price")
        print(products)
        context = {"products": products, "category": category_selected}
        return render(request, "pages/product_page.html", context)
    if filter_products == "expensive":
        print("filtering by expensive")
        products = Product.objects.filter(category=category_selected).order_by("-price")
        context = {"products": products, "category": category_selected}
        return render(request, "pages/product_page.html", context)
    if filter_products == "discount":
        print("filtering by discount")
        products = Product.objects.filter(
            category=category_selected, discount_price__gt=0
        )
        context = {"products": products, "category": category_selected}
        return render(request, "pages/product_page.html", context)
    if filter_products == "fastest":
        print("filtering by fastest")
        products = Product.objects.filter(category=category_selected).order_by(
            "-max_speed"
        )
        context = {"products": products, "category": category_selected}
        return render(request, "pages/product_page.html", context)
    if filter_products == "slowest":
        print("filtering by slowest")
        products = Product.objects.filter(category=category_selected).order_by(
            "max_speed"
        )
        context = {"products": products, "category": category_selected}
        return render(request, "pages/product_page.html", context)


def calculator(request):
    curtain_check = True
    product_suggested = ""
    if request.method == "POST":
        form = VehicleCalculatorForm(request.POST)
        if form.is_valid():
            curtain_check = False
            product_suggested = calculate(form.cleaned_data)

    else:
        curtain_check = True

    form = VehicleCalculatorForm()
    context = {
        "calculator_form": form,
        "curtain_check": curtain_check,
        "product_suggested": product_suggested,
    }
    return render(request, "pages/calculator.html", context=context)


class TotalOrders(SlickReportView):
    report_description = "Some description"
    report_model = Order
    date_field = "date"
    columns = [
        SlickReportField.create(Sum, "total_price", "Stonks"),
    ]
    chart_settings = [
        {
            "type": "column",
            "data_source": ["Stonks"],
            "plot_total": True,
        },
    ]
