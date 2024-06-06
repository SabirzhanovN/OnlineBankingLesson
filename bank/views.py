from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework import mixins

from .models import Customer, Account
from .serializers import CustomerSerializer, AccountSerializer


class CustomerList(generics.ListCreateAPIView):
    """
    Get a list, put and patch methods are not allowed.
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, )

    def get_queryset(self):
        """
        Return object for current authenticated user only
        """
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CustomerDetail(generics.RetrieveUpdateAPIView):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        Return object for current authenticated user only
        """
        return self.queryset.filter(user=self.request.user)


class CustomerViewSet(viewsets.ModelViewSet):
    """
    Example of viewset. PUT, PATCH, DELETE, POST available only via pk.
    """
    serializer_class = CustomerSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Customer.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """
        Return object for current authenticated user only
        """
        return self.queryset.filter(user=self.request.user)


class AccountViewSet(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin):
    """
    Viewset for list and create account.
    """
    serializer_class = AccountSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Account.objects.all()

    def perform_create(self, serializer):
        """
        Create a new account. POST method with empty body
        """
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """
        Return object for current authenticated user only
        """
        return self.queryset.filter(user=self.request.user)