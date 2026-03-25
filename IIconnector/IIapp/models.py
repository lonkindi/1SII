from django.db import models
import datetime


class AI_templates(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название шаблона ответа')
    template = models.JSONField(verbose_name='Шаблон ответа')
    
    class Meta:
        verbose_name = 'Шаблон ответа для ИИ'
        verbose_name_plural = "Список шаблонов ответа для ИИ"

        ordering = ('name',)

    def __str__(self):
        return self.name


class AI_promts(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название промта')
    template = models.TextField(verbose_name='Текст промта')
    
    class Meta:
        verbose_name = 'Промты для ИИ'
        verbose_name_plural = "Список промтов для ИИ"

        ordering = ('name',)

    def __str__(self):
        return self.name
    

class AI_requests(models.Model):    
    date_time = models.DateTimeField(verbose_name='Дата и время', default=datetime.datetime.today)
    requests = models.ForeignKey(AI_promts, verbose_name='Промт', on_delete=models.CASCADE)
    template = models.ForeignKey(AI_templates, verbose_name='Шаблон ответа ИИ', on_delete=models.CASCADE)
    response = models.JSONField(verbose_name='Ответ')
    note = models.CharField(max_length=256, verbose_name='Примечание')

    class Meta:
        verbose_name = 'Запрос к ИИ'
        verbose_name_plural = "Список запросов к ИИ"

        ordering = ('-date_time',)

    def __str__(self):
        return f'{self.date_time}_{self.requests}'
    
    

    