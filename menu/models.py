from django.db import models
from django.urls import reverse, NoReverseMatch
from django.core.exceptions import ValidationError

class MenuItem(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название пункта")
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name="Родительский пункт"
    )
    url = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Ссылка (URL)",
        help_text="Можно указать явный URL (например '/about/') или named URL (например 'about-page')"
    )
    menu_name = models.CharField(
        max_length=50,
        verbose_name="Название меню",
        help_text="Идентификатор меню для template tag"
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Порядок сортировки"
    )

    class Meta:
        verbose_name = "Пункт меню"
        verbose_name_plural = "Пункты меню"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def clean(self):
        # Валидация: предотвращение циклических ссылок
        if self.parent and self.parent == self:
            raise ValidationError("Пункт меню не может быть своим собственным родителем")
        
        # Проверка на создание циклов в дереве
        parent = self.parent
        while parent:
            if parent == self:
                raise ValidationError("Обнаружена циклическая ссылка в дереве меню")
            parent = parent.parent

    def get_absolute_url(self):
        """Возвращает корректный URL с учетом типа указанной ссылки"""
        if self.url:
            try:
                # Пробуем интерпретировать как named URL
                return reverse(self.url)
            except NoReverseMatch:
                # Если не named URL, используем как обычный URL
                return self.url
        return '#'