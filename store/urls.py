from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("store/", views.store, name="store"),
    path("register/", views.register_request, name="register"),
    path("login/", views.login_request, name="login"),
    path("logout/", views.logout_request, name="logout"),
    path(
        "store/<str:category>/", views.product_by_category, name="product_by_category"
    ),
    path("calculator/", views.calculator, name="calculator"),
    path("cart/", views.get_cart, name="cart"),
    # url for adding to cart button click on home page
    path("<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    # url to delete a cart item
    path("cart/<int:product_id>", views.remove_from_cart, name="remove_from_cart"),
    # filter by
    path(
        "store/<str:category>/<str:filter_products>",
        views.product_filter_search,
        name="filter_search",
    ),
    # url to create order
    path("order/", views.create_order, name="create_order"),
    path("single/<int:product_id>", views.single_product, name="single_product"),
    # path to see all previous orders
    path("orders/", views.get_orders, name="get_orders"),
    # path to get specific receipt
    path("receipt/<int:order_id>/", views.get_receipt, name="get_receipt"),
    # path to try edit profile
    path("edit_profile/", views.edit_profile, name="edit_profile"),
    path("about_unchained/", views.about_unchained, name="about_unchained"),
]
