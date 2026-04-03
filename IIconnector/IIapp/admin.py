from django.contrib import admin
from IIapp.models import Organizations, FOT, AI_promts, AI_requests, Http1S_requests


@admin.register(Organizations)
class OrganizationsAdmin(admin.ModelAdmin):    
    list_display = ('id', 'name', 'region', 'inn')    


@admin.register(FOT)
class FOTAdmin(admin.ModelAdmin):       
    list_display = ('id', 'organizations', 'month', 'year', 'amount', 'employees')
    
    
@admin.register(AI_promts)
class AI_promtsAdmin(admin.ModelAdmin):
    list_display = ('id', 'organizations', 'name', 'template')


@admin.register(AI_requests)
class AI_requestsAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_time', 'organizations', 'promt', 'response', 'note')


@admin.register(Http1S_requests)
class Http1S_requestsAdmin(admin.ModelAdmin):
    list_display = ('id', 'organizations', 'name', 'request')
