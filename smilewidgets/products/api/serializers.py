from rest_framework import serializers
from products.models import  Product, GiftCard, ProductPrice


class QuerySerializer(serializers.Serializer):
    date = serializers.DateField()
    productCode = serializers.CharField(max_length=10)
    giftCardCode = serializers.CharField(max_length=30, required=False, allow_blank=True)

    class Meta:
        fields = (
            'date',
            'product_code',
            'gift_card_code',
        )