from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('bouquet', 'quantity', 'price_at_order')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_email', 'status', 'delivery_name', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('delivery_name', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [OrderItemInline]

    def user_email(self, obj):
        return obj.user.email if obj.user else "Гость"
    user_email.short_description = "Email пользователя"