from rest_framework import serializers
from PurchasesData.models import Purchase


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = '__all__'
        read_only_fields = ('id',)
        extra_kwargs = {
            'user': {'required': True},
            'store': {'required': True},
            'date': {'required': True},
            'time': {'required': True},
            'total_price': {'required': True},
            'discount': {'required': True},
            'total_payed': {'required': True},
        }
