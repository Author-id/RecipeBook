from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(
        verbose_name="название",
        max_length=50,
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"


class Kitchen(models.Model):
    name = models.CharField(
        verbose_name="название",
        max_length=100,
    )

    class Meta:
        verbose_name = "кухня"
        verbose_name_plural = "кухни"


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name="название",
        max_length=255,
    )

    class Meta:
        verbose_name = "ингредиент"
        verbose_name_plural = "ингредиенты"


class Level(models.IntegerChoices):
    EASY = 1, _("recipes__level_choices__easy")
    NORMAL = 2, _("recipes__level_choices__normal")
    HARD = 3, _("recipes__level_choices__hard")
    EXTREME = 4, _("recipes__level_choices__extreme")


class Recipe(models.Model):
    title = models.CharField(
        verbose_name="заголовок",
        max_length=200,
    )
    author = models.ForeignKey(
        User,
        verbose_name="автор",
        related_name="recipe",
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(
        verbose_name="дата создания",
        auto_now_add=True,
        null=True,
    )
    updated = models.DateTimeField(
        verbose_name="дата изменения",
        auto_now=True,
        null=True,
    )
    category = models.ForeignKey(
        Category,
        related_name="recipe",
        verbose_name="категория",
        on_delete=models.SET_NULL,
        null=True,
    )
    kitchen = models.ForeignKey(
        Kitchen,
        related_name="recipe",
        verbose_name="кухня",
        on_delete=models.SET_NULL,
        null=True,
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name="recipe",
        verbose_name="ингредиент",
    )
    instruction = models.TextField(
        verbose_name="инструкция",
    )
    main_image = models.ImageField(
        verbose_name="главное изображение",
        upload_to="recipes/",
    )
    images = models.ManyToManyField(
        "AdditionalImage",
        related_name="recipe",
        verbose_name="фотографии",
        blank=True,
    )
    level = models.CharField(
        max_length=50,
        choices=Level,
        verbose_name="уровень сложности",
    )
    time = models.PositiveIntegerField(
        verbose_name="время готовки",
    )
    comments = models.ManyToManyField(
        "Comment",
        related_name="recipe",
        verbose_name="комментарий",
        blank=True,
    )
    rates = models.ManyToManyField(
        "Rate",
        related_name="recipe",
        verbose_name="оценки",
        blank=True,
    )

    class Meta:
        verbose_name = "рецепт"
        verbose_name_plural = "рецепты"


class UnitChoices(models.IntegerChoices):
    GRAM = 1, _("recipes__unit_choices__gram")
    KILOGRAM = 2, _("recipes__unit_choices__kilogram")
    LITER = 3, _("recipes__unit_choices__liter")
    MILLILITER = 4, _("recipes__unit_choices__milliliter")
    THING = 3, _("recipes__unit_choices__thing")
    TEASPOON = 4, _("recipes__unit_choices__tea_spoon")
    PIECE = 5, _("recipes__unit_choices__piece")
    TABLESPOON = 4, _("recipes__unit_choices__table_spoon")


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="recipe ingredients",
        verbose_name="рецепт",
    )
    ingredient = models.CharField(
        max_length=200,
        verbose_name="ингредиент",
    )
    count = models.FloatField(
        verbose_name="количество ингредиентов",
    )
    unit = models.CharField(
        max_length=200,
        verbose_name="единица измерения",
        choices=UnitChoices,
    )

    class Meta:
        verbose_name = "ингредиент"
        verbose_name_plural = "ингредиенты"


class AdditionalImage(models.Model):
    image = models.ImageField(
        upload_to="recipes/additional/",
        verbose_name="изображение",
    )

    class Meta:
        verbose_name = "изображение"
        verbose_name_plural = "изображения"


__all__: list[str] = []
