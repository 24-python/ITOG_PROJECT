from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse

class Bouquet(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Название букета",
        help_text="Например: «Романтика», «Полевой букет», «VIP-сборка»"
    )
    description = models.TextField(
        verbose_name="Описание",
        blank=True,
        help_text="Состав, особенности, повод для подарка"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Цена (в рублях)"
    )
    image = models.ImageField(
        upload_to='bouquets/',
        blank=True,
        null=True,
        verbose_name="Изображение букета"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Отображать в каталоге"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Букет"
        verbose_name_plural = "Букеты"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} — {self.price} ₽"

    def get_absolute_url(self):
        return reverse('bouquet-detail', kwargs={'pk': self.pk})