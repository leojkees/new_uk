from django.contrib import admin
from .models import Post, Category, Tag, MyFile
from ckeditor.widgets import CKEditorWidget
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
import os
from django_summernote.widgets import SummernoteWidget
from django_summernote.admin import SummernoteModelAdmin
from .models import StaticTemplate
from userprofile.models import Profile
from .models import MyFile
from django.conf import settings
from django import forms
from django.urls import reverse

#редактирование содержимого шаблонов страниц
class StaticTemplateAdmin(SummernoteModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


# class MyFileAdmin(admin.ModelAdmin):
#     list_display = ('display_name', 'file_thumbnail', 'file_html_code')

#     def display_name(self, obj):
#         return obj.name
#     display_name.short_description = "Имя файла"

#     def file_thumbnail(self, obj):
#         if obj.file:
#             # Обертываем миниатюру в ссылку для открытия файла
#             return format_html("<a href='{}'><img src='{}' alt='{}' style='height:50px;'/></a>", obj.file.url, obj.file.url, obj.file.name)
#         return "-"
#     file_thumbnail.short_description = "Миниатюра"

#     def file_html_code(self, obj):
#         if obj.file:
#             filename, file_extension = os.path.splitext(obj.file.name)
#             if file_extension.lower() in ['.jpg', '.jpeg', '.png', '.gif']:
#                 # Правильно сформированный HTML-код для изображения
#                 html_code = "<img src='{}' alt='{}' class='img-fluid w-75'>".format(obj.file.url, obj.name)
#             else:
#                 # Правильно сформированный HTML-код для других файлов
#                 html_code = "<a href='{}' alt='{}'>{}</a>".format(obj.file.url, obj.name, obj.name)
#             return format_html("<textarea rows='2' cols='100' readonly>{}</textarea>", html_code)
#         return "-"
#     file_html_code.short_description = "HTML для вставки"

#     fields = ('name', 'file')
class MyFileAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'file_thumbnail', 'file_html_code', 'upload_folder')
    fields = ('name', 'file', 'wrap_image', 'upload_folder')

    list_filter = ( 'name', 'upload_folder',
    )

    def display_name(self, obj):
        return obj.name
    display_name.short_description = "Имя файла"

    def file_thumbnail(self, obj):
        if obj.file:
            return format_html("<a href='{}'><img src='{}' alt='{}' style='height:100px;'/></a>", obj.file.url, obj.file.url, obj.name)
        return "-"
    file_thumbnail.short_description = "Миниатюра"

    def file_html_code(self, obj):
        if obj.file:
            filename, file_extension = os.path.splitext(obj.file.name)
            if obj.wrap_image:
                # HTML структура для случая с wrap_image, отформатирована правильно
                html_code = (
                    f"<figure class='figure w-25 float-start m-3'>"
                    f"<img src='{obj.file.url}' class='figure-img img-fluid rounded img-thumbnail' alt='{obj.name}'>"
                    f"</figure>"
                )
            else:
                # HTML структура для случая без wrap_image
                img_class = 'img-fluid w-100 mb-3 rounded'
                html_code = f"<img src='{obj.file.url}' alt='{obj.name}' class='{img_class}'>"
            
            if file_extension.lower() not in ['.jpg', '.jpeg', '.png', '.gif']:
                # Если файл не изображение, то выводим ссылку на файл
                html_code = f"<a href='{obj.file.url}' alt='{obj.name}'>{obj.name}</a>"

            # Возвращаем HTML-код внутри текстового поля для удобного копирования
            return format_html("<textarea rows='4' cols='100' readonly>{}</textarea>", html_code)
        return "-"
    file_html_code.short_description = "HTML для вставки"





# class PostAdmin(admin.ModelAdmin):
#     list_display = ('title', 'description', 'display_categories', 'is_paid', 'display_tags', 'is_arhive', 'month', 'year', 'image')
#     list_filter = ('category', 'tags')
#     search_fields = ('title', 'description', 'category__name', 'tags__name')
    
#     formfield_overrides = {
#         'models.TextField': {'widget': CKEditorWidget},
#     }
    
#     def display_categories(self, obj):
#         return format_html(", ".join([category.name for category in obj.category.all()]))
#     display_categories.short_description = 'Категории'

#     def display_tags(self, obj):
#         return format_html(", ".join([tag.name for tag in obj.tags.all()]))
#     display_tags.short_description = 'Теги'
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'display_categories', 'is_paid', 
        'display_tags', 'is_arhive', 'month', 'year', 'image',
        'published_date', 'is_published', 'view_on_site_link'  # Добавленные поля
    )
    list_filter = (
        'category', 'tags', 'is_published', 'published_date', 'month', 'year',  # Добавленные фильтры
    )
    search_fields = (
        'title', 'category__name', 'tags__name',
        'published_date'  
    )
    formfield_overrides = {
        'models.TextField': {'widget': SummernoteWidget()},
    }

    def display_categories(self, obj):
        return format_html(", ".join([category.name for category in obj.category.all()]))
    display_categories.short_description = 'Категории'

    def display_tags(self, obj):
        return format_html(", ".join([tag.name for tag in obj.tags.all()]))
    display_tags.short_description = 'Теги'

    def view_on_site_link(self, obj):
        # Проверяем, есть ли категории у поста
        if obj.category.all().exists():
            # Берем первую категорию по алфавиту или по умолчанию
            category = obj.category.all().order_by('slug').first()
            url = reverse('post_detail', args=[category.slug, obj.slug])
            url += '/preview/'  # Добавляем /preview/ к URL
            return format_html("<a href='{}'>Предпросмотр</a>", url)
        return "No category"

    view_on_site_link.short_description = "Предпросмотр"


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'subscribe', 'is_staff', 'is_active')
    list_filter = ('subscribe', 'is_staff', 'is_active')
    
    # Добавьте поле subscribe в fields или fieldsets
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'subscribe')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )


# @admin.register(Date)
# class DateAdmin(admin.ModelAdmin):
#     list_display = ('year', 'month', 'image')  # Определите, какие поля отображать в списке объектов
#     search_fields = ('year', 'month')  # Добавьте поля для поиска
#     list_filter = ('year', 'month')  # Добавьте фильтры для списка
#     ordering = ('year', 'month')  # Задайте сортировку

#     # Опционально, если у вас есть необходимость настроить форму редактирования объекта
#     fieldsets = (
#         (None, {
#             'fields': ('year', 'month', 'image')
#         }),
#     )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)


# Зарегистрируйте модель User с кастомным административным классом
admin.site.unregister(User)  # Снимите регистрацию стандартной модели User
admin.site.register(User, CustomUserAdmin)  # Зарегистрируйте её с кастомным административным классом
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(MyFile, MyFileAdmin)
admin.site.register(StaticTemplate, StaticTemplateAdmin)