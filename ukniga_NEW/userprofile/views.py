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




@login_required  # Проверка, что пользователь аутентифицирован, прежде чем доступ к этой функции
def profile(request):
    user = request.user  # Получаем текущего пользователя из запроса
    try:
        profile = Profile.objects.get(user=user)  # Пытаемся получить профиль пользователя из базы данных
    except Profile.DoesNotExist:  # Если профиль не существует, устанавливаем его значение None
        profile = None

    if request.method == 'POST':  # Проверяем, был ли запрос методом POST
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=profile)  # Создаем форму редактирования профиля с данными из запроса
        if profile_form.is_valid():  # Проверяем валидность данных формы
            profile_form.save()  # Сохраняем данные профиля, если форма валидна
            return redirect('profile')  # Перенаправляем пользователя на страницу профиля после успешного сохранения

    profile_form = ProfileEditForm(instance=profile)  # Создаем форму редактирования профиля с существующими данными профиля
    context = {'user': user, 'profile': profile, 'profile_form': profile_form}  # Создаем контекст для передачи данных в шаблон
    return render(request, 'profile.html', context)  # Отображаем страницу профиля с переданным контекстом

