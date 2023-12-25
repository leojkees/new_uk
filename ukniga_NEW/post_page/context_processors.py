from django.urls import reverse
from .models import Category


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