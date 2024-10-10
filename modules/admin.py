from django.contrib import admin
from .models import Module, Assessment

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'code', 'recommended_prerequisites', 'term', 
        'lecturer', 'assessments', 'category', 'programming'
    )
    search_fields = ('name', 'code', 'lecturer')
    list_filter = ('term', 'lecturer')

@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = (
        'module_name', 'coursework_name', 'start_date', 'end_date', 'value', 'submit_work_to'
    )
    search_fields = ('module_name', 'coursework_name')
    list_filter = ('module_name', 'start_date', 'end_date')

# @admin.register(Keyword)
# class KeywordAdmin(admin.ModelAdmin):
#     list_display = ('big_topic', 'topic_content', 'keywords', 'examinable')
#     search_fields = ('big_topic', 'topic_content', 'keywords')
#     list_filter = ('examinable',)

# admin.site.get_urls = get_urls