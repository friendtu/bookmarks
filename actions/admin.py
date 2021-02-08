from django.contrib import admin
from .models import Action

# Register your models here.

@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    fields = ('user','verb','target','created')
    list_display=('created',)
    search_field=('verb',)
