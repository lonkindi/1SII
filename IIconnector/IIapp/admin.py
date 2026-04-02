from django.contrib import admin
from IIapp.models import Organizations, FOT, AI_promts, AI_requests, AI_templates, Http1S_requests


@admin.register(Organizations)
class OrganizationsAdmin(admin.ModelAdmin):
    # formfield_overrides = {models.ManyToManyField: {'widget': CheckboxSelectMultiple}, }
    # search_fields = ['Sname', 'phoneNumber']
    # date_hierarchy = 'date_oper'
    list_display = ('id', 'name', 'region', 'inn')
    # list_display_links = ('date_oper', 'phoneNumber', 'Sname', 'Name', 'Mname')
    # list_editable = ('Doctor',)


@admin.register(FOT)
class FOTAdmin(admin.ModelAdmin):   
    pass
    list_display = ('id', 'organizations', 'month', 'year', 'amount')
    
    
@admin.register(AI_promts)
class AI_promtsAdmin(admin.ModelAdmin):   
    pass


@admin.register(AI_requests)
class AI_requestsAdmin(admin.ModelAdmin):   
    pass


@admin.register(AI_templates)
class AI_templatesAdmin(admin.ModelAdmin):   
    pass


@admin.register(Http1S_requests)
class Http1S_requestsAdmin(admin.ModelAdmin):   
    list_display = ('id', 'organizations', 'name', 'request')
