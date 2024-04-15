from typing import Any

from django import forms
from django.core.exceptions import ValidationError
from django.forms.renderers import TemplatesSetting

from core.forms import BaseForm
from feedback.models import Rate
from recipes import models


class RatingForm(forms.ModelForm, BaseForm):
    class Meta:
        model = Rate
        fields = [
            model.value.field.name,
        ]


class DeleteRatingForm(BaseForm):
    delete = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class IngredientsWidget(forms.Widget):
    template_name = "recipes/includes/ingredients_widget.html"

    @property
    def media(self) -> forms.Media:
        return forms.Media(
            css={
                "all": ["css/ingredients_widget.css"],
            },
        )

    def render(
        self,
        name: str,
        value: Any,
        attrs: Any = None,
        renderer: Any = None,
    ) -> Any:
        context = self.get_context(name, value, attrs)
        return self._render(self.template_name, context, TemplatesSetting())

    def value_from_datadict(
        self,
        data: dict[str, Any],
        files: Any,
        name: str,
    ) -> Any:
        value = []
        for key in data:
            if not key.startswith(name):
                continue

            keys = key.split("_")
            if len(keys) != 3:
                continue

            _, id_, field = keys

            if field == "ingredient":
                value.append(
                    {
                        "id": id_,
                        "ingredient": data[key],
                        "count": data["_".join([name, id_, "count"])],
                        "unit": data["_".join([name, id_, "unit"])],
                    },
                )

        return value

    def get_context(
        self,
        name: str,
        value: dict,
        attrs: Any,
    ) -> dict[str, Any]:
        context = super().get_context(name, value, attrs)
        value = value or []
        id_ = attrs.get("id")
        context["widget"]["id"] = id_
        context["widget"]["name"] = name
        context["widget"]["subwidgets"] = value
        context["widget"]["unit_options"] = models.IngredientUnit.choices
        context["widget"]["ingredients"] = models.Ingredient.objects.all()

        return context


class IngredientsField(forms.Field):
    widget = IngredientsWidget

    def prepare_value(self, value: Any) -> Any:
        prepared = []
        for v in value:
            if isinstance(v, dict):
                if not v["count"].isdecimal():
                    v["count"] = 0

                if not v["ingredient"].isdigit():
                    v["ingredient"] = 0

                prepared.append(v)
            else:
                prepared.append(
                    {
                        "id": v.id,
                        "ingredient": v.ingredient_id,
                        "count": v.count,
                        "unit": v.unit,
                    },
                )

        return prepared

    def clean(self, value: Any) -> Any:
        cleaned = []
        for v in value:
            id_ = v["id"]
            ingredient = v["ingredient"]
            count = v["count"]
            unit = v["unit"]
            new = "x" in id_
            if not new and not id_.isdigit():
                continue

            if not ingredient.isdigit() or int(ingredient) < 0:
                raise forms.ValidationError(
                    forms.FloatField.default_error_messages["invalid"],
                    code="invalid",
                )

            try:
                ingredient = models.Ingredient.objects.get(id=int(ingredient))
                ri = models.RecipeIngredient()
                ri.ingredient = ingredient
                ri.count = count
                ri.unit = unit
                ri.clean_fields()
            except ValidationError as er:
                er = dict(er)
                del er[models.RecipeIngredient.recipe.field.name]
                if er != {}:
                    raise forms.ValidationError(str(er))
            except models.Ingredient.DoesNotExist as er:
                raise forms.ValidationError(str(er))

            cleaned.append(
                {
                    "new": new,
                    "id": id_,
                    "ingredient": ingredient,
                    "count": float(count),
                    "unit": unit,
                },
            )

        return cleaned


class RecipeForm(forms.ModelForm, BaseForm):
    ingredients = IngredientsField()

    class Meta:
        model = models.Recipe
        fields = [
            models.Recipe.name.field.name,
            models.Recipe.main_image.field.name,
            models.Recipe.categories.field.name,
            models.Recipe.level.field.name,
            models.Recipe.time.field.name,
            models.Recipe.instruction.field.name,
        ]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        instance = kwargs["instance"]
        self.initial["ingredients"] = instance.ingredients.all()

    def save(self, commit: bool = True) -> models.Recipe:
        instance: models.Recipe = super().save(commit)
        ingredients_quary = instance.ingredients.all()
        ingredients_current = list(ingredients_quary)
        ingredients_new = self.cleaned_data["ingredients"]
        created_ingredients = []
        deleted_ingredients = []
        deleted_ingredients_ids = []
        for ingredient in ingredients_current:
            id_ = str(ingredient.id)
            deleted = True
            for ing in ingredients_new:
                if ing["id"] == id_:
                    deleted = False
                    break

            if deleted:
                deleted_ingredients.append(ingredient.id)
                deleted_ingredients_ids.append(ingredient.ingredient_id)

        for ingredient_data in ingredients_new:
            id_ = ingredient_data["id"]
            ingredient = ingredient_data["ingredient"]
            count = ingredient_data["count"]
            unit = ingredient_data["unit"]

            if id_.isdigit():
                id_ = int(id_)
                existing = None
                ing_used = False
                for ing in ingredients_current:
                    if ing.id == id_:
                        existing = ing
                    elif ing.ingredient_id == ingredient.id:
                        ing_used = True

                if existing:
                    if (
                        ing_used
                        and ingredient.id not in deleted_ingredients_ids
                    ):
                        deleted_ingredients.append(id_)
                    else:
                        existing.ingredient = ingredient
                        existing.count = count
                        existing.unit = unit

                continue

            existing = False
            for ing in ingredients_current:
                if ing.ingredient_id == ingredient.id:
                    existing = True
                    break

            if existing and ingredient.id not in deleted_ingredients_ids:
                continue

            created_ingredients.append(
                models.RecipeIngredient(
                    recipe=instance,
                    ingredient=ingredient,
                    count=count,
                    unit=unit,
                ),
            )

        if deleted_ingredients:
            models.RecipeIngredient.objects.filter(
                id__in=deleted_ingredients,
            ).delete()

        models.RecipeIngredient.objects.bulk_update(
            ingredients_quary,
            fields=[
                models.RecipeIngredient.ingredient.field.name,
                models.RecipeIngredient.count.field.name,
                models.RecipeIngredient.unit.field.name,
            ],
        )

        if created_ingredients:
            models.RecipeIngredient.objects.bulk_create(created_ingredients)

        return instance


__all__ = []
