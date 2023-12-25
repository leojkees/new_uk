from django.urls import path, include, re_path
from .views import PaidView, PostView, PostDetailView, PasswordView
from . import views
from ckeditor_uploader import views as ckeditor_uploader_views
from ckeditor_uploader.views import upload
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static
from ckeditor_uploader import views as ckeditor_views



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
    path('search/', views.search_posts, name='search_posts'),
    path('tags/', views.tag, name='tag'),
    path('tags/<str:tag_name>/', views.tags, name='tags'),
    path('manage_favorite/<int:post_id>/', views.manage_favorite, name='manage_favorite'),
    path('userprofile/', include('userprofile.urls')),
    path('paid/', PaidView.as_view(), name='paid_view'),
    path('', PostView.as_view(), name='home'), #Главная
    path('password/', PasswordView.as_view(), name='password_protected'),
    path('<slug:category_slug>/', views.category_posts, name='category_posts'),
    
    
    path('<slug:category_slug>/<slug:secondary_category_slug>/<slug:slug>/', PostDetailView.as_view(), name='post_detail_multiple_categories'),
    path('<slug:category_slug>/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)