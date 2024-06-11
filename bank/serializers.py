from rest_framework import serializers

from .models import Customer, Account, Action, Transaction, Transfer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'fname', 'lname',
                  'city', 'house', 'image')
        read_only_fields = ('id',)

    def create(self, validated_data):
        validated_data['user_id'] = self.context['request'].user.id
        return super(CustomerSerializer, self).create(validated_data)


class AccountSerializer(serializers.ModelSerializer):
    actions = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Account
        fields = ('id', 'balance', 'actions')
        read_only_fields = ('id', 'balance', 'actions')


class ActionSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(ActionSerializer, self).__init__(*args, **kwargs)
        if 'request' in self.context:
            self.fields['account'].queryset = self.fields['account'].queryset.filter(user=self.context['view'].request.user)

    class Meta:
        model = Action
        fields = ('id', 'account', 'amount', 'date')
        read_only_fields = ('id', 'date')

    def create(self, validated_data):
        print(validated_data['amount'])
        if validated_data['account'].balance + validated_data['amount'] > 0:
            validated_data['account'].balance += validated_data['amount']
            validated_data['account'].save()
        else:
            raise serializers.ValidationError(
                ('Not enough money')
            )
        return super(ActionSerializer, self).create(validated_data)


class TransactionSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(TransactionSerializer, self).__init__(*args, **kwargs)
        if 'request' in self.context:
            self.fields['account'].queryset = self.fields['account'].queryset.filter(user=self.context['view'].request.user)

    class Meta:
        model = Transaction
        fields = ('id', 'account', 'date', 'merchant', 'amount')
        read_only_fields = ('id',)


class TransferSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(TransferSerializer, self).__init__(*args, **kwargs)
        if 'request' in self.context:
            self.fields['from_account'].queryset = self.fields['from_account'].queryset.filter(user=self.context['view'].request.user)

    to_account = serializers.CharField()

    def validate(self, data):
        try:
            data['to_account'] = Account.objects.get(pk=data['to_account'])
        except Exception as e:
            print(e)
            raise serializers.ValidationError("No such account from serializer")

        return data

    class Meta:
        model = Transfer
        fields = ('id', 'from_account', 'to_account', 'amount')
        read_only_fields = ('id', )
