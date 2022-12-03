from django import template
from django.db.models import Avg

from electroshop.common.models import Review

register = template.Library()


@register.inclusion_tag('custom_tags_template/rating_stars.html')
def rating_stars(item):
    avg_rating = Review.objects.filter(item_id=item.id).aggregate(Avg('rating'))
    return {'avg_rating': avg_rating['rating__avg']}


