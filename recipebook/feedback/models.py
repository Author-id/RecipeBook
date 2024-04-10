from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from recipebook.recipes.models import Recipe


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        related_name="comments",
        verbose_name="деятель",
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name="comments",
        verbose_name="рецепт",
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(
        verbose_name="создан",
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        verbose_name="обновлен",
        auto_now=True,
    )

    def __str__(self):
        return _(f"comment__by {self.author} on {self.recipe}")

    class Meta:
        verbose_name = "комментарий"
        verbose_name_plural = "комментарии"


class RatingChoices(models.IntegerChoices):
    HATE = 1, _("rating__rating_choices__hate")
    DISLIKE = 2, _("rating__rating_choices__dislike")
    NEUTRAL = 3, _("rating__rating_choices__neutral")
    LIKE = 4, _("rating__rating_choices__like")
    LOVE = 5, _("rating__rating_choices__love")


class Rate(models.Model):
    author = models.ForeignKey(
        User,
        related_name="ratings",
        verbose_name="автор",
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name="ratings",
        verbose_name="рецепт",
        on_delete=models.CASCADE,
    )
    value = models.CharField(
        max_length=7,
        verbose_name="оценка",
        choices=RatingChoices,
    )

    def __str__(self):
        return _(f"{self.value} rated__by {self.author}")

    class Meta:
        verbose_name = "оценка"
        verbose_name_plural = "оценки"


__all__ = []
