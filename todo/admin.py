from django.contrib import admin
from .models import Todo, Control

# Register your models here.
class TodoAdmin(admin.ModelAdmin):

    list_display=('title','description','is_completed')
    search_fields =('title','description','is_completed')
    list_per_page=25

admin.site.register(Todo,TodoAdmin)

class ControlAdmin(admin.ModelAdmin):

    list_display=('title_order','description_order','complete_order', 'col_pri', 'complete_filter', 'user', 'id')
    search_fields =('title_order','description_order','complete_order', 'col_pri', 'complete_filter', 'user', 'id')

admin.site.register(Control,ControlAdmin)
# admin.site.register(Control)
