from django.db import models
import datetime
from users.models import CustomUser


class Organizations(models.Model):
    """Организации"""
    user = models.ForeignKey(CustomUser, related_name='org', on_delete=models.CASCADE)
    name = models.CharField(max_length=256, unique=True, verbose_name='Наименование организации')
    region = models.CharField(max_length=256, verbose_name='Регион')
    inn = models.CharField(max_length=12, verbose_name='ИНН')
    desription = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = "Организации"
        
    def __str__(self):
        return self.name
        
        
class FOT(models.Model):
    """ФОТ"""
    organizations = models.ForeignKey(Organizations, verbose_name='Организация', on_delete=models.CASCADE, related_name='fot_org')
    month = models.PositiveSmallIntegerField(verbose_name='Месяц')
    year = models.PositiveSmallIntegerField(verbose_name='Год')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма начислений')
    employees = models.PositiveSmallIntegerField(verbose_name='Количество сотрудников')
    
    class Meta:
        verbose_name = 'ФОТ'
        verbose_name_plural = "ФОТ"
        
        ordering = ('year', 'month')
        
    def __str__(self):
        return f'{self.organizations}_{self.month}_{self.year}_{self.amount}'


class Salary_AI(models.Model):
    """Зарплата по данным AI"""
    organizations = models.ForeignKey(Organizations, verbose_name='Организация', on_delete=models.CASCADE, related_name='salari_org')
    month = models.PositiveSmallIntegerField(verbose_name='Месяц')
    year = models.PositiveSmallIntegerField(verbose_name='Год')
    salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Средняя зарплата по региону за период')
    
    class Meta:
        verbose_name = 'Зарплата по данным AI'
        verbose_name_plural = "ЗП по данным AI"
        
        ordering = ('year', 'month')
        
    def __str__(self):
        return f'{self.organizations}_{self.month}_{self.year}_{self.salary}'


class Http1S_requests(models.Model):
    """Запросы к 1С"""
    organizations = models.ForeignKey(Organizations, verbose_name='Организация', on_delete=models.CASCADE)
    name = models.CharField(max_length=256, verbose_name='Название запроса к 1С')
    request = models.URLField(verbose_name='Запрос к 1С')
    # response = models.TextField(verbose_name='Ответ 1С')

    class Meta:
        verbose_name = 'Запрос к 1С'
        verbose_name_plural = "Запросы к 1С"

        ordering = ('name',)

    def __str__(self):
        return self.name+'_'+self.organizations.name


class AI_promts(models.Model):
    """Промты для ИИ"""
    organizations = models.ForeignKey(Organizations, verbose_name='Организация', on_delete=models.CASCADE)
    name = models.CharField(max_length=256, verbose_name='Название промта')
    template = models.TextField(verbose_name='Текст промта')
    
    class Meta:
        verbose_name = 'Промт для ИИ'
        verbose_name_plural = "Промты для ИИ"

        ordering = ('name',)

    def __str__(self):
        return self.name+'_'+self.organizations.name
    

class AI_requests(models.Model):
    """Запросы к ИИ"""
    organizations = models.ForeignKey(Organizations, verbose_name='Организация', on_delete=models.CASCADE)
    date_request = models.DateTimeField(verbose_name='Дата и время', default=datetime.datetime.today)
    promt_name = models.TextField(verbose_name='Название запроса')
    request = models.TextField(verbose_name='Текст запроса')
    response = models.TextField(verbose_name='Текст ответа')
    note = models.CharField(max_length=256, verbose_name='Примечание')

    class Meta:
        verbose_name = 'Запрос к ИИ'
        verbose_name_plural = "Запросы к ИИ"

        ordering = ('-date_request',)

    def __str__(self):
        return f'{self.date_request}_{self.organizations}_{self.promt_name}'
