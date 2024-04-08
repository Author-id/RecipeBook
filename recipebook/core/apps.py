from django.apps import AppConfig
from django.utils.translation import gettext_lazy


class CoreConfig(AppConfig):
    name = "core"
    verbose_name = gettext_lazy("app__core")


__all__ = []
