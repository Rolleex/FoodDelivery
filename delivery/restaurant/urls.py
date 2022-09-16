from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('order-info/<int:pk>', OrderDetails.as_view(), name='order-details'),
]
