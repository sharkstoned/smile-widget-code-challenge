from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from django.http import JsonResponse

from products.models import Product, GiftCard
from .serializers import QuerySerializer


def calculate_discount(gift_card_code, date):
    discount = 0

    if gift_card_code:
        gift_card = GiftCard.objects.gift_card_for_date(gift_card_code, date)
        discount = gift_card.amount

    return discount


class RetrieveProductPriceAPIView(RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        data = {
            'productCode': request.GET.get('productCode'),
            'date': request.GET.get('date'),
            'giftCardCode': request.GET.get('giftCardCode') or "",
        }

        serializer = QuerySerializer(data=data)

        if not serializer.is_valid():
            return JsonResponse(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        product_price = (
            Product.objects.get(
                code=serializer.data['productCode']
            ).get_price(
                date=serializer.data['date']
            )
        )

        discount = calculate_discount(
            serializer.data['giftCardCode'],
            serializer.data['date'],
        )

        return JsonResponse(
            data={'price': max(product_price - discount, 0)},
            status=status.HTTP_200_OK,
        )