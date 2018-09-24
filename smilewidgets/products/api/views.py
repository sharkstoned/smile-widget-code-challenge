from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from django.http import JsonResponse

from products.models import Product, GiftCard
from .serializers import QuerySerializer


class RetrieveProductPriceAPIView(RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        data = {
            'product_code': request.GET.get('product_code'),
            'date': request.GET.get('date'),
            'gift_card_code': request.GET.get('gift_card_code', ''),
        }

        serializer = QuerySerializer(data=data)

        if not serializer.is_valid():
            return JsonResponse(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        product = Product.objects.filter(
            code=serializer.data['product_code']
        ).first()

        final_price = product.get_discount_price(
            serializer.data['gift_card_code'],
            serializer.data['date'],
        )

        return JsonResponse(
            data={'price': final_price},
            status=status.HTTP_200_OK,
        )