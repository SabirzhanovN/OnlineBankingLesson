from rest_framework import serializers

from .models import Customer, Account


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

