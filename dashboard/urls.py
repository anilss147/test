from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='index'),
    path('products/', views.dashboard_products, name='products'),
    path('orders/', views.dashboard_orders, name='orders'),
    path('customers/', views.dashboard_customers, name='customers'),
    path('analytics/', views.dashboard_analytics, name='analytics'),
]
