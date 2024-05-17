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
from django.conf import settings
from django_q.tasks import schedule
from .tasks import check_and_publish_post
from django.db import connection




User.add_to_class('subscribe', models.BooleanField(default=False))


class MyPermissions(models.Model):
    class Meta:
        permissions = [
            ("can_view_content", "Can view content"),
            # Добавьте здесь другие разрешения, если нужно
        ]


#Файловый браузер
def upload_to_folder(instance, filename):
    return f'{instance.upload_folder}/{filename}'

class MyFile(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to=upload_to_folder)
    wrap_image = models.BooleanField(default=False, verbose_name='Картинка с обтеканием')
    upload_folder = models.CharField(max_length=100, default='uploads', verbose_name='Папка загрузки')

    class Meta:
        verbose_name = "Файл"
        verbose_name_plural = "Файловый браузер"
# class MyFile(models.Model):
#     name = models.CharField(max_length=100)
#     file = models.FileField(upload_to='uploads/')

#     def save(self, *args, **kwargs):
#         original_filename = self.file.name
#         extension = os.path.splitext(original_filename)[1]
#         # Сохраняем только расширение оригинального файла
#         self.file.name = self.name + extension
#         super(MyFile, self).save(*args, **kwargs)
        
#     class Meta:
#         verbose_name = "Файл"
#         verbose_name_plural = "Файловый браузер"


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
    
    title = models.CharField('Заголовок записи', max_length=200)
    description = models.TextField('Краткое описание', max_length=200)
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
    is_featured = models.BooleanField('Выводить на главной', default=False)


    @staticmethod
    def search(query):
        # Разбиваем запрос на отдельные слова и формируем строку с учетом весов полей
        words = query.split()
        query_with_weights = ' '.join([f'+{word}' for word in words])

        # Формируем условие для поиска, где оба слова должны встречаться в одном поле
        query_condition = ' '.join([f'(+{word})' for word in words])

        # Составляем SQL запрос с учетом весов полей и условия поиска
        sql_query = (
            "SELECT *, MATCH(title, description, text) AGAINST (%s IN BOOLEAN MODE) AS relevance "
            "FROM post_page_post "
            "WHERE MATCH(title, description, text) AGAINST (%s IN BOOLEAN MODE) AND "
            f"(MATCH(title, description, text) AGAINST ('{query_condition}' IN BOOLEAN MODE)) AND is_published = True "
            "ORDER BY relevance DESC"
        )

        return Post.objects.raw(sql_query, [query_with_weights, query_with_weights])


        

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

        # Текущее время
        local_time = timezone.localtime(timezone.now())

        # Логика публикации
        if self.is_published:
            if self.published_date and self.published_date > local_time:
                # Если время публикации в будущем, делаем пост невидимым на публичных страницах
                self.is_published = False
            else:
                # Время текущее или прошлое, пост публикуется
                self.is_published = True
        else:
            # Если чекбокс не выбран или снят, пост не виден на публичных страницах
            self.is_published = False

        # Сохраняем изменения
        super(Post, self).save(*args, **kwargs)

        # Планирование задачи на будущее время, если нужно
        if self.published_date and self.published_date > timezone.localtime():
            schedule('post_page.tasks.check_and_publish_post', self.id, schedule_type='O', next_run=self.published_date)

        # Логика снятия с публикации
        if self.unpublished_date:
            if self.unpublished_date <= local_time:
                # Если дата окончания публикации в прошлом или настоящем, снимаем пост с публикации
                self.is_published = False
                super(Post, self).save(*args, **kwargs)
            else:
                # Планирование задачи на будущее время для снятия с публикации
                schedule('post_page.tasks.check_and_unpublish_post', self.id, schedule_type='O', next_run=self.unpublished_date)
        

    def get_image_absolute_url(self):
        return f"{settings.SITE_URL}{self.img.url}"
        
    
    def get_absolute_url(self):
        # Используем URL-паттерн 'post_detail' если у поста есть slug и хотя бы одна категория
        if self.slug and hasattr(self, 'category') and self.category.exists():
            category_slug = self.category.all().order_by('slug').first().slug
            return reverse('post_detail', kwargs={'category_slug': category_slug, 'slug': self.slug})

        # Используем URL-паттерн 'posts_by_year' если у поста есть дата
        if hasattr(self, 'date') and self.date:
            return reverse('posts_by_year', kwargs={'year': self.date.year, 'month': self.date.month})

        # Возвращаем URL для просмотра деталей поста или платного контента в зависимости от подписки автора
        if hasattr(self, 'author') and self.author.subscribe:
            return reverse('post_detail', kwargs={'post_id': self.id})
        else:
            return reverse('paid')

        # Если ни одно из условий не выполнено, можно вернуть главную страницу или другой стандартный URL
        return reverse('home')
 
    
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