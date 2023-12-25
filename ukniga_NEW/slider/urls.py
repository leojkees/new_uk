from django.urls import path
from . import views

urlpatterns = [
    # Добавьте URL-путь для отображения слайдера с параметром slider_id
    path('<str:slider_id>/', views.slider_view, name='slider_view'),
]