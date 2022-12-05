from django import template

from electroshop.store_app.models import Order
from electroshop.store_app.utils.helpers import get_order_total_price

register = template.Library()


@register.inclusion_tag('custom_tags_template/user_card.html')
def user_card(user):
    orders = Order.objects.filter(user_id=user.id, status='added')
    total_price = get_order_total_price(orders)
    return {'orders': orders, 'total_price': total_price}
