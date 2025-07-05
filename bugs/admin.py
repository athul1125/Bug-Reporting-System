from django.contrib import admin
from .models import Bug

@admin.register(Bug)
class BugAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_by', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at')
    search_fields = ('created_by', 'status', 'fixed_by', 'info')