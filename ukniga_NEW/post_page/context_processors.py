from django.urls import reverse
from .models import Category, Post
import random
from django.db.models import Max


# def latest_post_processor(request):
#     month_mapping = {
#         'Январь': 1, 'Февраль': 2, 'Март': 3,
#         'Апрель': 4, 'Май': 5, 'Июнь': 6,
#         'Июль': 7, 'Август': 8, 'Сентябрь': 9,
#         'Октябрь': 10, 'Ноябрь': 11, 'Декабрь': 12
#     }

#     latest_year = Post.objects.filter(is_arhive=True).aggregate(Max('year'))['year__max']

#     if latest_year:
#         # Фильтрация постов по году и is_arhive=True
#         year_posts = Post.objects.filter(year=latest_year, is_arhive=True)
#         latest_month = max(year_posts, key=lambda post: month_mapping[post.month]).month
        
#         # Фильтрация постов по году, месяцу и is_arhive=True
#         latest_posts = year_posts.filter(month=latest_month)

#         if latest_posts.exists():
#             random_post = random.choice(latest_posts)
#             title = random_post.title
#             image_url = random_post.image.url if random_post.image else None
#             post_slug = random_post.slug
#             category_slug = random_post.category.first().slug if random_post.category.exists() else None
#         else:
#             title = None
#             image_url = None
#             post_slug = None
#             category_slug = None
#     else:
#         title = None
#         image_url = None
#         post_slug = None
#         category_slug = None
#         latest_year = None
#         latest_month = None

#     return {
#         'latest_post_title': title,
#         'latest_post_image': image_url,
#         'latest_post_slug': post_slug,
#         'latest_post_category_slug': category_slug,
#         'latest_post_year': latest_year,
#         'latest_post_month': latest_month
#     }
def latest_post_processor(request):
    month_mapping = {
        'Январь': 1, 'Февраль': 2, 'Март': 3,
        'Апрель': 4, 'Май': 5, 'Июнь': 6,
        'Июль': 7, 'Август': 8, 'Сентябрь': 9,
        'Октябрь': 10, 'Ноябрь': 11, 'Декабрь': 12
    }

    latest_year = Post.objects.filter(is_arhive=True).aggregate(Max('year'))['year__max']

    if latest_year:
        year_posts = Post.objects.filter(year=latest_year, is_arhive=True)
        latest_month = max(year_posts, key=lambda post: month_mapping[post.month]).month
        latest_posts = year_posts.filter(month=latest_month)

        if latest_posts.exists():
            random_post = random.choice(latest_posts)
            title = random_post.title
            post_slug = random_post.slug
            category_slug = random_post.category.first().slug if random_post.category.exists() else None

            # Initially assign image_url from the random post
            image_url = random_post.image.url if random_post.image else None

            # If the random_post doesn't have an image, find the first post in the same year and month that does
            if not image_url:
                for post in latest_posts:
                    if post.image:
                        image_url = post.image.url
                        break

        else:
            title = None
            image_url = None
            post_slug = None
            category_slug = None
    else:
        title = None
        image_url = None
        post_slug = None
        category_slug = None
        latest_year = None
        latest_month = None

    return {
        'latest_post_title': title,
        'latest_post_image': image_url,
        'latest_post_slug': post_slug,
        'latest_post_category_slug': category_slug,
        'latest_post_year': latest_year,
        'latest_post_month': latest_month
    }


def add_breadcrumb(breadcrumbs, url_name, *args, title=None, **kwargs):
    print(f"Adding breadcrumb for URL name: {url_name} with args: {args} and kwargs: {kwargs}")
    
    try:
        url = reverse(url_name, args=args, kwargs=kwargs)
    except Exception as e:
        url = '#'
    
    
    breadcrumbs.append({
        'url': url,
        'title': title or url_name.capitalize().replace('_', ' ')
    })



