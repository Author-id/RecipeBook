from typing import Any

from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import DetailView, ListView, TemplateView

from recipes.forms import RecipeForm
from recipes.models import Category, Ingredient, Kitchen, Recipe, RecipeLevel


class MainView(TemplateView):
    template_name = "recipes/main.html"


class SearchView(ListView):
    template_name = "recipes/search.html"
    paginate_by = 16
    context_object_name = "recipes"

    def get_queryset(self) -> QuerySet:
        queryset = Recipe.objects.search(self.request.GET)
        return Recipe.objects.optimize_for_search_page(queryset)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        context.update(
            {
                "categories": Category.objects.all(),
                "ingredients": Ingredient.objects.all(),
                "kitchens": Kitchen.objects.all(),
                "levels": RecipeLevel.choices,
            },
        )

        return context


class RecipeView(DetailView):
    template_name = "recipes/recipe.html"
    queryset = Recipe.objects.published()
    context_object_name = "recipe"


class RecipeEditView(DetailView):
    template_name = "recipes/recipe_edit.html"
    queryset = Recipe.objects.published()
    context_object_name = "recipe"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        item = self.get_object()

        context.update(
            {
                "form": RecipeForm(instance=item),
            },
        )

        return context

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        self.object = self.get_object()
        context = self.get_context_data()
        form = RecipeForm(request.POST, instance=self.object)
        context["form"] = form
        if self.request.user.is_authenticated:
            if form.is_valid():
                form.save()
                return redirect(reverse("recipes:recipe-edit", args=[pk]))

        return self.render_to_response(context)


__all__ = []
