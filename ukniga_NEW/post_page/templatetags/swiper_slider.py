# from django import template
# from django.template.loader import render_to_string
# from django.conf import settings
# from models import Slider  # Импорт модели Slider
# from . import mark_safe

# register = template.Library()

# @register.simple_tag
# def swiper_slider(slider_title):
#     try:
#         slider = Slider.objects.get(title=slider_title)
#         # Здесь вы можете создать HTML-код для вашего слайдера на основе данных из модели Slider
#         slider_html = f'<div class="slider">...</div>'  # Замените на ваш реальный HTML код
#         return mark_safe(slider_html)  # Помечаем как безопасный HTML

#     except Slider.DoesNotExist:
#         return ''


# from django import template
# from django.utils.safestring import mark_safe
# from ..models import Slider

# register = template.Library()

# @register.simple_tag
# def swiper_slider(slider_title):
#     try:
#         slider = Slider.objects.get(title=slider_title)
        
#         # Здесь создайте код Swiper-слайдера, используя данные из модели Slider
#         # Ниже пример кода для Swiper-слайдера
#         slider_html = '''
#             <div class="swiper-container">
#                 <div class="swiper-wrapper">
#                     {% for slide in slider.slides.all %}
#                         <div class="swiper-slide">
#                             <img src="{{ slide.image.url }}" alt="{{ slide.caption }}">
#                         </div>
#                     {% endfor %}
#                 </div>
#                 <div class="swiper-pagination"></div>
#                 <div class="swiper-button-next"></div>
#                 <div class="swiper-button-prev"></div>
#             </div>
            
#             <script>
#                 var swiper = new Swiper('.swiper-container', {
#                     pagination: {
#                         el: '.swiper-pagination',
#                     },
#                     navigation: {
#                         nextEl: '.swiper-button-next',
#                         prevEl: '.swiper-button-prev',
#                     },
#                 });
#             </script>
#         '''.strip()
        
#         return mark_safe(slider_html)  # Помечаем как безопасный HTML

#     except Slider.DoesNotExist:
#         return ''



