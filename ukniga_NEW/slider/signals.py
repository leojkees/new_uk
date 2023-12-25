from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Slider

@receiver(m2m_changed, sender=Slider.images.through)
def update_slider_html(sender, instance, **kwargs):
    if 'action' in kwargs and kwargs['action'] in ('post_add', 'post_remove', 'post_clear'):
        instance.html_code = instance.generate_slider_html()
        instance.save()
