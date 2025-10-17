from django.db import models
from django.conf import settings
from catalog.models import Bouquet

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтверждён'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменён'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Пользователь"
    )
    # ПДн — только если пользователь не авторизован!
    # У авторизованных — берём из профиля.
    delivery_name = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Имя получателя"
    )
    delivery_phone = models.CharField(
        max_length=16,
        blank=True,
        verbose_name="Телефон для доставки"
    )
    delivery_address = models.TextField(
        blank=True,
        verbose_name="Адрес доставки"
    )
    delivery_time = models.DateTimeField(
        verbose_name="Желаемое время доставки"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-created_at']

    def __str__(self):
        user_info = self.user.email if self.user else "Гость"
        return f"Заказ от {user_info} ({self.created_at.strftime('%Y-%m-%d')})"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    bouquet = models.ForeignKey(Bouquet, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    price_at_order = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Цена на момент заказа"
    )

    def __str__(self):
        return f"{self.bouquet.name} × {self.quantity}"