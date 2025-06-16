from django import template
from django.urls import reverse, resolve, NoReverseMatch, Resolver404
from ..models import MenuItem
from collections import defaultdict

register = template.Library()

class MenuBuilder:
    """Класс для построения и отрисовки древовидного меню"""
    
    def __init__(self, menu_name, current_path):
        self.menu_name = menu_name
        self.current_path = current_path
        self.menu_items = []
        self.active_item = None
        self.expanded_items = set()
        self._load_menu_items()
    
    def _load_menu_items(self):
        items = MenuItem.objects.filter(menu_name=self.menu_name).order_by('order', 'name')
        children_map = defaultdict(list)
        id_to_item = {}
        
        for item in items:
            id_to_item[item.id] = item
            parent_id = item.parent_id if item.parent_id else 0
            children_map[parent_id].append(item)
        
        self.menu_items = children_map.get(0, [])
        for item in items:
            item.children = children_map.get(item.id, [])
        
        self._find_active_item(items)
        self._mark_expanded_items()
    
    def _find_active_item(self, items):
        for item in items:
            try:
                item_url = item.get_absolute_url()
                if item_url == self.current_path:
                    self.active_item = item
                    return
            except (NoReverseMatch, Resolver404):
                continue
    
    def _mark_expanded_items(self):
        if not self.active_item:
            return
        item = self.active_item
        while item:
            self.expanded_items.add(item.id)
            item = item.parent
    
    def render_menu(self):
        if not self.menu_items:
            return ""
        return self._render_items(self.menu_items)
    
    def _render_items(self, items):
        html = '<ul>'
        for item in items:
            classes = []
            if item == self.active_item:
                classes.append('active')
            if item.id in self.expanded_items:
                classes.append('expanded')
            
            class_attr = f' class="{" ".join(classes)}"' if classes else ""
            
            html += f'<li{class_attr}>'
            html += f'<a href="{item.get_absolute_url()}">{item.name}</a>'
            
            if item.children and item.id in self.expanded_items:
                html += self._render_items(item.children)
            
            html += '</li>'
        html += '</ul>'
        return html

@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    current_path = request.path
    menu_builder = MenuBuilder(menu_name, current_path)
    return menu_builder.render_menu()