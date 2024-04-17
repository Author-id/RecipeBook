from typing import Any

from django.db.models import Count, Sum
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import DetailView, ListView, TemplateView

from feedback.forms import (
    CommentForm,
    DeleteCommentForm,
    DeleteRatingForm,
    RatingForm,
)
from feedback.forms import CookForm, DeleteCookForm
from feedback.models import Comment, Cooked, Rate
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
    queryset = Recipe.objects.optimize_for_detail_page(
        Recipe.objects.published(),
    )
    context_object_name = "recipe"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        recipe = self.object
        user_cooked = None
        if self.request.user.is_authenticated:
            user_cooked = Cooked.objects.filter(
                author=self.request.user,
                recipe=recipe,
            ).first()

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

        comments = list(Comment.objects.filter(recipe=recipe).all())
        user_comment = None
        for i, comment in enumerate(comments):
            if comment.author_id == self.request.user.id:
                user_comment = comment
                del comments[i]
                break

        context.update(
            {
                "rating_form": RatingForm(instance=user_rating),
                "delete_rating_form": DeleteRatingForm(),
                "comment_form": CommentForm(instance=user_comment),
                "delete_comment_form": DeleteCommentForm(),
                "rating": (
                    round(rating_sum / rating_count, 2)
                    if rating_count > 0
                    else 0
                ),
                "rating_count": rating_count,
                "user_rating": user_rating,
                "user_comment": user_comment,
                "comments": comments,
                "user_cooked": user_cooked,
                "cook_form": CookForm(instance=user_cooked),
                "delete_cook_form": DeleteCookForm(),
            },
        )

        return context

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        self.object = self.get_object()
        context = self.get_context_data()
        user_rating = context["user_rating"]
        user_comment = context["user_comment"]
        user_cooked = context["user_cooked"]
        rating_form = RatingForm(request.POST, instance=user_rating)
        comment_form = CommentForm(request.POST, instance=user_comment)
        delete_rating_form = DeleteRatingForm(request.POST)
        delete_comment_form = DeleteCommentForm(request.POST)
        cook_form = CookForm(request.POST, instance=user_cooked)
        delete_cook_form = DeleteCookForm(request.POST)

        if self.request.user.is_authenticated:
            if rating_form.is_valid():
                if user_rating:
                    rating_form.save()
                else:
                    user_rating = rating_form.save(False)
                    user_rating.author = self.request.user
                    user_rating.recipe = self.object
                    user_rating.save()

                return redirect(reverse("recipes:recipe", args=[pk]))

            if user_rating and delete_rating_form.is_valid():
                user_rating.delete()
                return redirect(reverse("recipes:recipe", args=[pk]))

            if self.request.user.is_authenticated:

                if user_cooked and delete_cook_form.is_valid():
                    user_cooked.delete()
                    return redirect(reverse("recipes:recipe", args=[pk]))

                if cook_form.is_valid():
                    if user_cooked:
                        cook_form.save()
                    else:
                        user_cooked = cook_form.save(False)
                        user_cooked.author = self.request.user
                        user_cooked.recipe = self.object
                        user_cooked.save()

                    return redirect(reverse("recipes:recipe", args=[pk]))

            if comment_form.is_valid():
                if user_comment:
                    comment_form.save()
                else:
                    user_comment = comment_form.save(False)
                    user_comment.author = self.request.user
                    user_comment.recipe = self.object
                    user_comment.save()

                return redirect(reverse("recipes:recipe", args=[pk]))

            if user_comment and delete_comment_form.is_valid():
                user_comment.delete()
                return redirect(reverse("recipes:recipe", args=[pk]))

        return self.render_to_response(context)


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
