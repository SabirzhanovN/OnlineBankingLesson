from rest_framework import serializers

from bank.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'fname', 'lname',
                  'city', 'house', 'image')
        read_only_fields = ('id',)

    def create(self, validated_data):
        validated_data['user_id'] = self.context['request'].user.id
        return super(CustomerSerializer, self).create(validated_data)



