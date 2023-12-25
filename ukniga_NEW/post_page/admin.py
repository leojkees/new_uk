from django.contrib import admin
from .models import Post, Category, Tag
from ckeditor.widgets import CKEditorWidget
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html




class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


# class PostAdmin(admin.ModelAdmin):
#     list_display = ('title', 'description', 'year', 'month', 'category', 'is_paid', 'tags')
#     list_filter = ('year', 'month', 'category', 'tags')
#     search_fields = ('title', 'description', 'year', 'month', 'category__name', 'tags__name')
#     formfield_overrides = {
#         'models.TextField': {'widget': CKEditorWidget},
#     }
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'display_categories', 'is_paid', 'display_tags', 'is_arhive', 'month', 'year', 'image')
    list_filter = ('category', 'tags')
    search_fields = ('title', 'description', 'category__name', 'tags__name')
    formfield_overrides = {
        'models.TextField': {'widget': CKEditorWidget},
    }
    
    def display_categories(self, obj):
        return format_html(", ".join([category.name for category in obj.category.all()]))
    display_categories.short_description = 'Категории'

    def display_tags(self, obj):
        return format_html(", ".join([tag.name for tag in obj.tags.all()]))
    display_tags.short_description = 'Теги'


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



# Зарегистрируйте модель User с кастомным административным классом
admin.site.unregister(User)  # Снимите регистрацию стандартной модели User
admin.site.register(User, CustomUserAdmin)  # Зарегистрируйте её с кастомным административным классом
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)