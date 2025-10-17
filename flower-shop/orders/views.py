# orders/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import OrderForm
from .models import Order, OrderItem
from .cart import Cart
from catalog.models import Bouquet

def order_create(request):
    cart = Cart(request)
    if not cart:
        messages.error(request, "Ваша корзина пуста.")
        return redirect('catalog:bouquet_list')  # ← позже создадим

    if request.method == 'POST':
        form = OrderForm(request.POST, user=request.user)
        if form.is_valid():
            # Создаём заказ
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.save()

            # Добавляем товары из корзины
            for item in cart:
                bouquet = item['bouquet']
                OrderItem.objects.create(
                    order=order,
                    bouquet=bouquet,
                    quantity=item['quantity'],
                    price_at_order=bouquet.price
                )

            # Очищаем корзину
            cart.clear()

            messages.success(request, f"Заказ №{order.id} успешно оформлен!")
            return redirect('orders:order_success', order_id=order.id)
    else:
        form = OrderForm(user=request.user)

    return render(request, 'orders/order_form.html', {'form': form, 'cart': cart})

def order_success(request, order_id):
    return render(request, 'orders/order_success.html', {'order_id': order_id})