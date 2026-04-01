from django.db import models
import datetime


class Organizations(models.Model):
    """Организации"""
    name = models.CharField(max_length=256, unique=True, verbose_name='Наименование организации')
    region = models.CharField(max_length=256, verbose_name='Регион')
    inn = models.CharField(max_length=12, verbose_name='ИНН')
    desription = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = "Список организаций"
        
    def __str__(self):
        return self.name
        
        
class FOT(models.Model):
    """ФОТ"""
    organizations = models.ForeignKey(Organizations, verbose_name='Организация', on_delete=models.CASCADE)
    month = models.PositiveSmallIntegerField(verbose_name='Месяц')
    year = models.PositiveSmallIntegerField(verbose_name='Год')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма начислений')
    
    class Meta:
        verbose_name = 'ФОТ'
        verbose_name_plural = "Список ФОТ"


class Http1S_requests(models.Model):
    """Запросы к 1С"""
    organizations = models.ForeignKey(Organizations, verbose_name='Организация', on_delete=models.CASCADE)
    name = models.CharField(max_length=256,
                            verbose_name='Название запроса к 1С')
    request = models.URLField(verbose_name='Запрос к 1С')
    # response = models.TextField(verbose_name='Ответ 1С')

    class Meta:
        verbose_name = 'Запрос к 1С'
        verbose_name_plural = "Список запросов к 1С"

        ordering = ('name',)

    def __str__(self):
        return self.name+'_'+self.organizations.name


class AI_templates(models.Model):
    """Шаблоны ответов ИИ"""
    organizations = models.ForeignKey(Organizations, verbose_name='Организация', on_delete=models.CASCADE)
    name = models.CharField(max_length=256,
                            verbose_name='Название шаблона ответа')
    template = models.TextField(verbose_name='Шаблон ответа')

    class Meta:
        verbose_name = 'Шаблон ответа для ИИ'
        verbose_name_plural = "Список шаблонов ответа для ИИ"

        ordering = ('name',)

    def __str__(self):
        return self.name


class AI_promts(models.Model):
    """Промты для ИИ"""
    organizations = models.ForeignKey(Organizations, verbose_name='Организация', on_delete=models.CASCADE)
    name = models.CharField(max_length=256, verbose_name='Название промта')
    template = models.TextField(verbose_name='Текст промта')
    
    class Meta:
        verbose_name = 'Промты для ИИ'
        verbose_name_plural = "Список промтов для ИИ"

        ordering = ('name',)

    def __str__(self):
        return self.name+'_'+self.organizations.name
    

class AI_requests(models.Model):    
    date_time = models.DateTimeField(verbose_name='Дата и время',
                                     default=datetime.datetime.today)
    request = models.TextField(verbose_name='Промт')
    template = models.ForeignKey(AI_templates, verbose_name='Шаблон ответа ИИ',
                                 on_delete=models.CASCADE)
    response = models.TextField(verbose_name='Ответ')
    note = models.CharField(max_length=256, verbose_name='Примечание')

    class Meta:
        verbose_name = 'Запрос к ИИ'
        verbose_name_plural = "Список запросов к ИИ"

        ordering = ('-date_time',)

    def __str__(self):
        return f'{self.date_time}_{self.requests}'