def menu_and_breadcrumbs(request):
    menu_items = [
        {'title': "Главная", 'url_name': 'home'},
        {'title': "Подробнее", 'url_name': 'post_detail'},
        {'title': "Архив", 'url_name': 'archive_posts'},
        {'title': "Страница поиска", 'url_name': 'search_posts'},
        {'title': "Теги", 'url_name': 'tags'},
        {'title': "Тег", 'url_name': 'tag'},
        {'title': "Избранное", 'url_name': 'manage_favorite'},
        {'title': "Профиль", 'url_name': 'userprofile'},
        {'title': "Страница оплаты", 'url_name': 'paid_view'},
        {'title': "Категории", 'url_name': 'category_posts'},
        {'title': "Архив", 'url_name': 'posts_by_year'},
    ]

    # Пример хлебных крошек
    breadcrumbs = [{'url': reverse('home'), 'title': 'Главная'}]

    # Добавляем хлебные крошки для каждого адреса
    if 'search_posts' in request.resolver_match.url_name:
        add_breadcrumb(breadcrumbs, 'search_posts', title='Страница поиска')
        
        
    elif 'tags' in request.resolver_match.url_name:
        tag_name = request.resolver_match.kwargs.get('tag_name')
        add_breadcrumb(breadcrumbs, 'tags', title='Теги')
        if tag_name:
            add_breadcrumb(breadcrumbs, 'app:tags', tag_name=tag_name, title=f'Тег: {tag_name}')
            
    elif 'tag' in request.resolver_match.url_name:
        tag_name = request.resolver_match.kwargs.get('tag_name')
        breadcrumbs.append({'url': reverse('tag'), 'title': 'Тег'})
        if tag_name:
            breadcrumbs.append({'url': reverse('tag', args=[tag_name]), 'title': f'Тег: {tag_name}'})
            
    elif 'contact' in request.resolver_match.url_name:
        add_breadcrumb(breadcrumbs, 'contact', title='Контакты')   
            
    elif 'manage_favorite' in request.resolver_match.url_name:
        post_id = request.resolver_match.kwargs.get('post_id')
        add_breadcrumb(breadcrumbs, 'manage_favorite', post_id, title='Избранное')
    elif 'userprofile' in request.resolver_match.url_name:
        add_breadcrumb(breadcrumbs, 'userprofile', title='Профиль')
    elif 'paid_view' in request.resolver_match.url_name:
        add_breadcrumb(breadcrumbs, 'paid_view', title='Страница оплаты')
        
    elif 'category_posts' in request.resolver_match.url_name:
        category_slug = request.resolver_match.kwargs.get('category_slug')
        category = Category.objects.get(slug=category_slug)  # Предполагается, что у вас есть поле slug в модели Category
        category_name = category.name
        add_breadcrumb(breadcrumbs, 'category_posts', category_slug, title=f'Рубрика: {category_name}')
        
        
    elif 'post_detail' in request.resolver_match.url_name:
        category_slug = request.resolver_match.kwargs.get('category_slug')
        slug = request.resolver_match.kwargs.get('slug')
        category = Category.objects.get(slug=category_slug)  # Предполагается, что у вас есть поле slug в модели Category
        category_name = category.name
        add_breadcrumb(breadcrumbs, 'category_posts', category_slug, title=f'Рубрика: {category_name}')
        add_breadcrumb(breadcrumbs, 'post_detail', category_slug, slug, title='Подробнее')

    elif 'ckeditor_upload' in request.resolver_match.url_name:
        add_breadcrumb(breadcrumbs, 'ckeditor_upload', title='Загрузка CKEditor')
    
    elif 'posts_by_year' in request.resolver_match.url_name:
        # year = request.resolver_match.kwargs.get('year')
        # month = request.resolver_match.kwargs.get('month')
        add_breadcrumb(breadcrumbs, 'posts_by_year', title=f'Архив')

    return {'menu': menu_items, 'breadcrumbs': breadcrumbs}