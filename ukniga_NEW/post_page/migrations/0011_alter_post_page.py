# Generated by Django 4.2.7 on 2024-02-28 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post_page', '0010_post_page'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='page',
            field=models.IntegerField(blank=True, default=None, null=True, verbose_name='Номер страницы в журнале'),
        ),
    ]