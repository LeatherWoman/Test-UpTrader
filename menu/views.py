from django.shortcuts import render

def index(request):
    """Главная страница с демонстрацией меню"""
    return render(request, 'example.html', {'page_title': 'Главная страница'})

def about(request):
    """Страница 'О нас'"""
    return render(request, 'example.html', {'page_title': 'О нас'})

def contacts(request):
    """Страница 'Контакты'"""
    return render(request, 'example.html', {'page_title': 'Контакты'})