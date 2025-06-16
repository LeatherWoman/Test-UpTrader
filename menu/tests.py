from django.test import TestCase, RequestFactory
from django.urls import reverse
from .models import MenuItem
from .templatetags.menu_tags import MenuBuilder

class MenuTestCase(TestCase):
    def setUp(self):
        self.main_menu = MenuItem.objects.create(
            name="Главная",
            url="/",
            menu_name="main"
        )
        self.about_menu = MenuItem.objects.create(
            name="О нас",
            url="/about/",
            menu_name="main"
        )
        self.contacts_menu = MenuItem.objects.create(
            name="Контакты",
            url=reverse('contacts'),
            menu_name="main",
            parent=self.about_menu
        )
    
    def test_menu_creation(self):
        self.assertEqual(MenuItem.objects.count(), 3)
        self.assertEqual(self.contacts_menu.parent, self.about_menu)
    
    def test_menu_rendering(self):
        factory = RequestFactory()
        request = factory.get('/about/')
        builder = MenuBuilder("main", "/about/")
        html = builder.render_menu()
        self.assertIn("О нас", html)
        self.assertIn("Контакты", html)
        self.assertIn('class="expanded"', html)
        self.assertIn('class="active"', html)