from django import template
from slider.models import Slider


register = template.Library()

@register.inclusion_tag('slider_template.html')
def render_slider(slider_id):
    try:
        slider = Slider.objects.get(slider_id=slider_id)
    except Slider.DoesNotExist:
        slider = None
    return {'slider': slider}

