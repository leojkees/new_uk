# Generated by Django 4.2.7 on 2024-01-31 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slider', '0002_banner'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='place',
            field=models.CharField(blank=True, default='default', max_length=100),
        ),
    ]