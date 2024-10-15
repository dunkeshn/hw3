from django.db import models


class Product(models.Model):
    class Category(models.TextChoices):
        DRINK = 'DRINK', 'Напиток'
        DESSERT = 'DESSERT', 'Десерт'
        HOT = 'HOT', 'Горячее блюдо'

    class Availability(models.TextChoices):
        ABSENT = 'ABSENT', 'Товар отсутствует'
        AVAILABLE = 'AVAILABLE', 'В наличии'

    name = models.CharField('Название товара', max_length=255)
    price = models.DecimalField(verbose_name='Цена товара', max_digits=10, decimal_places=2)
    description = models.TextField('Описание товара', null=True, blank=True, )
    category = models.CharField('Категория товара', max_length=100, choices=Category.choices, null=True)
    availability = models.CharField('Наличие', max_length=100, choices=Availability.choices,
                                    default=Availability.AVAILABLE)
    image = models.ImageField('Фотография товара', blank=True)
    create_date = models.DateField('Дата создания товара', auto_now_add=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ('create_date',)

    def __str__(self):
        return self.name


class Cafe(models.Model):
    geolocation = models.CharField('Геолокация (заглушка)', max_length=255)
    address = models.TextField('Адрес кофейни')
    barista_number = models.IntegerField('Число бариста на смене')

    class Meta:
        verbose_name = 'Кофейня'
        verbose_name_plural = 'Кофейни'
        ordering = ('barista_number',)

    def __str__(self):
        return self.address


class Order(models.Model):
    class DeliveryStatus(models.TextChoices):
        PAYING = 'PAYING', 'Оплата заказа'
        PREPARING = 'PREPARING', 'Заказ готовится'
        DELIVERING = 'DELIVERING', 'Заказ доставляется'
        RECEIVED = 'RECEIVED', 'Заказ получен'

    class PaymentMethod(models.TextChoices):
        BANK_CARD = 'BANK_CARD', 'Банковская карта'

    products = models.ManyToManyField(to=Product, related_name='orders',
                                      verbose_name='Товары')
    cafe = models.ForeignKey(to=Cafe, on_delete=models.PROTECT, related_name='orders', verbose_name='Кофейни',
                             null=True)
    sum = models.DecimalField(verbose_name='Сумма', max_digits=10, decimal_places=2)
    delivery_status = models.CharField('Статус доставки', max_length=100, choices=DeliveryStatus.choices,
                                       default=DeliveryStatus.PAYING)
    payment_method = models.CharField('Способ оплаты', max_length=100, choices=PaymentMethod.choices, null=True)
    address = models.TextField('Адрес')
    waiting_time = models.TimeField('Время доставки')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ('waiting_time',)

    def __str__(self):
        return self.address


class Courier(models.Model):
    class CourierCategory(models.TextChoices):
        FOOT = 'FOOT', 'Пеший курьер'
        BICYCLE = 'BICYCLE', 'Велокурьер'
        CAR = 'CAR', 'Автокурьер'

    class CourierStatus(models.TextChoices):
        AT_WORK = 'AT_WORK', 'На работе'
        RELAXING = 'RELAXING', 'Отдыхает'
        BREAK = 'BREAK', 'Перерыв'

    name = models.CharField('Имя', max_length=255)
    courier_category = models.CharField(
        'Категория курьера',
        max_length=100,
        choices=CourierCategory.choices,
        default=CourierCategory.CAR
    )
    courier_status = models.CharField(
        'Статус курьера',
        max_length=100,
        choices=CourierStatus.choices
    )

    class Meta:
        verbose_name = 'Курьер'
        verbose_name_plural = 'Курьеры'
        ordering = ('courier_status',)

    def __str__(self):
        return self.name


class Cart(models.Model):
    products = models.ManyToManyField(to=Product, related_name='carts', verbose_name='Товары')
    sum = models.DecimalField(verbose_name='Сумма', max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        ordering = ('sum',)

    def __str__(self):
        return f'Корзина {self.id} на сумму {self.sum}'

class DeliveryDescription(models.Model):
    description = models.TextField('Описание доставки', null=True, blank=True)

    class Meta:
        verbose_name = 'Описание'
        verbose_name_plural = 'Описания'
        ordering = ('id',)

    def __str__(self):
        return 'Описание'


class Delivery(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.PROTECT, related_name='deliveries', verbose_name='Заказ')
    time_left = models.TimeField('Времени доставки прошло')
    geolocation = models.CharField('Геолокация (заглушка)', max_length=255)
    courier = models.ForeignKey(to=Courier, on_delete=models.PROTECT, related_name='deliveries', verbose_name='Курьер')
    description = models.OneToOneField(to=DeliveryDescription, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = 'Доставка'
        verbose_name_plural = 'Доставки'
        ordering = ('time_left',)

    def __str__(self):
        return f'Доставка #{self.id}'
