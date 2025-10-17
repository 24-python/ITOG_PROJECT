# orders/forms.py
from django import forms
from .models import Order
from django.core.validators import RegexValidator

class OrderForm(forms.ModelForm):
    # Согласие на ПДн — обязательно!
    consent = forms.BooleanField(
        required=True,
        label='Я даю согласие на обработку персональных данных в целях оформления заказа и доставки',
        error_messages={'required': 'Вы должны дать согласие на обработку ПДн'}
    )

    # Валидация телефона (только РФ, 10-11 цифр)
    phone_validator = RegexValidator(
        regex=r'^\+?7\d{10}$|^8\d{10}$',
        message="Введите корректный номер телефона (например, +79991234567)"
    )

    delivery_phone = forms.CharField(
        max_length=16,
        validators=[phone_validator],
        widget=forms.TextInput(attrs={'placeholder': '+79991234567'})
    )

    class Meta:
        model = Order
        fields = ['delivery_name', 'delivery_phone', 'delivery_address', 'delivery_time']
        widgets = {
            'delivery_address': forms.Textarea(attrs={'rows': 3}),
            'delivery_time': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Если пользователь авторизован — подставляем данные из профиля
        if self.user and self.user.is_authenticated:
            profile = getattr(self.user, 'profile', None)
            if profile:
                self.fields['delivery_phone'].initial = profile.phone
                self.fields['delivery_address'].initial = profile.address
            self.fields['delivery_name'].initial = self.user.get_full_name() or self.user.username