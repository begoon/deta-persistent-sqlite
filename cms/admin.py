from cms.models import Human
from django.contrib import admin


@admin.register(Human)
class HumanAdmin(admin.ModelAdmin):
    list_display = ('name', 'age')
    search_fields = list_display
    sortable_by = list_display
    list_per_page = 2
