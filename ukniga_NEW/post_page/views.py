from django.shortcuts import render, get_object_or_404
from .models import Category, Post, FavoritePost, Tag
from django.views.generic.base import View
from django.shortcuts import redirect
from allauth.account.forms import LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from .context_processors import menu_and_breadcrumbs
from .forms import PostFilterForm, TagFilterForm, PasswordForm, YearForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.db.models import Case, When, IntegerField
from .models import StaticTemplate
from subscriptions.models import Month




menu = [{'title': "Главная", 'url_name': 'home'},
        {'title': "Подробнее", 'url_name': 'post_detail'},
        {'title': "Архив", 'url_name': 'arhive_posts'},
        
        ]

class PasswordView(View):
    def get(self, request):
        return render(request, 'password_form.html', {'form': PasswordForm()})

    def post(self, request):
        form = PasswordForm(request.POST)
        if form.is_valid() and form.cleaned_data['password'] == '0000':
            request.session['is_verified'] = True
            return redirect('home')
        return render(request, 'password_form.html', {'form': form})


class PostView(View):
    def get(self, request):
        # Проверка, ввел ли пользователь пароль
        if not request.session.get('is_verified', False):
            return redirect('password_protected')  # Перенаправление на страницу с вводом пароля
        
        current_time = timezone.now()

        try:
            template = StaticTemplate.objects.get(name='header.html')
            header_content = template.content
        except StaticTemplate.DoesNotExist:
            header_content = None

        excluded_categories = ['Новости', 'Новости партнеров', 'Анонсы']

        posts = Post.objects.filter(
            is_published=True,
            published_date__lte=current_time
        ).exclude(
            category__name__in=excluded_categories
        ).order_by('-published_date')

        # Paginator с 5 постами на странице
        paginator = Paginator(posts, 10)
        
        # Получите номер текущей страницы из параметра GET
        page = request.GET.get('page')

        # Получаем посты с категорией "Библиотеки"
        library_posts = Post.objects.filter(category__name='Библиотеки', is_published=True).order_by('-published_date')[:10]

        # Получаем посты с категорией "Новости"
        news_posts = Post.objects.filter(category__name='Новости', is_published=True).order_by('-published_date')[:10]

        # Получаем посты с категорией "Интервью"
        interview_posts = Post.objects.filter(category__name='Интервью', is_published=True).order_by('-published_date')[:10]

        # Получаем посты с категорией "Книжный рынок"
        bookrinok_posts = Post.objects.filter(category__name='Книжный рынок', is_published=True).order_by('-published_date')[:10]

        # Получаем посты с категорией "Острая тема"
        ostraya_posts = Post.objects.filter(category__name='Острая тема', is_published=True).order_by('-published_date')[:10]

        # Получаем посты с категорией "Выставки и конференции"
        vistavki_posts = Post.objects.filter(category__name='Выставки и конференции', is_published=True).order_by('-published_date')[:10]

        # Получаем посты с категорией "Новости партнеров"
        partners_posts = Post.objects.filter(category__name='Новости партнеров', is_published=True).order_by('-published_date')[:10]

        # Получаем посты с категорией "Наука и образование"
        nauka_posts = Post.objects.filter(category__name='Наука и образование', is_published=True).order_by('-published_date')[:10]

        # Получаем посты с категорией "Инновационные технологии"
        inovations_posts = Post.objects.filter(category__name='Инновационные технологии', is_published=True).order_by('-published_date')[:10]

        # Получаем посты с категорией "Креативный контекст"
        сreative_posts = Post.objects.filter(category__name='Креативный контекст', is_published=True).order_by('-published_date')[:10]

        # Получаем посты с категорией "Анонсы"
        anonced_posts = Post.objects.filter(category__name='Анонсы', is_published=True).order_by('-published_date')[:10]

        try:
            # Получите текущую страницу
            posts = paginator.page(page)
        except PageNotAnInteger:
            # Если параметр page не является целым числом, отобразите первую страницу
            posts = paginator.page(1)
        except EmptyPage:
            # Если параметр page превышает общее количество страниц, отобразите последнюю страницу
            posts = paginator.page(paginator.num_pages)

        for post in posts:
            post.content_preview = " ".join(post.text.split()[:15]) + "..." if len(post.text.split()) > 15 else post.text

        form = LoginForm()  # Создание экземпляра формы для входа

        context = {
            'post_list': posts,
            'library_posts': library_posts,
            'interview_posts': interview_posts,
            'bookrinok_posts': bookrinok_posts,
            'ostraya_posts': ostraya_posts,
            'news_posts': news_posts,
            'vistavki_posts': vistavki_posts,
            'partners_posts': partners_posts,
            'nauka_posts': nauka_posts,
            'inovations_posts': inovations_posts,
            'сreative_posts': сreative_posts,
            'anonced_posts': anonced_posts,
            'menu': menu,  # Ваша переменная menu
            'title': 'Главная страница',
            'form': form,  # Включение формы в контекст данных
            'header_content': header_content,
        }

        return render(request, 'arhiv/index.html', context=context)


    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            # Обработка данных из формы и выполнение необходимых действий
            # ...

            # Перенаправьте на PostDetailView или Paid в зависимости от значения subscribe
            if request.user.subscribe:
                return redirect('arhive/post_detail')  # Замените 'post_detail' на имя URL-шаблона для PostDetailView
            else:
                return redirect('paid_view')  # Замените 'paid_view' на имя URL-шаблона для Paid

        else:
            # Если форма недействительна, верните шаблон с ошибками
            posts = Post.objects.all()
            form = LoginForm()
            context = {
                'post_list': posts,
                'menu': menu,  # Ваша переменная menu
                'title': 'Главная страница',
                'form': form,  # Включение формы в контекст данных
            }
            return render(request, 'arhiv/post_list.html', context=context)

        

