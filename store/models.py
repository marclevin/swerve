import datetime

from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=100, blank=True)
    address = models.CharField(max_length=200, blank=True)
    contact = models.CharField(max_length=24, blank=True)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=350, blank=True)
    image = models.ImageField(upload_to='category_images/', default='afk.jpg')

    @staticmethod
    def get_categories():
        return Category.objects.all()

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()
    discount_price = models.FloatField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.CharField(max_length=100, default="")
    colour = models.CharField(max_length=100, default="")
    weight = models.FloatField(default=0)
    stock = models.IntegerField()
    image = models.ImageField(upload_to='product_images/', default='afk.jpg')

    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in=ids)

    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_all_products_by_category(category_id):
        if category_id:
            return Product.objects.filter(category=category_id)
        else:
            return Product.get_all_products()

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)
    total_price = models.FloatField(default=0)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.FloatField(default=0)

    def __str__(self):
        return f'{self.quantity} of {self.product.name}'

    def get_total_price(self):
        return self.quantity * self.price


class Invoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    destination = models.CharField(max_length=50, default='', blank=True)
    price = models.IntegerField(default=0)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def saveInvoice(self):
        self.save()

    @staticmethod
    def get_invoice_by_customer(customer_id):
        return Invoice.objects.filter(customer=customer_id).order_by('-date')
