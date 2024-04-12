from typing import Any

from django.db.models.query import QuerySet
from django.views.generic import DetailView, ListView, TemplateView

from core.utils import normalize_name
from recipes.models import Category, Ingredient, Recipe, RecipeLevel


class MainView(TemplateView):
    template_name = "recipes/main.html"


class SearchView(ListView):
    template_name = "recipes/search.html"
    context_object_name = "recipes"

    def get_queryset(self) -> QuerySet:
        queryset = Recipe.objects.all()

        search_name = self.request.GET.get("sn", "")
        if search_name:
            search_name = normalize_name(search_name)
            queryset = queryset.filter(normalized_name__contains=search_name)

        search_category = self.request.GET.get("sc", "")
        if search_category.isdigit():
            queryset = queryset.filter(categories__in=[search_category])

        search_ingredients = self.request.GET.get("si", "")
        if search_ingredients:
            ingredients = [int(v) for v in search_ingredients.split("-") if v.isdigit()]
            queryset = queryset.filter(ingredients__ingredient__in=ingredients)

        search_ingredients_exclude = self.request.GET.get("sie", "")
        if search_ingredients_exclude:
            ingredients = [int(v) for v in search_ingredients_exclude.split("-") if v.isdigit()]
            queryset = queryset.exclude(ingredients__ingredient__in=ingredients)

        search_level = self.request.GET.get("sl", "")
        if search_level.isdigit():
            return queryset.filter(level=search_level)

        return queryset

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        context.update(
            {
                "categories": Category.objects.all(),
                "ingredients": Ingredient.objects.all(),
                "levels": RecipeLevel.choices,
            },
        )

        return context


class RecipeView(DetailView):
    template_name = "recipes/recipe.html"
    queryset = Recipe.objects.all()
    context_object_name = "recipe"


__all__ = []
