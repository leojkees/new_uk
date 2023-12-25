from django.db import models
from django.contrib.auth.models import User  # Импортируем модель User из django.contrib.auth.models






class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('post_page.Post', on_delete=models.CASCADE)
    date_subscribed = models.DateTimeField(auto_now_add=True)


