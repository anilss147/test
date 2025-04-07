from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='list'),
    path('search/', views.search_products, name='search'),
    path('category/<str:gender_or_category>/', views.category_list, name='category_list'),
    path('<uuid:product_id>/', views.product_detail, name='detail'),
]
