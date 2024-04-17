from django import forms

from core.forms import BaseForm
from feedback.models import Comment, Cooked, Rate


class RatingForm(forms.ModelForm, BaseForm):
    class Meta:
        model = Rate
        fields = [
            model.value.field.name,
        ]


class DeleteRatingForm(BaseForm):
    delete_rating = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class CommentForm(forms.ModelForm, BaseForm):
    class Meta:
        model = Comment
        fields = [
            model.text.field.name,
        ]


class DeleteCommentForm(BaseForm):
    delete_comment = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class CookForm(forms.ModelForm, BaseForm):
    class Meta:
        model = Cooked
        fields = []


class DeleteCookForm(BaseForm):
    delete_cook = forms.BooleanField(widget=forms.HiddenInput, initial=True)


__all__ = []