# class PostDetailView(View):
#     def get(self, request, category_slug, slug):
#         category = get_object_or_404(Category, slug=category_slug)
#         post = get_object_or_404(Post, category=category, slug=slug)
#         year = post.year
#         month = post.month

#         context = {
#             'category': category,
#             'post': post,
#             'year': year,
#             'month': month,
#         }

#         return render(request, 'arhiv/post_detail.html', context)
class PostDetailView(View):
    def get(self, request, category_slug, slug, secondary_category_slug=None):
        if secondary_category_slug:
            # Если указан второй параметр, значит у поста есть две категории
            category = get_object_or_404(Category, slug=secondary_category_slug)
        else:
            # Если второй параметр не указан, значит у поста одна категория
            category = get_object_or_404(Category, slug=category_slug)

        post = get_object_or_404(Post, category=category, slug=slug, is_published=True)
        year = post.year
        month = post.month

        context = {
            'category': category,
            'post': post,
            'year': year,
            'month': month,
        }

        return render(request, 'arhiv/post_detail.html', context)



class PaidView(View):
    def get(self, request):
        return render(request, 'arhiv/paid.html', {'menu': menu_and_breadcrumbs(request)['menu'], 'title': 'Платный контент'})




# def category_posts(request, category_slug):
#     category = get_object_or_404(Category, slug=category_slug)
#     posts = Post.objects.filter(category=category)
#     for post in posts:
#         post.content_preview = " ".join(post.text.split()[:30]) + "..." if len(post.text.split()) > 30 else post.text

