from django import forms
from .models import CorporateSubscription, Month, UserSubscription

class CorporateSubscriptionForm(forms.ModelForm):
    issues = forms.ModelMultipleChoiceField(
        queryset=Month.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Выберите нужные номера'
    )

    class Meta:
        model = CorporateSubscription
        fields = [
            'type', 'year', 'issues', 'amount', 'org_name', 'phone', 'inn',
            'kpp', 'real_address', 'corporate_address', 'email', 'contact'
        ]
        widgets = {
            'org_name': forms.Textarea(attrs={'rows': 1}),
            'real_address': forms.Textarea(attrs={'rows': 2}),
            'corporate_address': forms.Textarea(attrs={'rows': 2}),
        }
        labels = {
            'type': 'Варианты получения журнала',
            'year': 'Год',
            'amount': 'Количество экземпляров',
            'org_name': 'Наименование организации',
            'phone': 'Телефон',
            'inn': 'ИНН',
            'kpp': 'КПП',
            'real_address': 'Адрес фактический',
            'corporate_address': 'Адрес Юридический',
            'email': 'Электронный почтовый адрес e-mail',
            'contact': 'Контактное лицо',
        }


class UserSubscriptionForm(forms.ModelForm):
    issues = forms.ModelMultipleChoiceField(
        queryset=Month.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Выберите нужные номера'
    )

    class Meta:
        model = UserSubscription
        fields = ['type', 'year', 'issues', 'amount', 'contact', 'phone', 'real_address', 'email']
        labels = {
            'type': 'Варианты получения журнала',
            'year': 'Год',
            'amount': 'Количество экземпляров',
            'contact': 'ФИО',
            'phone': 'Телефон',
            'real_address': 'Адрес фактический',
            'email': 'Электронный почтовый адрес e-mail',
        }
        widgets = {
            'issues': forms.CheckboxSelectMultiple
        }