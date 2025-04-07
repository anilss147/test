from django.urls import path
from . import views

app_name = 'wishlist'

urlpatterns = [
    path('', views.wishlist_view, name='view'),
    path('add/<uuid:product_id>/', views.add_to_wishlist, name='add'),
    path('remove/<uuid:product_id>/', views.remove_from_wishlist, name='remove'),
    path('clear/', views.clear_wishlist, name='clear'),
]
