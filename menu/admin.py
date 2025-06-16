from django.contrib import admin
from .models import MenuItem

class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'menu_name', 'parent', 'get_absolute_url', 'order')
    list_filter = ('menu_name',)
    search_fields = ('name', 'url', 'menu_name')
    list_editable = ('order',)
    fields = ('name', 'parent', 'menu_name', 'url', 'order')
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "parent":
            kwargs["queryset"] = MenuItem.objects.order_by('menu_name', 'name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(MenuItem, MenuItemAdmin)