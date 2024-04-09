from django.apps import AppConfig
from django.utils.translation import gettext_lazy


class FeedbackConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "feedback"
    verbose_name = gettext_lazy("app__feedback")


__all__: list[str] = []
