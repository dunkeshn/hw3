from django.test import TestCase
from django.urls import reverse

from core import factories, models


class OrderTestCase(TestCase):
    def setUp(self):
        self.product = factories.ProductFactory()
        self.cafe = factories.CafeFactory()
        self.order = {
            'products': [self.product.pk],
            'cafe': self.cafe.pk,
            'sum': self.product.price,
            'delivery_status': models.Order.DeliveryStatus.PAYING,
            'payment_method': models.Order.PaymentMethod.BANK_CARD,
            'address': 'new_address',
            'waiting_time': '00:05:00'
        }

    def test_create_order(self):
        old_orders_count = models.Order.objects.count()
        response = self.client.post(reverse('order_create'), data=self.order)
        self.assertEqual(response.status_code, 302)
        self.assertNotEqual(models.Order.objects.count(), old_orders_count)

    def test_update_order(self):
        order = factories.OrderFactory(cafe=self.cafe, sum=self.product.price)
        data = {
            'products': [self.product.pk],
            'cafe': self.cafe.pk,
            'sum': self.product.price,
            'delivery_status': models.Order.DeliveryStatus.RECEIVED,
            'payment_method': models.Order.PaymentMethod.BANK_CARD,
            'address': 'new_address',
            'waiting_time': '00:05:00'
        }
        old_address = order.address
        response = self.client.post(reverse('order_update', args=[order.pk]), data=data)
        self.assertEqual(response.status_code, 302)
        order.refresh_from_db()
        self.assertNotEqual(order.address, old_address)

    def test_get_order_address(self):
        response = self.client.get(reverse('order_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['orders'].count(), models.Order.objects.count())

    def test_get_order_detail(self):
        order = factories.OrderFactory(cafe=self.cafe, sum=self.product.price)
        response = self.client.get(reverse('order_detail', args=[order.pk]))
        self.assertEqual(response.status_code, 200)

    def test_delete_order(self):
        order = factories.OrderFactory(cafe=self.cafe, sum=self.product.price)
        old_order_count = models.Order.objects.count()
        response = self.client.delete(reverse('order_delete', args=[order.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertGreater(old_order_count, models.Order.objects.count())
