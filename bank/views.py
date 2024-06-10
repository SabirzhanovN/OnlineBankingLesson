from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.response import Response

from .models import Customer, Account, Action
from .serializers import CustomerSerializer, AccountSerializer, ActionSerializer


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


class ActionViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin):
    serializer_class = ActionSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Action.objects.all()

    def get_queryset(self):
        """
        Return Action objects for current authenticated user only.
        """
        accounts = Account.objects.filter(user=self.request.user)

        return self.queryset.filter(account__in=accounts)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Checks if requested account belongs to user.
        try:
            account = Account.objects.filter(user=self.request.user).get(pk=self.request.data['account'])
        except Exception as e:
            print(e)

            content = {'Error': 'No such account!'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(account=account)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



