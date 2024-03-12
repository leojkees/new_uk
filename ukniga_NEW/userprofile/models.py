from django.db import models
from django.contrib.auth.models import User
from post_page.models import Tag




#модель подписчика
class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('post_page.Post', on_delete=models.CASCADE)
    date_subscribed = models.DateTimeField(auto_now_add=True)


#модель пользователя
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    position = models.CharField(max_length=100, blank=True, verbose_name="Должность")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    work_phone = models.CharField(max_length=20, blank=True, verbose_name="Рабочий телефон")
    bio = models.TextField(blank=True, verbose_name="Биография")
    photo = models.ImageField(upload_to='profile_photos', blank=True, verbose_name="Фото")
    cover_photo = models.ImageField(upload_to='cover_photos', blank=True, verbose_name="Обложка")
    is_author = models.BooleanField('Автор', default=False)
    is_personal = models.BooleanField('Член ред.коллегии', default=False)
    tags = models.ManyToManyField(Tag, related_name='user_profiles', verbose_name="Теги")

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"


class UserTag(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'tag')
        verbose_name = "Авторский тег"
        verbose_name_plural = "Авторские теги"

    def __str__(self):
        return f"{self.user.username} - {self.tag.name}"