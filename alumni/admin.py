from django.contrib import admin
from .models import Alumni

@admin.register(Alumni)
class AlumniAdmin(admin.ModelAdmin):
    list_display = ('name', 'job', 'degree')
    search_fields = ('name', 'job', 'degree')