from django import template
from post_page.models import FavoritePost

register = template.Library()

@register.filter
def join_slashes(categories):
    return '/'.join(category.slug for category in categories)


