from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register('customer', views.CustomerViewSet)
router.register('account', views.AccountViewSet)
router.register('action', views.ActionViewSet)
router.register('transaction', views.TransactionViewSet)
router.register('transfer', views.TransferViewSet)

urlpatterns = [
    # path('customer-list/', views.CustomerList.as_view(), name='customer-list'),
    # path('customer-detail/<int:pk>/', views.CustomerDetail.as_view(), name='customer-detail')

    path('', include(router.urls))
]
