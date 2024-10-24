import factory
from factory.django import ImageField

from core import models

class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Product

    name = factory.Faker('sentence', nb_words=3)
    price = factory.Faker('random_number', digits=3, fix_len=True)
    description = factory.Faker('text')
    category = models.Product.Category.DRINK
    availability = models.Product.Availability.AVAILABLE

class CafeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Cafe

    geolocation = factory.Faker('address')
    address = factory.Faker('address')
    barista_number = factory.Faker('random_int', min=1, max=10)

class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Order

    cafe = factory.SubFactory(CafeFactory)
    sum = factory.Faker('random_number', digits=3, fix_len=True)
    delivery_status = models.Order.DeliveryStatus.PAYING
    payment_method = models.Order.PaymentMethod.BANK_CARD
    address = factory.Faker('address')
    waiting_time = factory.Faker('time')