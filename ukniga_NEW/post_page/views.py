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
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.db.models import Case, When, IntegerField
from .models import StaticTemplate
from subscriptions.models import Month
from bs4 import BeautifulSoup
import re



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

        try:
            template = StaticTemplate.objects.get(name='header.html')
            header_content = template.content
        except StaticTemplate.DoesNotExist:
            header_content = None

        excluded_categories = ['Новости', 'Новости партнеров', 'Анонсы']

        posts = Post.objects.filter(
            is_published=True,
            is_featured=True  # Добавляем проверку на is_featured
        ).exclude(
            category__name__in=excluded_categories
        ).order_by('-published_date')
        # Paginator с 5 постами на странице
        paginator = Paginator(posts, 10)
        
        # Получите номер текущей страницы из параметра GET
        page = request.GET.get('page')

        # Получаем посты с категорией "Библиотеки"
        library_posts = Post.objects.filter(
            Q(category__name='Библиотечное дело') |
            Q(category__name='Формирование библиотечных фондов') |
            Q(category__name='Вузовские библиотеки') |
            Q(category__name='Библиотеки мира') |
            Q(category__name='Гений места') |
            Q(category__name='Абсолютно медиа'),
            is_published=True,
            is_featured=True
        ).order_by('-published_date')[:10]

        # Получаем посты с категорией "Новости"
        news_posts = Post.objects.filter(category__name='Новости', is_published=True, is_featured=True).order_by('-published_date')[:10]

        # Получаем посты с категорией "Интервью"
        interview_posts = Post.objects.filter(
            Q(category__name='Действующие лица') |
            Q(category__name='Персональный подход') |
            Q(category__name='Интервью'),
            is_published=True,
            is_featured=True
        ).order_by('-published_date')[:10]

        # Получаем посты с категорией "Книжный рынок"
        bookrinok_posts = Post.objects.filter(
            Q(category__name='Книжный рынок') |
            Q(category__name='Книгораспространение') |
            Q(category__name='Мир издательств') |
            Q(category__name='Зарубежный опыт'),
            is_published=True,
            is_featured=True
        ).order_by('-published_date')[:10]

        # Получаем посты с категорией "Острая тема"
        ostraya_posts = Post.objects.filter(category__name='Острая тема', is_published=True, is_featured=True).order_by('-published_date')[:10]

        # Получаем посты с категорией "Выставки и конференции"
        vistavki_posts = Post.objects.filter(category__name='Выставки и конференции', is_published=True, is_featured=True).order_by('-published_date')[:10]

        # Получаем посты с категорией "Новости партнеров"
        partners_posts = Post.objects.filter(category__name='Новости партнеров', is_published=True, is_featured=True).order_by('-published_date')[:10]

        # Получаем посты с категорией "Наука и образование"
        nauka_posts = Post.objects.filter(category__name='Наука и образование', is_published=True, is_featured=True).order_by('-published_date')[:10]

        # Получаем посты с категорией "Инновационные технологии"
        inovations_posts = Post.objects.filter(
            Q(category__name='Инновационные технологии') |
            Q(category__name='Технологии печати') |
            Q(category__name='Электронные библиотеки') |
            Q(category__name='Искусственный интеллект и нейросети') |
            Q(category__name='Книга+'),
            is_published=True,
            is_featured=True
        ).order_by('-published_date')[:10]

        # Получаем посты с категорией "Креативный контекст"
        сreative_posts = Post.objects.filter(category__name='Креативный контекст', is_published=True, is_featured=True).order_by('-published_date')[:10]

        # Получаем посты с категорией "Анонсы"
        anonced_posts = Post.objects.filter(category__name='Анонсы', is_published=True, is_featured=True).order_by('-published_date')[:10]

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
                'title': 'Главная страница',
                'form': form,  # Включение формы в контекст данных
            }
            return render(request, 'arhiv/post_list.html', context=context)

        

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
        # Получаем шаблон 'paid.html' из базы данных
        template = StaticTemplate.objects.get(name='paid.html')

        # Подготавливаем контекст для передачи в шаблон
        context = {
            'content': template.content
        }

        # Рендерим шаблон 'paid.html' с контекстом и дополнительными данными, такими как меню и заголовок
        return render(request, 'paid.html', context)



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
    form_type = request.GET.get('form')  # Получаем значение параметра 'form'

    # Определяем, какую форму показать на основе значения параметра
    if form_type == 'userForm':
        user_form_display = True
        corporate_form_display = False
    elif form_type == 'corporateForm':
        user_form_display = False
        corporate_form_display = True
    else:
        # Если параметр не указан или имеет некорректное значение, показываем обе формы
        user_form_display = False
        corporate_form_display = True

    context = {
        'months': months,
        'user_form_display': user_form_display,
        'corporate_form_display': corporate_form_display,
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
                posts = posts.filter(year=year, is_published=True)

            if month:
                posts = posts.filter(month=month, is_published=True)

            # Фильтрация постов по is_arhive
            if is_arhive is True:
                posts = posts.filter(is_arhive=True, is_published=True)
            else:
                # Этот фильтр применяется, если is_arhive=False или is_arhive не указан
                posts = posts.filter(is_arhive=True, is_published=True)

            # Добавляем сортировку по странице журнала
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



# Представление для управления избранными постами
@login_required  # Требует аутентификации пользователя
def manage_favorite(request, post_id):
    # Получаем объект поста или возвращаем 404, если пост не найден
    post = get_object_or_404(Post, pk=post_id)
    is_favorite = False  # Переменная для отслеживания статуса поста в избранном

    if request.method == 'POST':  # Если запрос - POST
        if 'add_to_favorite' in request.POST:  # Если пользователь хочет добавить пост в избранное
            existing_favorite = FavoritePost.objects.filter(user=request.user, post=post).first()  # Проверяем, есть ли уже пост в избранном у текущего пользователя
            if existing_favorite:  # Если пост уже в избранном
                messages.error(request, 'Этот пост уже в избранном.')  # Показываем сообщение об ошибке
            else:
                FavoritePost.objects.create(user=request.user, post=post)  # Добавляем пост в избранное для текущего пользователя
                messages.success(request, 'Пост добавлен в избранное.')  # Показываем сообщение об успешном добавлении
                is_favorite = True  # Устанавливаем статус поста в избранном как True
        elif 'remove_from_favorite' in request.POST:  # Если пользователь хочет удалить пост из избранного
            favorites_to_remove = FavoritePost.objects.filter(user=request.user, post=post)  # Находим записи об избранных постах для текущего пользователя и этого поста
            favorites_to_remove.delete()  # Удаляем все записи об избранных постах для текущего пользователя и этого поста

    # Перенаправляем пользователя на предыдущую страницу
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



####################################################################################################

# def clean_html(raw_html):
#     """
#     Очистка HTML тегов из текста
#     """
#     soup = BeautifulSoup(raw_html, "html.parser")
#     return soup.get_text()

# def create_snippets(text, query_words):
#     """
#     Создание сниппетов из текста с подсветкой найденных слов.
#     """
#     snippets = []
#     sentences = re.split(r'(?<=[.!?]) +', text)

#     # Проверка на целую фразу
#     query_phrase = ' '.join(query_words)
#     phrase_match = re.search(r'\b{}\b'.format(query_phrase), text, flags=re.IGNORECASE)
    
#     if phrase_match:
#         start_idx = max(0, phrase_match.start() - 50)
#         end_idx = min(len(text), phrase_match.end() + 50)
#         final_snippet = text[start_idx:end_idx]
#         for q_word in query_words:
#             final_snippet = re.sub(f'({q_word})', r'<mark>\1</mark>', final_snippet, flags=re.IGNORECASE)
#         return [f"<p>{final_snippet}</p>"]
    
#     # Если целая фраза не найдена, ищем отдельные слова
#     final_snippets = []
#     for word in query_words:
#         word_pattern = re.compile(r'\b{}\b'.format(re.escape(word)), re.IGNORECASE)
#         matches = word_pattern.finditer(text)
#         for match in matches:
#             start_idx = max(0, match.start() - 50)
#             end_idx = min(len(text), match.end() + 50)
#             snippet = text[start_idx:end_idx]
#             snippet = re.sub(f'({word})', r'<mark>\1</mark>', snippet, flags=re.IGNORECASE)
#             final_snippets.append(f"<p>{snippet}</p>")
#             if len(final_snippets) >= len(query_words):
#                 break
#         if len(final_snippets) >= len(query_words):
#             break

#     return final_snippets

# def search_posts(query):
#     """
#     Поиск по постам с учетом всех условий и создание сниппетов с подсветкой найденных слов.
#     """
#     query_words = [word for word in re.findall(r'\b\w{3,}\b', query) if len(word) > 2]
    
#     if not query_words:
#         return []

#     q_objects = Q()
#     for word in query_words:
#         q_objects &= (Q(title__icontains=word) | Q(text__icontains=word))

#     posts = Post.objects.filter(q_objects).prefetch_related('category')

#     exact_phrase_posts = []
#     partial_phrase_posts = []

#     query_phrase = ' '.join(query_words)
#     for post in posts:
#         text = clean_html(post.text)
#         title = post.title
#         content = f"{title} {text}"

#         # Проверка на целую фразу
#         if re.search(r'\b{}\b'.format(query_phrase), content, flags=re.IGNORECASE):
#             exact_phrase_posts.append(post)
#         else:
#             if all(word in content for word in query_words):
#                 partial_phrase_posts.append(post)

#     search_results = []
#     for post in exact_phrase_posts + partial_phrase_posts:
#         text = clean_html(post.text)
#         title = post.title
#         content = f"{title} {text}"
#         snippets = create_snippets(content, query_words)
#         categories = post.category.all()
#         search_results.append({'post': post, 'snippets': snippets, 'categories': categories})

#     return search_results

# def search_view(request):
#     query = request.GET.get('q', '')
#     search_results = search_posts(query)
#     context = {
#         'query': query,
#         'posts_with_snippets': search_results,
#     }
#     return render(request, 'search.html', context)
def clean_html(raw_html):
    """
    Очистка HTML тегов из текста
    """
    soup = BeautifulSoup(raw_html, "html.parser")
    return soup.get_text()

def create_snippets(text, query_words):
    """
    Создание сниппетов из текста с подсветкой найденных слов.
    """
    snippets = []
    paragraphs = text.split('\n')

    # Проверка на целую фразу
    query_phrase = ' '.join(query_words)
    phrase_pattern = re.compile(r'\b{}\b'.format(re.escape(query_phrase)), re.IGNORECASE)
    
    for paragraph in paragraphs:
        if phrase_pattern.search(paragraph):
            snippet = paragraph
            for q_word in query_words:
                snippet = re.sub(f'({q_word})', r'<mark>\1</mark>', snippet, flags=re.IGNORECASE)
            return [f"<p>{snippet}</p>"]

    # Если целая фраза не найдена, ищем отдельные слова
    final_snippets = []
    for paragraph in paragraphs:
        for word in query_words:
            word_pattern = re.compile(r'\b{}\b'.format(re.escape(word)), re.IGNORECASE)
            if word_pattern.search(paragraph):
                snippet = paragraph
                snippet = re.sub(f'({word})', r'<mark>\1</mark>', snippet, flags=re.IGNORECASE)
                final_snippets.append(f"<p>{snippet}</p>")
                if len(final_snippets) >= len(query_words):
                    break
        if len(final_snippets) >= len(query_words):
            break

    return final_snippets

# def search_posts(query):
#     """
#     Поиск по постам с учетом всех условий и создание сниппетов с подсветкой найденных слов.
#     """
#     query_words = [word for word in re.findall(r'\b\w{3,}\b', query) if len(word) > 2]
    
#     if not query_words:
#         return []

#     q_objects = Q()
#     for word in query_words:
#         q_objects &= (Q(title__icontains=word) | Q(text__icontains=word))

#     posts = Post.objects.filter(q_objects).prefetch_related('category').order_by('-published_date')

#     exact_phrase_posts = []
#     partial_phrase_posts = []

#     query_phrase = ' '.join(query_words)
#     phrase_pattern = re.compile(r'\b{}\b'.format(re.escape(query_phrase)), re.IGNORECASE)
    
#     for post in posts:
#         text = clean_html(post.text)
#         title = post.title
#         content = f"{title} {text}"

#         if phrase_pattern.search(content):
#             exact_phrase_posts.append(post)
#         elif all(re.search(r'\b{}\b'.format(re.escape(word)), content, re.IGNORECASE) for word in query_words):
#             partial_phrase_posts.append(post)

#     search_results = []
#     for post in exact_phrase_posts + partial_phrase_posts:
#         text = clean_html(post.text)
#         title = post.title
#         content = f"{title} {text}"
#         snippets = create_snippets(content, query_words)
#         categories = post.category.all()
#         search_results.append({'post': post, 'snippets': snippets, 'categories': categories})

#     return search_results
def search_posts(query):
    """
    Поиск по постам с учетом всех условий и создание сниппетов с подсветкой найденных слов.
    """
    query_words = [word for word in re.findall(r'\b\w{3,}\b', query) if len(word) > 2]
    
    if not query_words:
        return []

    q_objects = Q()
    for word in query_words:
        q_objects &= (Q(title__icontains=word) | Q(text__icontains=word))

    posts = Post.objects.filter(q_objects).prefetch_related('category').order_by('-published_date')

    search_results = []
    query_phrase = ' '.join(query_words)
    phrase_pattern = re.compile(r'\b{}\b'.format(re.escape(query_phrase)), re.IGNORECASE)

    for post in posts:
        text = clean_html(post.text)
        title = post.title
        content = f"{title} {text}"
        
        if phrase_pattern.search(content) or all(re.search(r'\b{}\b'.format(re.escape(word)), content, re.IGNORECASE) for word in query_words):
            snippets = create_snippets(content, query_words)
            categories = post.category.all()
            search_results.append({'post': post, 'snippets': snippets, 'categories': categories})

    return search_results

def search_view(request):
    query = request.GET.get('q', '')
    search_results = search_posts(query)
    
    # Пагинация
    page = request.GET.get('page', 1)
    paginator = Paginator(search_results, 10)  # По 10 результатов на странице

    try:
        paginated_results = paginator.page(page)
    except PageNotAnInteger:
        paginated_results = paginator.page(1)
    except EmptyPage:
        paginated_results = paginator.page(paginator.num_pages)
    
    try:
        template = StaticTemplate.objects.get(name='header.html')
        header_content = template.content
    except StaticTemplate.DoesNotExist:
        header_content = None
        
    context = {
        'query': query,
        'posts_with_snippets': paginated_results,
        'header_content': header_content,
    }
    return render(request, 'search.html', context)

#################################################################################################################################




# Функция для отображения всех постов с возможностью фильтрации по тегам
def tag(request):
    # Получаем данные из запроса
    form = TagFilterForm(request.GET)
    
    # Получаем все существующие теги
    tags = Tag.objects.all()

    if form.is_valid():  # Если форма валидна
        selected_tags = form.cleaned_data['tags']  # Выбранные теги из формы
        full_match = form.cleaned_data['full_match']  # Полное совпадение тегов

        if selected_tags:  # Если выбраны какие-то теги
            # Фильтруем только опубликованные посты
            posts = Post.objects.filter(is_published=True)

            for tag in selected_tags:  # Для каждого выбранного тега
                posts = posts.filter(tags=tag)  # Фильтруем посты по этому тегу

            if full_match:  # Если выбрано полное совпадение
                posts = posts.annotate(match_count=Count('tags'))  # Подсчитываем количество тегов у каждого поста
                posts = posts.filter(match_count=len(selected_tags))  # Фильтруем только посты с количеством тегов, равным количеству выбранных тегов
        else:
            # Если не выбраны теги, отображаем все опубликованные посты
            posts = Post.objects.filter(is_published=True)
    else:
        # Если форма не валидна, отображаем все опубликованные посты
        posts = Post.objects.filter(is_published=True)

    # Для каждого поста создаем краткий предварительный просмотр содержимого
    for post in posts:
        post.content_preview = " ".join(post.text.split()[:15]) + "..." if len(post.text.split()) > 15 else post.text

    # Формируем контекст для передачи в шаблон
    context = {
        'form': form,  # Форма фильтрации тегов
        'tags': tags,  # Список всех тегов
        'posts': posts,  # Список постов после применения фильтрации
    }

    # Отображаем шаблон tag.html с переданным контекстом
    return render(request, 'tag.html', context)



#функция отображения конкретного тега
def tags(request, tag_name):
    # Получаем объект тега или возвращаем 404, если такового нет
    tag = get_object_or_404(Tag, name=tag_name)
    
    # Основной запрос на посты, уже включающий проверку на публикацию и фильтрацию по тегу
    posts = Post.objects.filter(tags=tag, is_published=True).order_by('-published_date')

    # Обработка формы фильтрации по тегам
    form = TagFilterForm(request.GET)
    if form.is_valid():
        selected_tags = form.cleaned_data['tags']
        full_match = form.cleaned_data['full_match']

        if selected_tags:
            # Фильтрация постов по дополнительным тегам
            posts = posts.filter(tags__in=selected_tags).distinct()

            if full_match:
                # Если требуется полное совпадение, считаем количество тегов
                posts = posts.annotate(match_count=Count('tags'))
                posts = posts.filter(match_count=len(selected_tags))

    # Генерация предпросмотра контента поста
    for post in posts:
        post.content_preview = " ".join(post.text.split()[:15]) + "..." if len(post.text.split()) > 15 else post.text

    context = {'tag': tag, 'posts': posts, 'form': form}
    
    return render(request, 'tags.html', context)



# Представление для отображения изображений по годам
def images_by_year(request):
    form = YearForm(request.GET)  # Получаем форму с данными о годе из параметров GET запроса
    
    if form.is_valid():  # Если форма валидна
        selected_year = form.cleaned_data['year']  # Получаем выбранный год из формы

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

        # Получаем уникальные изображения по месяцам за выбранный год
        unique_images = (
            Post.objects.filter(year=selected_year, is_arhive=True)  # Фильтруем посты по году и статусу архива
                        .values('month')  # Выбираем только месяцы
                        .annotate(count=Count('image'))  # Подсчитываем количество изображений для каждого месяца
                        .filter(count__gt=0)  # Фильтруем только месяцы с изображениями
                        .order_by(month_ordering)  # Сортируем месяцы в определенном порядке
        )
        
        # Собираем по одному случайному посту с изображением для каждого месяца
        posts_by_month = {}
        for month_data in unique_images:
            posts = Post.objects.filter(year=selected_year,  # Фильтруем посты по году
                                        month=month_data['month'],  # Фильтруем по месяцу
                                        image__isnull=False,  # Фильтруем только посты с изображениями
                                        is_arhive=True).order_by('?')[:1]  # Случайно выбираем один пост
            if posts.exists():  # Проверяем, есть ли посты с is_archive=True
                posts_by_month[month_data['month']] = posts
        
        context = {'form': form, 'selected_year': selected_year, 'posts_by_month': posts_by_month}  # Формируем контекст
        return render(request, 'arhiv-list.html', context)  # Отображаем шаблон archive-list.html с переданным контекстом
    
    # Если форма не валидна или не была отправлена, отображаем форму без данных о годе
    context = {'form': form}
    return render(request, 'arhiv-list.html', context)



def post_preview(request, category_slug, slug):
    post = get_object_or_404(Post, slug=slug, category__slug=category_slug)
    if post.is_published or request.user.is_staff or request.user == post.author:
        return render(request, "posts/post_detail.html", {"post": post})
    else:
        raise Http404("You do not have permission to view this preview.")
    
def custom_404(request, exception):
    return render(request, '404.html', status=404)