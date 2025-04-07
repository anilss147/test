from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.checkout_view, name='checkout'),
    path('success/<uuid:order_id>/', views.order_success_view, name='success'),
    path('history/', views.order_history_view, name='history'),
    path('detail/<uuid:order_id>/', views.order_detail_view, name='detail'),
]
