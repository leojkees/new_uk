from allauth.account.views import SignupView, LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import CustomSignupForm, CustomLoginForm, UserProfileForm, CustomChangePasswordForm, ProfileEditForm
from django.urls import reverse_lazy
from .models import Profile

# @login_required
# def profile(request):
#     user = request.user
#     context = {'user': user}
#     return render(request, 'profile.html', context)


class CustomSignupView(SignupView):
    form_class = CustomSignupForm
    template_name = 'signup.html'
    success_url = reverse_lazy('account_profile')  # Замените на ваш путь успешного входа

    def get_success_url(self):
        return self.success_url

    def form_valid(self, form):
        # Добавьте вашу проверку галочки здесь
        terms_accepted = form.cleaned_data.get("terms_accepted")
        
        if not terms_accepted:
            form.add_error("terms_accepted", "Вам нужно принять условия пользовательского соглашения.")
            return self.form_invalid(form)

        # Продолжаем с обработкой, если галочка принята
        return super().form_valid(form)

    
def custom_logout(request):
    return LogoutView.as_view(template_name='logout.html')(request)


class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'login-cs.html'


# def profile(request):
#     user = request.user
#     profile_form = UserProfileForm(instance=user)

#     if request.method == 'POST':
#         profile_form = UserProfileForm(request.POST, instance=user)
#         if profile_form.is_valid():
#             profile_form.save()

#     return render(request, 'profile.html', {'profile_form': profile_form})

class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomChangePasswordForm



@login_required
def profile(request):
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_instance = profile_form.save(commit=False)
            profile_instance.user = user  # Здесь устанавливаем пользователя
            profile_instance.save()
            return redirect('profile')

    profile_form = ProfileEditForm(instance=profile)
    context = {'user': user, 'profile': profile, 'profile_form': profile_form}
    return render(request, 'profile.html', context)

