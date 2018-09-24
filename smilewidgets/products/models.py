from django.db import models
from django.db.models import Q


class Product(models.Model):
    name = models.CharField(max_length=25, help_text='Customer facing name of product')
    code = models.CharField(max_length=10, help_text='Internal facing reference to product')
    price = models.PositiveIntegerField(help_text='Price of product in cents')

    def get_price(self, date):
        product_price_qs = self.prices.filter(
            Q(date_start__lte=date, date_end__gte=date) |
            Q(date_start__lte=date, date_end__isnull=True)
        )
        if product_price_qs.first():
            return product_price_qs.first().price
        return self.price

    def get_discount_price(self, gift_card_code, date):
        discount = 0

        if gift_card_code:
            gift_card = GiftCard.objects.gift_card_for_date(gift_card_code, date)
            discount = gift_card.amount

        default_price = self.get_price(date=date)

        return max(default_price - discount, 0)

    def __str__(self):
        return '{} - {}'.format(self.name, self.code)


class GiftCardQuerySet(models.QuerySet):
    def gift_card_for_date(self, card_code, date):
        return self.filter(
            Q(
                date_start__lte=date,
                date_end__gte=date,
            ) |
            Q(
                date_start__lte=date,
                date_end__isnull=True,
            )
        ).get(code=card_code)


class GiftCard(models.Model):
    code = models.CharField(max_length=30)
    amount = models.PositiveIntegerField(help_text='Value of gift card in cents')
    date_start = models.DateField()
    date_end = models.DateField(blank=True, null=True)

    objects = GiftCardQuerySet.as_manager()

    def __str__(self):
        return '{} - {}'.format(self.code, self.formatted_amount)

    @property
    def formatted_amount(self):
        return '${0:.2f}'.format(self.amount / 100)


class ProductPrice(models.Model):
    date_start = models.DateField()
    date_end = models.DateField(blank=True, null=True)

    product = models.ForeignKey(
        Product,
        null=True,
        on_delete=models.CASCADE,
        related_name='prices',

    )

    price = models.PositiveIntegerField()
