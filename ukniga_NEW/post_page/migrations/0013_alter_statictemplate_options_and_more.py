# Generated by Django 4.2.7 on 2024-03-04 09:10

from django.db import migrations, models
import django_summernote.fields


class Migration(migrations.Migration):

    dependencies = [
        ('post_page', '0012_statictemplate_alter_post_month'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='statictemplate',
            options={'verbose_name': 'Статический шаблон', 'verbose_name_plural': 'Статические шаблоны'},
        ),
        migrations.AlterField(
            model_name='statictemplate',
            name='content',
            field=django_summernote.fields.SummernoteTextField(verbose_name='Содержимое'),
        ),
        migrations.AlterField(
            model_name='statictemplate',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='Название шаблона'),
        ),
    ]
