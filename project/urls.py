from django.contrib import admin
from django.urls import path
from menu.views import index, about, contacts

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='home'),
    path('about/', about, name='about'),
    path('contacts/', contacts, name='contacts'),
]