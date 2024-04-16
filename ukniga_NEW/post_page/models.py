from django.db import models
from slugify import slugify
from django_ckeditor_5.fields import CKEditor5Field
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
import os
from django.utils import timezone
from ckeditor.fields import RichTextField
from django_summernote.fields import SummernoteTextField
from django.core.exceptions import ValidationError



User.add_to_class('subscribe', models.BooleanField(default=False))


class MyPermissions(models.Model):
    class Meta:
        permissions = [
            ("can_view_content", "Can view content"),
            # Добавьте здесь другие разрешения, если нужно
        ]


class MyFile(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='uploads/')

    def save(self, *args, **kwargs):
        original_filename = self.file.name
        extension = os.path.splitext(original_filename)[1]
        # Сохраняем только расширение оригинального файла
        self.file.name = self.name + extension
        super(MyFile, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name = "Файл"
        verbose_name_plural = "Файловый браузер"


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=300, blank=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    image = models.ImageField(upload_to='images/category_img', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name



class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name
    



#данные о записи
class Post(models.Model):
    MONTH_CHOICES = [
        ('Январь', 'Январь'), ('Январь/Февраль', 'Январь/Февраль'), ('Февраль', 'Февраль'), ('Март', 'Март'),
        ('Апрель', 'Апрель'), ('Май', 'Май'), ('Июнь', 'Июнь'),
        ('Июль', 'Июль'), ('Июль/Август', 'Июль/Август'), ('Август', 'Август'), ('Сентябрь', 'Сентябрь'),
        ('Октябрь', 'Октябрь'), ('Ноябрь', 'Ноябрь'), ('Декабрь', 'Декабрь')
    ]
    
    title = models.CharField('Заголовок записи', max_length=150)
    description = SummernoteTextField('Краткое описание', max_length=150)
    text = SummernoteTextField()
    page = models.IntegerField('Номер страницы в журнале', default=None, blank=True, null=True)
    img = models.ImageField('Главное изображение поста', upload_to='images/%Y/%m-%d')
    img_card = models.ImageField('Фото для карточки категорий', upload_to='images/%Y/%m-%d', default=None)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    category = models.ManyToManyField(Category, related_name='Category')
    tags = models.ManyToManyField('Tag', related_name='posts')
    year = models.IntegerField('Год', validators=[MinValueValidator(2000), MaxValueValidator(2100)])
    month = models.CharField('Месяц', max_length=20, choices=MONTH_CHOICES)
    image = models.ImageField('Обложка архива', upload_to='date_images/', default='', blank=True, null=True)
    is_paid = models.BooleanField('Платный материал', default=False)
    is_arhive = models.BooleanField('Архив', default=False)
    published_date = models.DateTimeField('Дата публикации', null=True, blank=True)
    is_published = models.BooleanField('Опубликовано', default=False)

    def clean(self):
        if self.is_arhive and not self.image:
            raise ValidationError("Поле: Обложка архива - обязательно для архивной статьи.")    

    CARD_DISPLAY_CHOICES = [
        ('default', 'Фото + Заголовок'),
        ('fullscreen', 'Фото на всю ширину с оверфлоу + Заголовок поверх фото'),
        ('NoFoto', 'Без фото'),
    ]

    card_display = models.CharField('Вид карточки', max_length=20, choices=CARD_DISPLAY_CHOICES, default='default')

    def get_id(self):
        return self.id
    get_id.short_description = 'ID'

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'


    def save(self, *args, **kwargs):

        # Если slug не был указан явно, генерируем его на основе title
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

        # Получаем оригинальный объект из базы данных для сравнения
        if self.pk:
            original = Post.objects.get(pk=self.pk)
        else:
            original = None

        # Автоматическая установка is_published в True, если наступила дата публикации
        # и если поле is_published не было изменено вручную на False
        if self.published_date and self.published_date <= timezone.now():
            if original is None or original.is_published:
                self.is_published = True

        super().save(*args, **kwargs)
        
    
    def get_absolute_url(self):
        # Если self.slug определен, используйте URL-паттерн 'post_detail'
        # if self.slug:
        #     return reverse('post_detail', kwargs={'slug': self.slug})
        if self.slug:
            return reverse('post_detail', kwargs={'category_slug': self.category.slug, 'slug': self.slug})
        
        # Если self.date определен, используйте URL-паттерн 'posts_by_year' с годом
        # if self.date:
        #     return reverse('posts_by_year', args=[str(self.date.year)])
        if self.date:
            return reverse('posts_by_year', args=[str(self.date.year), str(self.date.month)])

        
        if self.author.subscribe:
            return reverse('post_detail', args=[str(self.id)])
        else:
            return reverse('paid')
 
    
    #отображение записей в админке?    
    def __str__(self):
        return f'{self.title}{self.description}'
    
    
    
    
class FavoritePost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.post.title}"
    
    
class StaticTemplate(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название шаблона")
    content = SummernoteTextField(verbose_name="Содержимое")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Статический шаблон"
        verbose_name_plural = "Статические шаблоны"