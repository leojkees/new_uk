"""ukniga_NEW URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings #импортируем настройки конфига
from django.conf.urls.static import static
from ckeditor_uploader import views as ckeditor_uploader_views
from filebrowser.sites import site


urlpatterns = [
        
    path('ckeditor/', include('ckeditor_uploader.urls')), #добавляем путь к ckeditor
    path('admin/filebrowser/', site.urls),
    path('jet/', include('jet.urls', 'jet')),  # Django JET URLS
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')), #добавляем путь к allauth
    path('', include('userprofile.urls')),
    path('', include('post_page.urls')), #include принимает набор маршрутов из файла блог пэйдж\
    path('', include('slider.urls')), #include принимает набор маршрутов из файла блог пэйдж\
    path('tinymce/', include('tinymce.urls')),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #дает доступ к медиа в режиме дебагинга