# Generated by Django 4.2.7 on 2024-03-04 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSubscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('paper', 'Бумажный вариант'), ('electronic', 'Электронный вариант')], max_length=10, verbose_name='Варианты получения журнала')),
                ('year', models.CharField(default='2024', max_length=4, verbose_name='Год')),
                ('amount', models.IntegerField(default=1, verbose_name='Количество экземпляров')),
                ('contact', models.CharField(max_length=50, verbose_name='ФИО')),
                ('phone', models.CharField(max_length=12, verbose_name='Телефон')),
                ('real_address', models.TextField(verbose_name='Адрес фактический')),
                ('email', models.EmailField(max_length=100, verbose_name='Электронный почтовый адрес e-mail')),
                ('issues', models.ManyToManyField(to='subscriptions.month', verbose_name='Выберите нужные номера')),
            ],
            options={
                'verbose_name': 'Подписка физ-лиц',
                'verbose_name_plural': 'Подписка физ-лиц',
            },
        ),
    ]
