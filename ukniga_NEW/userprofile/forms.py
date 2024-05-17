from django import forms
from allauth.account.forms import SignupForm, LoginForm, ChangePasswordForm
from django.contrib.auth.models import User
from .models import Profile
from captcha.fields import CaptchaField

class ProfileEditForm(forms.ModelForm):
    # Добавляем поле "Имя и Фамилия"
    full_name = forms.CharField(
        label="Имя и Фамилия",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True,
    )

    class Meta:
        model = Profile
        # Включаем поле "Имя и Фамилия" в список полей
        fields = ['full_name', 'position', 'phone', 'work_phone', 'bio', 'photo', 'cover_photo']
        widgets = {
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'work_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'cover_photo': forms.FileInput(attrs={'class': 'form-control'}),
        }


class CustomSignupForm(SignupForm):
    full_name = forms.CharField(
        label="Имя и фамилия",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg rounded-0', 'placeholder': 'Введите ваше имя и фамилию'}),
        required=True,
    )

    terms_accepted = forms.BooleanField(
        label="Я принимаю условия пользовательского соглашения",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input me-2'}),
        required=True,
    )

    captcha = CaptchaField(label="Введите код с картинки")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Обновляем виджет username
        self.fields['username'].widget.attrs.update({
            'class': 'form-control form-control-lg rounded-0',
            'placeholder': 'Придумайте логин'
        })

        # Добавляем классы и placeholder к полям full_name
        self.fields['full_name'].widget.attrs.update({
            'class': 'form-control form-control-lg rounded-0',
            'placeholder': 'Введите ваше имя и фамилию'
        })

        # Добавляем глазик для просмотра пароля при вводе
        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg rounded-0',
            'placeholder': 'Придумайте пароль',
            'render_value': True  # Добавляем атрибут render_value для возможности отображения пароля
        })
        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg rounded-0',
            'placeholder': 'Повторите пароль',
            'render_value': True  # Добавляем атрибут render_value для возможности отображения пароля
        })

        # Добавляем классы к другим полям формы
        for field_name in ['email', 'password1', 'password2']:
            self.fields[field_name].widget.attrs.update({'class': 'form-control form-control-lg rounded-0'})

        # Обновляем виджет для капчи
        self.fields['captcha'].widget.attrs.update({
            'class': 'form-control form-control-lg rounded-0',
            'placeholder': 'Введите код с картинки'
        })

    def clean(self):
        cleaned_data = super().clean()
        terms_accepted = cleaned_data.get("terms_accepted")

        if not terms_accepted:
            raise forms.ValidationError("Вам нужно принять условия пользовательского соглашения.")
        
        # Разбиение значения из одного поля на имя и фамилию
        full_name = cleaned_data.get("full_name")
        if full_name:
            names = full_name.split(maxsplit=1)
            if len(names) == 1:
                cleaned_data['first_name'] = names[0]
                cleaned_data['last_name'] = ''
            elif len(names) == 2:
                cleaned_data['first_name'] = names[0]
                cleaned_data['last_name'] = names[1]

        return cleaned_data


        
        
class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)

        # Применяем классы к виджетам полей формы
        for field_name, field in self.fields.items():
            current_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f'{current_classes} form-control form-control-lg rounded-0'

            # Установка placeholders для каждого поля
            if field_name == 'login':
                field.widget.attrs['placeholder'] = 'Введите логин'
            elif field_name == 'password':
                field.widget.attrs['placeholder'] = 'Введите пароль'

        # Опционально, вы также можете добавить метки к полям
        self.fields['login'].label = 'Логин пользователя для входа на сайт'
        self.fields['password'].label = 'Пароль'



class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

class CustomChangePasswordForm(ChangePasswordForm):
    pass