#     return render(request, 'category_posts.html', {'category': category, 'posts': posts})
def category_posts(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    posts = Post.objects.filter(category=category, is_published=True).order_by('-published_date')

    #Paginator с 5 постами на странице
    paginator = Paginator(posts, 10)
    
    # Получите номер текущей страницы из параметра GET
    page = request.GET.get('page')

    try:
        # Получите текущую страницу
        posts = paginator.page(page)
    except PageNotAnInteger:
        # Если параметр page не является целым числом, отобразите первую страницу
        posts = paginator.page(1)
    except EmptyPage:
        # Если параметр page превышает общее количество страниц, отобразите последнюю страницу
        posts = paginator.page(paginator.num_pages)

    for post in posts:
        post.content_preview = " ".join(post.text.split()[:30]) + "..." if len(post.text.split()) > 30 else post.text

    return render(request, 'category_posts.html', {'category': category, 'posts': posts})


#Шаблон страницы для контакты
def contact(request):
    # Получаем объект шаблона из базы данных
    template = StaticTemplate.objects.get(name='contacts.html')

    # Передаем содержимое шаблона в контекст
    context = {
        'content': template.content
    }

    return render(request, 'contacts.html', context)

#Шаблон страницы для авторов
def authors(request):
    # Получаем объект шаблона из базы данных
    template = StaticTemplate.objects.get(name='forautors.html')

    # Передаем содержимое шаблона в контекст
    context = {
        'content': template.content
    }

    return render(request, 'forautors.html', context)


#Шаблон страницы рекламы
def reklama(request):
    # Получаем объект шаблона из базы данных
    template = StaticTemplate.objects.get(name='reklama.html')

    # Передаем содержимое шаблона в контекст
    context = {
        'content': template.content
    }

    return render(request, 'reklama.html', context)


def podpiska(request):
    months = Month.objects.all()
    context = {
        'months': months
    }

    return render(request, 'podpiska.html', context)


#Шаблон страницы о нас
def about(request):
    # Получаем объект шаблона из базы данных
    template = StaticTemplate.objects.get(name='about.html')

    # Передаем содержимое шаблона в контекст
    context = {
        'content': template.content
    }

    # Рендерим шаблон, передавая контекст
    return render(request, 'about.html', context)



# def posts_by_year(request):
#     if request.method == 'GET':
#         form = PostFilterForm(request.GET)

#         if form.is_valid():
#             year = form.cleaned_data['year']
#             month = form.cleaned_data['month']
#             is_arhive = form.cleaned_data['is_arhive']

#             # Фильтрация постов в соответствии с переданными параметрами
#             posts = Post.objects.all()

#             if year:
#                 posts = posts.filter(year=year)

#             if month:
#                 posts = posts.filter(month=month)

#             if is_arhive:
#                 posts = posts.filter(is_arhive=True)

#             # Добавляем первые 30 слов текста в атрибут content_preview для каждого поста
#             for post in posts:
#                 post.content_preview = " ".join(post.text.split()[:15]) + "..." if len(post.text.split()) > 15 else post.text

#             return render(request, 'arhive_page.html', {'posts': posts, 'form': form})

#     else:
#         form = PostFilterForm()

#     return render(request, 'arhive_page.html', {'form': form})
def posts_by_year(request):
    if request.method == 'GET':
        form = PostFilterForm(request.GET)

        if form.is_valid():
            year = form.cleaned_data['year']
            month = form.cleaned_data['month']
            is_arhive = form.cleaned_data['is_arhive']

            # Фильтрация постов в соответствии с переданными параметрами
            posts = Post.objects.all()

            if year:
                posts = posts.filter(year=year)

            if month:
                posts = posts.filter(month=month)

            # Фильтрация постов по is_arhive
            if is_arhive is True:
                posts = posts.filter(is_arhive=True)
            else:
                # Этот фильтр применяется, если is_arhive=False или is_arhive не указан
                posts = posts.filter(is_arhive=True)

            # Добавляем сортировку по published_date
            posts = posts.order_by('page')

            # Получение изображения для выбранного месяца
            image_for_month = None
            if month:
                # Перебор всех постов выбранного месяца для поиска первого изображения
                for post in posts.filter(month=month):
                    if post.image:
                        image_for_month = post.image
                        break

            # Добавляем первые 30 слов текста в атрибут content_preview для каждого поста
            for post in posts:
                post.content_preview = " ".join(post.text.split()[:15]) + "..." if len(post.text.split()) > 15 else post.text

            return render(request, 'arhive_page.html', {'posts': posts, 'form': form, 'image_for_month': image_for_month})

    else:
        form = PostFilterForm()

    return render(request, 'arhive_page.html', {'form': form})



# @login_required
# def manage_favorite(request, post_id):
#     post = get_object_or_404(Post, pk=post_id)

#     if request.method == 'POST':
#         if 'add_to_favorite' in request.POST:
#             existing_favorite = FavoritePost.objects.filter(user=request.user, post=post).first()
#             if existing_favorite:
#                 messages.error(request, 'Этот пост уже в избранном.')
#             else:
#                 FavoritePost.objects.create(user=request.user, post=post)
#                 messages.success(request, 'Пост добавлен в избранное.')
#         elif 'remove_from_favorite' in request.POST:
#             favorites_to_remove = FavoritePost.objects.filter(user=request.user, post=post)
#             favorites_to_remove.delete()

#     return redirect('account_profile')
@login_required
def manage_favorite(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    is_favorite = False

    if request.method == 'POST':
        if 'add_to_favorite' in request.POST:
            # Выполните код для добавления в избранное
            existing_favorite = FavoritePost.objects.filter(user=request.user, post=post).first()
            if existing_favorite:
                messages.error(request, 'Этот пост уже в избранном.')
            else:
                FavoritePost.objects.create(user=request.user, post=post)
                messages.success(request, 'Пост добавлен в избранное.')
                is_favorite = True
        elif 'remove_from_favorite' in request.POST:
            # Выполните код для удаления из избранного
            favorites_to_remove = FavoritePost.objects.filter(user=request.user, post=post)
            favorites_to_remove.delete()
    
    print(is_favorite)  # Убедитесь, что is_favorite обновляется правильно
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# def search_posts(request):
#     query = request.GET.get('q')  # Получение строки поиска из GET-параметра

#     if query:
#         # Используйте Q-объекты для поиска по разным полям
#         results = Post.objects.filter(
#             Q(title__icontains=query) |  # Поиск по заголовку (без учета регистра)
#             Q(description__icontains=query) |  # Поиск по подзаголовку (без учета регистра)
#             Q(text__icontains=query)  # Поиск по тексту записи (без учета регистра)
#         )
#     else:
#         results = []

#     context = {
#         'results': results,
#         'query': query
#     }
    
#     return render(request, 'search.html', context)
def search_posts(request):
    query = request.GET.get('q')  # Получение строки поиска из GET-параметра

    try:
        template = StaticTemplate.objects.get(name='header.html')
        header_content = template.content
    except StaticTemplate.DoesNotExist:
        header_content = None

    if query:
        # Используйте Q-объекты для поиска по разным полям
        posts = Post.objects.filter(
            Q(title__icontains=query) |  # Поиск по заголовку (без учета регистра)
            Q(description__icontains=query) |  # Поиск по подзаголовку (без учета регистра)
            Q(text__icontains=query)  # Поиск по тексту записи (без учета регистра)
        )
    else:
        posts = Post.objects.none()  # Возвращает пустой QuerySet, если запрос не задан

    # Добавляем первые 30 слов текста в атрибут content_preview для каждого поста
    for post in posts:
        post.content_preview = " ".join(post.text.split()[:30]) + "..." if len(post.text.split()) > 30 else post.text

    context = {
        'posts': posts,
        'query': query,
        'header_content': header_content,
    }
    
    return render(request, 'search.html', context)



def tag(request):
    form = TagFilterForm(request.GET)

    # Получаем все теги из базы данных
    tags = Tag.objects.all()

    # Если форма отправлена и валидна, обрабатываем фильтрацию
    if form.is_valid():
        selected_tags = form.cleaned_data['tags']
        full_match = form.cleaned_data['full_match']

        # Получаем посты в зависимости от выбранных тегов и условия полного вхождения
        if selected_tags:
            posts = Post.objects.all()

            for tag in selected_tags:
                posts = posts.filter(tags=tag)

            if full_match:
                # Аннотируем количество совпадающих тегов для каждого поста
                posts = posts.annotate(match_count=Count('tags'))

                # Фильтруем только посты, у которых количество совпадающих тегов равно выбранному количеству тегов
                posts = posts.filter(match_count=len(selected_tags))

        else:
            # Если теги не выбраны, показываем все посты
            posts = Post.objects.all()

    else:
        # Если форма не отправлена, показываем все посты
        posts = Post.objects.all()
        
    for post in posts:
        post.content_preview = " ".join(post.text.split()[:15]) + "..." if len(post.text.split()) > 15 else post.text

    context = {
        'form': form,
        'tags': tags,
        'posts': posts,
    }

    return render(request, 'tag.html', context)


    # form = PostFilterForm(request.GET)
    # posts = Post.objects.all()

    # if tag_name:
    #     # Если указан тег, фильтруем по нему
    #     posts = posts.filter(tags__name=tag_name)

    # if form.is_valid():
    #     tags = form.cleaned_data['tags']
    #     full_match = form.cleaned_data['full_match']

    #     if tags:
    #         if full_match:
    #             posts = posts.filter(tags__in=tags).distinct()
    #         else:
    #             posts = posts.filter(tags__in=tags)

    # for post in posts:
    #     post.content_preview = " ".join(post.text.split()[:15]) + "..." if len(post.text.split()) > 15 else post.text
    
    # context = {
    #     'form': form,
    #     'posts': posts,
    # }
def tags(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    posts = Post.objects.filter(tags=tag)

    form = TagFilterForm(request.GET)
    if form.is_valid():
        selected_tags = form.cleaned_data['tags']
        full_match = form.cleaned_data['full_match']

        if selected_tags:
            if full_match:
                posts = posts.filter(tags__in=selected_tags).distinct()
            else:
                posts = posts.filter(tags__in=selected_tags)

    for post in posts:
        post.content_preview = " ".join(post.text.split()[:15]) + "..." if len(post.text.split()) > 15 else post.text

    context = {'tag': tag, 'posts': posts, 'form': form}
    
    return render(request, 'tags.html', context)


# def images_by_year(request):
#     # Получаем уникальные изображения для каждого месяца
#     unique_images = (
#         Post.objects.values('month')
#                     .annotate(count=Count('image'))
#                     .filter(count__gt=0)
#     )

#     # Получаем список объектов Post для каждого месяца
#     posts_by_month = {}
#     for month_data in unique_images:
#         posts = Post.objects.filter(month=month_data['month'], image__isnull=False).order_by('?')[:1]
#         posts_by_month[month_data['month']] = posts

#     # Передаем данные в контекст представления
#     context = {'posts_by_month': posts_by_month}

#     return render(request, 'arhiv-list.html', context)
def images_by_year(request):
    form = YearForm(request.GET)
    
    if form.is_valid():
        selected_year = form.cleaned_data['year']
        
        # Определяем порядок сортировки для месяцев
        month_ordering = Case(
            When(month='Январь', then=1),
            When(month='Февраль', then=2),
            When(month='Январь/Февраль', then=3),
            When(month='Март', then=4),
            When(month='Апрель', then=5),
            When(month='Май', then=6),
            When(month='Июнь', then=7),
            When(month='Июль', then=8),
            When(month='Август', then=9),
            When(month='Июль/Август', then=10),
            When(month='Сентябрь', then=11),
            When(month='Октябрь', then=12),
            When(month='Ноябрь', then=13),
            When(month='Декабрь', then=14),           
            default=0, 
            output_field=IntegerField(),
        )

        unique_images = (
            Post.objects.filter(year=selected_year, is_arhive=True)
                        .values('month')
                        .annotate(count=Count('image'))
                        .filter(count__gt=0)
                        .order_by(month_ordering)  # Используем определенный порядок сортировки
        )
        
        posts_by_month = {}
        for month_data in unique_images:
            posts = Post.objects.filter(year=selected_year, 
                                        month=month_data['month'], 
                                        image__isnull=False,
                                        is_arhive=True).order_by('?')[:1]
            if posts.exists():  # Проверяем, есть ли посты с is_arhive=True
                posts_by_month[month_data['month']] = posts
        
        context = {'form': form, 'selected_year': selected_year, 'posts_by_month': posts_by_month}
        return render(request, 'arhiv-list.html', context)
    
    context = {'form': form}
    return render(request, 'arhiv-list.html', context)