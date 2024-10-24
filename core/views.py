from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Order
from django_filters.views import FilterView
from core import filters


class OrderListView(FilterView):
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'
    filterset_class = filters.Order


class OrderDetailView(DetailView):
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'


class OrderCreateView(CreateView):
    model = Order
    template_name = 'orders/order_form.html'
    fields = ['products', 'cafe', 'sum', 'delivery_status', 'payment_method', 'address', 'waiting_time']
    def get_success_url(self):
        return reverse_lazy('order_list')


class OrderUpdateView(UpdateView):
    model = Order
    template_name = 'orders/order_form.html'
    fields = ['products', 'cafe', 'sum', 'delivery_status', 'payment_method', 'address', 'waiting_time']
    def get_success_url(self):
        return reverse_lazy('order_list')


class OrderDeleteView(DeleteView):
    model = Order
    template_name = 'orders/order_confirm_delete.html'
    success_url = reverse_lazy('order_list')
