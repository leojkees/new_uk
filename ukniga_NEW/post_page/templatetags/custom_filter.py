from django import template

register = template.Library()

@register.filter
def join_slashes(categories):
    return '/'.join(category.slug for category in categories)
