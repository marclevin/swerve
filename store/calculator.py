from unicodedata import category
from .models import Product


def calculate(dictionary):
    context = {}
    # Take in the vehicle form dictionary and return an product from products
    vehicle_type = dictionary["vehicle_type"]
    vehicle_drive_dist = dictionary["vehicle_drive_dist"]
    vehicle_people_count = dictionary["vehicle_people_count"]
    vehicle_frequency = dictionary["vehicle_frequency"]
    # Now we have all the data we need to calculate the best product
    # We need to get the product with the highest max_range that is less than vehicle_drive_dist
    products = Product.objects.filter(category=vehicle_type)
    # use max_range
    # GTE = greater than or equal to
    products = products.filter(max_range__gte=vehicle_drive_dist)
    # Use the frequency to determine if they need a fast charger
    # If they drive more than once a day, they need a fast charger
    if vehicle_frequency == "More than once a day":
        products = products.filter(charge_time__lte=3)
    if vehicle_frequency == "Once a day":
        products = products.filter(charge_time__lte=5)
    if vehicle_frequency == "Once a week":
        products = products.filter(charge_time__lte=10)
    if vehicle_frequency == "Once a month":
        products = products.filter(charge_time__lte=20)
    # Randomize the final selection
    # Use the number of people to determine if we should suggest a different product (maybe todo)
    return products.order_by("?").first()
