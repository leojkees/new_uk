from django.urls import path
from .views import subscription_company, subscription_user

urlpatterns = [
    path('podpiska2.html', subscription_company, name='subscribe'),
    path('podpiska.html', subscription_user, name='subscribe_user'),
]