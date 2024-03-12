from django.db import models

class Month(models.Model):
    MONTH_CHOICES = [
        ('01/02', 'Январь-Февраль'),
        ('03', 'Март'),
        ('04', 'Апрель'),
        ('05', 'Май'),
        ('06', 'Июнь'),
        ('07/08', 'Июль-Август'),
        ('09', 'Сентябрь'),
        ('10', 'Октябрь'),
        ('11', 'Ноябрь'),
        ('12', 'Декабрь'),
    ]
    code = models.CharField(max_length=5, choices=MONTH_CHOICES, unique=True, verbose_name='Код месяца')
    name = models.CharField(max_length=20, verbose_name='Название месяца')

    def __str__(self):
        return self.name

class CorporateSubscription(models.Model):
    DELIVERY_CHOICES = (
        ('paper', 'Бумажный вариант'),
        ('electronic', 'Электронный вариант'),
    )

    type = models.CharField(max_length=10, choices=DELIVERY_CHOICES, verbose_name='Варианты получения журнала')
    year = models.CharField(max_length=4, default='2024', verbose_name='Год')
    issues = models.ManyToManyField(Month, verbose_name='Выберите нужные номера')
    amount = models.IntegerField(default=1, verbose_name='Количество экземпляров')
    org_name = models.TextField(verbose_name='Наименование организации')
    phone = models.CharField(max_length=12, verbose_name='Телефон')
    inn = models.CharField(max_length=12, verbose_name='ИНН')
    kpp = models.CharField(max_length=9, verbose_name='КПП')
    real_address = models.TextField(verbose_name='Адрес фактический')
    corporate_address = models.TextField(verbose_name='Адрес Юридический')
    email = models.EmailField(max_length=100, verbose_name='Электронный почтовый адрес e-mail')
    contact = models.CharField(max_length=50, verbose_name='Контактное лицо')

    def __str__(self):
        return self.org_name
    
    class Meta:
        verbose_name = "Подписка Юр-лиц"
        verbose_name_plural = "Подписка Юр-лиц"
    

class UserSubscription(models.Model):
    DELIVERY_CHOICES = (
        ('paper', 'Бумажный вариант'),
        ('electronic', 'Электронный вариант'),
    )

    type = models.CharField(max_length=10, choices=DELIVERY_CHOICES, verbose_name='Варианты получения журнала')
    year = models.CharField(max_length=4, default='2024', verbose_name='Год')
    issues = models.ManyToManyField(Month, verbose_name='Выберите нужные номера')
    amount = models.IntegerField(default=1, verbose_name='Количество экземпляров')
    contact = models.CharField(max_length=50, verbose_name='ФИО')
    phone = models.CharField(max_length=12, verbose_name='Телефон')
    real_address = models.TextField(verbose_name='Адрес фактический')
    email = models.EmailField(max_length=100, verbose_name='Электронный почтовый адрес e-mail')

    def __str__(self):
        return self.org_name
    
    class Meta:
        verbose_name = "Подписка физ-лиц"
        verbose_name_plural = "Подписка физ-лиц"

