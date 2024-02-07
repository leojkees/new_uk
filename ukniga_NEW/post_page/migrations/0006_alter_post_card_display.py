# Generated by Django 4.2.7 on 2024-02-06 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post_page', '0005_post_card_display'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='card_display',
            field=models.CharField(choices=[('default', 'Фото + Заголовок'), ('fullscreen', 'Фото на всю ширину с оверфлоу + Заголовок поверх фото'), ('NoFoto', 'Без фото')], default='default', max_length=20, verbose_name='Вид карточки'),
        ),
    ]