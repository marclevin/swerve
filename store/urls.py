from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
                  path('', views.index, name='index'),
                  path('store/', views.store, name='store'),
                  path('register/', views.register_request, name='register'),
                  path('login/', views.login_request, name='login'),
                  path('logout/', views.logout_request, name='logout'),
                  path('store/<str:category>/', views.product_by_category, name='product_by_category'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
