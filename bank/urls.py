from django.urls import path

from . import views

urlpatterns = [
    path('customer-list/', views.CustomerList.as_view(), name='customer-list')
]
