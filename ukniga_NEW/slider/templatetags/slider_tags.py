from django import template
from slider.models import Slider, Banner


register = template.Library()

@register.inclusion_tag('slider_template.html')
def render_slider(slider_id):
    try:
        slider = Slider.objects.get(slider_id=slider_id)
    except Slider.DoesNotExist:
        slider = None
    return {'slider': slider}


@register.simple_tag
def get_banners(place=None, order_by=None):
    banners = Banner.objects.all()
    if place:
        banners = banners.filter(place=place)
    if order_by:
        banners = banners.order_by(order_by)
    return banners
