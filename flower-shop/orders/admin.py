# orders/admin.py
from django.contrib import admin
from .models import Order, OrderItem
from .models import Bouquet

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1  # сколько пустых форм показывать
    autocomplete_fields = ['bouquet']  # поиск по букетам (если много)

    # Защита: нельзя удалить, если заказ подтверждён
    def has_delete_permission(self, request, obj=None):
        if obj and obj.order and obj.order.status != 'pending':
            return False
        return super().has_delete_permission(request, obj)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_email', 'status', 'delivery_name', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('delivery_name', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [OrderItemInline]

    def user_email(self, obj):
        return obj.user.email if obj.user else "Гость"
    user_email.short_description = "Email"

    # Защита: нельзя редактировать подтверждённый заказ
    def has_change_permission(self, request, obj=None):
        if obj and obj.status not in ['pending', 'cancelled']:
            return False
        return super().has_change_permission(request, obj)