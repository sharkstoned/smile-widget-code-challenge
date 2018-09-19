from django.urls import path

from .views import RetrieveProductPriceAPIView

urlpatterns = [
    path('get-price', RetrieveProductPriceAPIView.as_view(), name='retrieve_product_price')
]