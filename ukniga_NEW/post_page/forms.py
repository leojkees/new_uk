from django import forms
from .models import Post, Tag





    

class AddToFavoritesForm(forms.Form):
    post = forms.ModelChoiceField(queryset=Post.objects.all(), empty_label=None)

class PasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput())


class PostFilterForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['year', 'month', 'is_arhive']

    year = forms.ChoiceField(label='Год', choices=[], required=False)
    month = forms.ChoiceField(label='Месяц', choices=[], required=False)
    is_arhive = forms.BooleanField(label='Архив', required=False)

    def __init__(self, *args, **kwargs):
        super(PostFilterForm, self).__init__(*args, **kwargs)

        # Заполнение выбора года и месяца значениями из базы данных
        years = Post.objects.values_list('year', flat=True).distinct()
        months = Post.MONTH_CHOICES
        self.fields['year'].choices = [(year, year) for year in years]
        self.fields['month'].choices = months

        # Установка атрибутов для красивого отображения в HTML
        self.fields['year'].widget.attrs = {'class': 'form-select rounded-0'}
        self.fields['month'].widget.attrs = {'class': 'form-select rounded-0'}
        self.fields['is_arhive'].widget.attrs = {'class': 'form-check-input'}




class TagFilterForm(forms.Form):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.SelectMultiple,  # Используем SelectMultiple для выпадающего списка
        required=False,
        label='Теги'
    )
    full_match = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput,
        label='Полное вхождение'
    )


# class SlideForm(forms.ModelForm):
#     class Meta:
#         model = Slide
#         fields = ('image', 'caption', 'order')


# class YearMonthFilterForm(forms.Form):
#     year = forms.IntegerField(label='Год', required=False)
#     month = forms.IntegerField(label='Месяц', required=False)




# class PostFilterForm(forms.Form):
#     year = forms.ChoiceField(choices=DateModel.YEAR_CHOICES, required=False, label='Год')
#     month = forms.ChoiceField(choices=DateModel.MONTH_CHOICES, required=False, label='Месяц')
# class PostFilterForm(forms.Form):
#     year_choices = DateModel.objects.values_list('year', flat=True).distinct()
#     year = forms.ChoiceField(label='Год', choices=[(year, year) for year in year_choices])

#     month_choices = DateModel.objects.values_list('month', flat=True).distinct()
#     month = forms.ChoiceField(label='Месяц', choices=[(month, month) for month in month_choices])

#     def filter_posts(self):
#         year = self.cleaned_data.get('year')
#         month = self.cleaned_data.get('month')

#         # Фильтрация постов
#         posts = Post.objects.filter(year__year=year, month__month=month)

#         return posts




# class PostFilterForm(forms.Form):############################################################################
#     year_choices = Date.objects.values_list('year', flat=True).distinct()
#     year = forms.ChoiceField(label='Год', choices=[(year, year) for year in year_choices])

#     month_choices = Date.objects.values_list('month', flat=True).distinct()
#     month_dict = dict(Date.MONTH_CHOICES)  # Предполагается, что в вашей модели DateModel есть поле MONTH_CHOICES
#     month = forms.ChoiceField(label='Месяц', choices=[])

#     def __init__(self, *args, **kwargs):
#         super(PostFilterForm, self).__init__(*args, **kwargs)
#         self.fields['month'].choices = [(month, self.month_dict[month]) for month in self.month_choices]

#     def filter_posts(self):
#         year = self.cleaned_data.get('year')
#         month = self.cleaned_data.get('month')

#         # Фильтрация постов
#         posts = Post.objects.filter(year__year=year, month__month=month)

#         return posts
    