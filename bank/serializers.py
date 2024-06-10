from rest_framework import serializers

from .models import Customer, Account, Action


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


