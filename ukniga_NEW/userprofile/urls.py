from django.urls import path
from . import views
# from django.contrib.auth.views import LogoutView, LoginView
from .views import CustomSignupView, custom_logout, CustomLoginView, CustomPasswordChangeView, profile
from allauth.account.views import LogoutView

urlpatterns = [
    # path('logout/', LogoutView.as_view(), name='logout'),
    path('account/logout/', custom_logout, name='account_logout'),
    path('accounts/profile/', profile, name='profile'),
    # path('register/', CustomSignupView.as_view(), name='custom_signup'),
    path('login/', CustomLoginView.as_view(), name='custom-login'),
    path('accounts/profile/', views.profile, name='account_profile'),
    path('signup/', CustomSignupView.as_view(), name='custom_signup'),
    path('accounts/password/change/', CustomPasswordChangeView.as_view(), name='account_change_password'),
]