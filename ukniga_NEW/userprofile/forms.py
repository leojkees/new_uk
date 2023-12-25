from django import forms
from allauth.account.forms import SignupForm, LoginForm, ChangePasswordForm
from django.contrib.auth.models import User





# class CustomSignupForm(SignupForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         # Добавляем классы к полям формы
#         for field_name in ['email', 'password1', 'password2', 'username']:  # изменено на 'username'
#             self.fields[field_name].widget.attrs.update({'class': 'form-control form-control-lg'})

#     # Опционально, вы также можете добавить метки к полям
#     def setup(self, request, user):
#         super().setup(request, user)
#         self.fields['email'].label = 'Your Email'
#         self.fields['password1'].label = 'Password'
#         self.fields['password2'].label = 'Repeat your password'
#         self.fields['username'].label = 'Your Name'

class CustomSignupForm(SignupForm):
    terms_accepted = forms.BooleanField(
        label="I agree all statements in Terms of service",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input me-2'}),
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Добавляем классы к полям формы
        for field_name in ['email', 'password1', 'password2', 'username']:
            self.fields[field_name].widget.attrs.update({'class': 'form-control form-control-lg'})

        # Опционально, вы также можете добавить метки к полям
        self.fields['email'].label = 'Your Email'
        self.fields['password1'].label = 'Password'
        self.fields['password2'].label = 'Repeat your password'
        self.fields['username'].label = 'Your Name'

    def clean(self):
        cleaned_data = super().clean()
        terms_accepted = cleaned_data.get("terms_accepted")

        if not terms_accepted:
            raise forms.ValidationError("You must agree to the terms of service.")
        
        
class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)

        # Применяем классы к виджетам полей формы
        for field_name, field in self.fields.items():
            current_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f'{current_classes} form-control form-control-lg'

        # Опционально, вы также можете добавить метки к полям
        self.fields['login'].label = 'Username'
        self.fields['password'].label = 'Password'


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

class CustomChangePasswordForm(ChangePasswordForm):
    pass