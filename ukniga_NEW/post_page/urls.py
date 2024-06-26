from django.urls import path, include, re_path
from .views import PaidView, PostView, PostDetailView, PasswordView, post_preview
from . import views
from ckeditor_uploader import views as ckeditor_uploader_views
from ckeditor_uploader.views import upload
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static
from ckeditor_uploader import views as ckeditor_views
from django.conf.urls import handler404



urlpatterns = [
    #главная - если пустые кавычки, потом подключаем файл вью и обращаемся к классу
    path("ckeditor/upload/", upload, name="ckeditor_upload"),
    path("ckeditor/browse/", ckeditor_views.browse, name="ckeditor_browse"),
    path("ckeditor5/", include('django_ckeditor_5.urls'), name="ck_editor_5_upload_file"),
    path("contacts/", views.contact, name='contact'),
    path("forautors/", views.authors, name='forautors'),
    path("reklama/", views.reklama, name='reklama'),
    path("podpiska/", views.podpiska, name='podpiska'),
    path("about/", views.about, name='about'),
    path('arhive/', views.posts_by_year, name='posts_by_year'),
    path('arhiv/', views.images_by_year, name='arhiv-list'),
    path('search/', views.search_posts, name='search_posts'),
    path('tags/', views.tag, name='tag'),
    path('tags/<str:tag_name>/', views.tags, name='tags'),
    path('manage_favorite/<int:post_id>/', views.manage_favorite, name='manage_favorite'),
    path('userprofile/', include('userprofile.urls')),
    path('paid/', PaidView.as_view(), name='paid_view'),
    path('', PostView.as_view(), name='home'), #Главная
    path('password/', PasswordView.as_view(), name='password_protected'),
    re_path(r'^(?P<category_slug>[-\w]+)\.html$', views.category_posts, name='category_posts'),
    
    re_path(r'^(?P<category_slug>[-\w]+)/(?P<secondary_category_slug>[-\w]+)/(?P<slug>[-\w]+)\.html$', PostDetailView.as_view(), name='post_detail_multiple_categories'),
    re_path(r'^(?P<category_slug>[-\w]+)/(?P<slug>[-\w]+)\.html$', PostDetailView.as_view(), name='post_detail'),
    re_path(r'^(?P<category_slug>[-\w]+)/(?P<slug>[-\w]+)\.html/preview/$', post_preview, name='post-preview'),
    
]

handler404 = 'post_page.views.custom_404'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

