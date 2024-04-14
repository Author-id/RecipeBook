from typing import Any

from django.db.models import Count, Sum
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import DetailView, ListView, TemplateView

from feedback.models import Rate
from recipes.forms import DeleteRatingForm, RatingForm
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

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        recipe = self.get_object()
        ratings = Rate.objects.filter(recipe=recipe).aggregate(
            sum=Sum("value"),
            count=Count("value"),
        )
        rating_count = ratings["count"]
        rating_sum = ratings["sum"] or 0

        user_rating = None
        if self.request.user.is_authenticated:
            user_rating = Rate.objects.filter(
                author=self.request.user,
                recipe=recipe,
            ).first()

        context.update(
            {
                "rating_form": RatingForm(instance=user_rating),
                "delete_rating_form": DeleteRatingForm(),
                "rating": (
                    round(rating_sum / rating_count, 2)
                    if rating_count > 0
                    else 0
                ),
                "rating_count": rating_count,
                "user_rating": user_rating,
            },
        )

        return context

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        self.object = self.get_object()
        context = self.get_context_data()
        user_rating = context["user_rating"]
        form = RatingForm(request.POST, instance=user_rating)
        delete_form = DeleteRatingForm(request.POST)
        context["rating_form"] = form
        if self.request.user.is_authenticated:
            if form.is_valid():
                if user_rating:
                    form.save()
                else:
                    user_rating = form.save(False)
                    user_rating.author = self.request.user
                    user_rating.recipe = self.object
                    user_rating.save()

                return redirect(reverse("recipes:recipe", args=[pk]))

            if user_rating and delete_form.is_valid():
                user_rating.delete()
                return redirect(reverse("recipes:recipe", args=[pk]))

        return self.render_to_response(context)


__all__ = []
