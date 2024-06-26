# Generated by Django 4.2.7 on 2024-02-01 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slider', '0003_banner_place'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='banner',
            options={'verbose_name': 'Баннер', 'verbose_name_plural': 'Баннеры'},
        ),
        migrations.AlterField(
            model_name='banner',
            name='image_desktop',
            field=models.ImageField(upload_to='banners/', verbose_name='Изображение (десктоп), размер 940*150 px'),
        ),
        migrations.AlterField(
            model_name='banner',
            name='image_mobile',
            field=models.ImageField(upload_to='banners/', verbose_name='Изображение (мобильное), размер 360*80 px'),
        ),
        migrations.AlterField(
            model_name='banner',
            name='image_tablet',
            field=models.ImageField(upload_to='banners/', verbose_name='Изображение (планшет), размер 670*150 px'),
        ),
        migrations.AlterField(
            model_name='banner',
            name='place',
            field=models.CharField(blank=True, default='default', max_length=100, verbose_name='Место расположения баннера'),
        ),
        migrations.AlterField(
            model_name='banner',
            name='title',
            field=models.CharField(max_length=100, verbose_name='Заголовок'),
        ),
        migrations.AlterField(
            model_name='banner',
            name='url',
            field=models.URLField(verbose_name='URL'),
        ),
    ]
