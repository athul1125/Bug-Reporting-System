from django.contrib import admin
from .models import *

@admin.register(Sprint)
class SprintAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)
