from django.contrib import admin
from .models import Image, Slider

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'url')

@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'slider_id', 'display_html_code')
    filter_horizontal = ('images',)  # Добавьте это для более удобного выбора изображений в админ-панели

    def display_html_code(self, obj):
        return obj.html_code

    display_html_code.short_description = 'HTML Code'  # Задать заголовок для колонки

