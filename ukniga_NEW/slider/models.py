from django.db import models



class Image(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    image = models.ImageField(upload_to='images/', verbose_name='Изображение')
    url = models.URLField(blank=True, null=True, verbose_name='URL')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'


class Slider(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    slider_id = models.SlugField(unique=True, verbose_name='Уникальный ID слайдера')
    images = models.ManyToManyField(Image, verbose_name='Изображения', related_name='sliders')
    html_code = models.TextField(blank=True, null=True, verbose_name='HTML-код слайдера')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Слайдер'
        verbose_name_plural = 'Слайдеры'
        
    # def generate_slider_html(self):
    #     # Получаем все изображения, связанные с этим слайдером
    #     images = self.images.all()

    #     # Создаем список HTML-кодов для каждого изображения
    #     image_html = []
    #     for image in images:
    #         image_html.append(f'<img src="{image.image.url}" alt="{image.title}">')

    #     # Собираем HTML-код для слайдера, вставляя изображения
    #     slider_html = f'<div class="carousel" data-flickity=\'{{ "autoPlay": 6000 , "wrapAround": true }}\'>\n'
    #     slider_html += '\n'.join(image_html)
    #     slider_html += '\n</div>'

    #     return slider_html
    def generate_slider_html(self):
        # Получаем все изображения, связанные с этим слайдером
        images = self.images.all()

        # Создаем список HTML-кодов для каждого изображения
        image_html = []
        for image in images:
            # Используем image.url, если он существует, иначе используем 'your_target_url'
            target_url = image.url if image.url else 'your_target_url'
            image_html.append(f'<a href="{target_url}"><img src="{image.image.url}" alt="{image.title}"></a>')

        # Собираем HTML-код для слайдера, вставляя изображения
        slider_html = f'<div class="carousel" data-flickity=\'{{ "autoPlay": 6000 , "wrapAround": true }}\'>\n'
        slider_html += '\n'.join(image_html)
        slider_html += '\n</div>'

        return slider_html

class Banner(models.Model):
    DEPTH_CHOICES = (
        ('main', 'Главная'),
        ('all', 'Все'),
    )

    title = models.CharField(max_length=100, verbose_name='Заголовок')
    image_mobile = models.ImageField(upload_to='banners/', verbose_name='Изображение (мобильное), размер 360*80 px')
    image_tablet = models.ImageField(upload_to='banners/', verbose_name='Изображение (планшет), размер 670*150 px')
    image_desktop = models.ImageField(upload_to='banners/', verbose_name='Изображение (десктоп), размер 940*150 px')
    place = models.CharField(max_length=100, default='default', blank=True, verbose_name='Место расположения баннера')
    url = models.URLField(verbose_name='URL')
    show_on_main = models.BooleanField(default=True, verbose_name='Показывать на главной странице')

    class Meta:
        verbose_name = 'Баннер'
        verbose_name_plural = 'Баннеры'

    def get_depth_display(self):
        return dict(self.DEPTH_CHOICES).get(self.place, self.place)