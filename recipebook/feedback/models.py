from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from recipes.models import Recipe


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return "Comment by {} on {}".format(self.author, self.recipe)


class RatingChoices(models.IntegerChoices):
    HATE = 1, _("rating__rating_choices__hate")
    DISLIKE = 2, _("rating__rating_choices__dislike")
    NEUTRAL = 3, _("rating__rating_choices__neutral")
    LIKE = 4, _("rating__rating_choices__like")
    LOVE = 5, _("rating__rating_choices__love")


class Rate(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name="ratings",
        on_delete=models.CASCADE,
    )
    value = models.CharField(
        max_length=7,
        choices=RatingChoices,
    )

    def __str__(self):
        return "{} rating by {}".format(self.value, self.author)


__all__ = []
