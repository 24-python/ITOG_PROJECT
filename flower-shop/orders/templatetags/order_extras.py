# orders/templatetags/order_extras.py
from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    """Умножает value на arg"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0