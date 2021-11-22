from django.shortcuts import get_object_or_404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.db import transaction

from django.forms import inlineformset_factory

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from basketapp.models import Basket
from ordersapp.models import Order, OrderItem
from ordersapp.forms import OrderItemForm


class OrderList(ListView):
   model = Order

   def get_queryset(self):
       return Order.objects.filter(user=self.request.user)


class OrderItemsCreate(CreateView)
    model = Order
    fields = []
    success_url = reverse_lazy('ordersapp:orders_list')

    OrderFormSet = inlineformset_factory(
        Order, 
        OrderItem, 
        form=OrderItemForm, 
        extra=1
    )

    basket_items = Basket.get_items(self.request.user)
    if len(basket_items):
        OrderFormSet = inlineformset_factory(
            Order, 
            OrderItem, 
            form=OrderItemForm,
            extra=len(basket_items)
        )
        formset = OrderFormSet()
        for num, form in enumerate(formset.forms):
            form.initial['product'] = basket_items[num].product
            form.initial['quantity'] = basket_items[num].quantity
            basket_items.delete()
    else:
        formset = OrderFormSet()
