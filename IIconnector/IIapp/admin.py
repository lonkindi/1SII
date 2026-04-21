from django.contrib import admin
from IIapp.models import Organizations, FOT, AI_promts, AI_requests, Http1S_requests, Salary_AI


@admin.register(Organizations)
class OrganizationsAdmin(admin.ModelAdmin):    
    list_display = ('id', 'name', 'region', 'inn')
    list_display_links = ('id', 'name', 'region', 'inn')


@admin.register(FOT)
class FOTAdmin(admin.ModelAdmin):       
    list_display = ('id', 'organizations', 'month', 'year', 'amount', 'employees')
    list_display_links = ('id', 'organizations', 'month', 'year', 'amount', 'employees')


@admin.register(AI_promts)
class AI_promtsAdmin(admin.ModelAdmin):
    list_display = ('id', 'organizations', 'name', 'template')
    list_display_links = ('id', 'organizations', 'name',)


@admin.register(AI_requests)
class AI_requestsAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_request', 'organizations', 'promt_name', 'response', 'note')
    list_display_links = ('id', 'date_request', 'promt_name', 'organizations')


@admin.register(Http1S_requests)
class Http1S_requestsAdmin(admin.ModelAdmin):
    list_display = ('id', 'organizations', 'name', 'request')
    list_display_links = ('id', 'organizations', 'name')
    

@admin.register(Salary_AI)
class Salary_AIAdmin(admin.ModelAdmin):
    list_display = ('id', 'organizations', 'month', 'year', 'salary')
    list_display_links = ('id', 'organizations', 'month', 'year', 'salary')
