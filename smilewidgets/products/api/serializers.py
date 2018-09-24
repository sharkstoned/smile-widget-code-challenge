from rest_framework import serializers
from products.models import Product, GiftCard


class QuerySerializer(serializers.Serializer):
    date = serializers.DateField()
    product_code = serializers.CharField(max_length=10)
    gift_card_code = serializers.CharField(max_length=30, required=False, allow_blank=True)

    def validate(self, params):
        if params['gift_card_code']:
            try:
                GiftCard.objects.get(code=params['gift_card_code'])
            except GiftCard.DoesNotExist:
                raise serializers.ValidationError('Incorrect gift card code')

        return params

    def validate_product_code(self, data):
        try:
            Product.objects.get(code=data)
        except Product.DoesNotExist:
            raise serializers.ValidationError('Incorrect product code')

        return data
