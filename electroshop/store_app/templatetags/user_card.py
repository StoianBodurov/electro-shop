from django import template
from django.db.models import Sum

from electroshop.store_app.models import Item, Order

register = template.Library()


def get_order_total_price(products):
    return sum(item.item.price * item.quantity for item in products)


@register.inclusion_tag('custom_tags_template/user_card.html')
def user_card(user):
    orders = Order.objects.filter(user_id=user.id, status='added')
    total_price = round(get_order_total_price(orders), 2)
    return {'orders': orders, 'total_price': total_price}
