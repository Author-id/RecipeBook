from django.contrib import admin

from core.utils import make_admin_fieldsets
from recipes import models


class AdditionalImageAdmin(admin.TabularInline):
    model = models.AdditionalImage
    fields = [
        models.AdditionalImage.image_tmb.__name__,
        models.AdditionalImage.image.field.name,
    ]
    readonly_fields = [models.AdditionalImage.image_tmb.__name__]
    extra = 1


class RecipeIngredientAdmin(admin.TabularInline):
    model = models.RecipeIngredient
    extra = 1


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Kitchen)
class KitchenAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        models.Recipe.title.field.name,
        models.Recipe.state.field.name,
    )
    list_display_links = (models.Recipe.title.field.name,)
    fieldsets = make_admin_fieldsets(
        [
            models.Recipe.title.field.name,
            models.Recipe.author.field.name,
            models.Recipe.created.field.name,
            models.Recipe.updated.field.name,
            models.Recipe.categories.field.name,
            models.Recipe.kitchen.field.name,
            models.Recipe.level.field.name,
            models.Recipe.time.field.name,
            models.Recipe.main_image.field.name,
            models.Recipe.image_tmb.__name__,
            models.Recipe.instruction.field.name,
        ],
    )
    filter_horizontal = (models.Recipe.categories.field.name,)
    readonly_fields = [
        models.Recipe.created.field.name,
        models.Recipe.updated.field.name,
        models.Recipe.image_tmb.__name__,
    ]
    inlines = [AdditionalImageAdmin, RecipeIngredientAdmin]


__all__ = []
