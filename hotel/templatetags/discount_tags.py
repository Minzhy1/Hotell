from django import template

register = template.Library()

@register.filter
def apply_discount(price, discount):
    try:
        price = float(price)
        discount = float(discount)
        if discount > 0:
            return round(price * (1 - discount / 100), 2)
        return price
    except:
        return price

@register.filter
def is_high_discount(discount):
    try:
        return float(discount) > 10
    except:
        return False