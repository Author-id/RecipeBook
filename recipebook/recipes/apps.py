from django.apps import AppConfig
from django.utils.translation import gettext_lazy


class RecipesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "recipes"
    verbose_name = gettext_lazy("app__recipes")


__all__ = []
