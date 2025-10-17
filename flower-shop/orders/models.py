from django.db import models
from django.conf import settings
from django_cryptography.fields import encrypt

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
    delivery_name = models.CharField(max_length=255, blank=True)
    delivery_phone = encrypt(models.CharField(max_length=16, blank=True))
    delivery_address = encrypt(models.TextField(blank=True))
    delivery_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
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
    bouquet = models.ForeignKey('catalog.Bouquet', on_delete=models.PROTECT)  # ← строка!
    quantity = models.PositiveIntegerField(default=1)
    price_at_order = models.DecimalField(max_digits=10, decimal_places=2)