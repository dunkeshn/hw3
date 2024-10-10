from django.db import models


class Product(models.Model):
    name = models.CharField('Название товара', max_length=255)
    price = models.FloatField('Цена товара')
    description = models.TextField('Описание товара', null=True, blank=True, )
    category = models.CharField('Категория товара', max_length=100, choices=[
        ('DRINK', 'Напиток'),
        ('DESSERT', 'Десерт'),
        ('HOT', 'Горячее блюдо'),
    ], null=True)
    availability = models.CharField('Наличие', max_length=100, choices=[
        ('ABSENT', 'Товар отсутствует'),
        ('AVAILABLE', 'В наличии'),
    ], default='AVAILABLE')
    image = models.ImageField('Фотография товара', blank=True)
    create_date = models.DateField('Дата создания товара', auto_now_add=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ('create_date', )

    def __str__(self):
        return self.name


class Cafe(models.Model):
    geolocation = models.CharField('Геолокация (заглушка)', max_length=255)
    address = models.TextField('Адрес кофейни')
    barista_number = models.IntegerField('Число бариста на смене')

    class Meta:
        verbose_name = 'Кофейня'
        verbose_name_plural = 'Кофейни'
        ordering = ('barista_number', )

    def __str__(self):
        return self.address


class Order(models.Model):
    products = models.ManyToManyField(to=Product, related_name='orders',
                                      verbose_name='Товары')
    cafe = models.ForeignKey(to=Cafe, on_delete=models.PROTECT, related_name='orders', verbose_name='Кофейни',
                             null=True)
    sum = models.FloatField('Сумма')
    delivery_status = models.CharField('Статус доставки', max_length=100, choices=[
        ('PAYING', 'Оплата заказа'),
        ('PREPARING', 'Заказ готовится'),
        ('DELIVERING', 'Заказ доставляется'),
        ('RECEIVED', 'Заказ получен'),
    ], default='PAYING')
    payment_method = models.CharField('Способ оплаты', max_length=100, choices=[
        ('BANK_CARD', 'Банковская карта'),
    ], null=True)
    address = models.TextField('Адрес')
    waiting_time = models.TimeField('Время доставки')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ('waiting_time', )

    def __str__(self):
        return self.address


class Courier(models.Model):
    name = models.CharField('Имя', max_length=255)
    courier_category = models.CharField('Категория курьера', max_length=100, choices=[
        ('FOOT', 'Пеший курьер'),
        ('BICYCLE', 'Велокурьер'),
        ('CAR', 'Автокурьер'),
    ], default='CAR')
    courier_status = models.CharField('Категория курьера', max_length=100, choices=[
        ('AT_WORK', 'На работе'),
        ('RELAXING', 'Отдыхает'),
        ('BREAK', 'Перерыв'),
    ])

    class Meta:
        verbose_name = 'Курьер'
        verbose_name_plural = 'Курьеры'
        ordering = ('courier_status', )

    def __str__(self):
        return self.name

class Cart(models.Model):
    products = models.ManyToManyField(to=Product, related_name='carts', verbose_name='Товары')
    sum = models.FloatField('Сумма')

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        ordering = ('sum', )

class DeliveryDescription(models.Model):
    description = models.TextField('Описание доставки', null=True, blank=True)

    class Meta:
        verbose_name = 'Описание'
        verbose_name_plural = 'Описания'
        ordering = ('id', )

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
        ordering = ('time_left', )

    def __str__(self):
        return f'Доставка #{self.id}'







