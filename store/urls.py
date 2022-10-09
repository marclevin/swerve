from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('store/', views.store, name='store'),
    path('register/', views.register_request, name='register'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('store/<str:category>/', views.product_by_category, name='product_by_category'),
    path('calculator/', views.calculator, name='calculator'),
    path('cart/', views.get_cart, name='cart'),
    # url for adding to cart button click on home page
    path('<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    # filter by
    path('store/<str:category>/<str:filter_products>', views.product_filter_search, name='filter_search'),
]