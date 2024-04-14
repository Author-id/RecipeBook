from django import forms

from core.forms import BaseForm
from feedback.models import Rate


class RatingForm(forms.ModelForm, BaseForm):
    class Meta:
        model = Rate
        fields = [
            model.value.field.name,
        ]


class DeleteRatingForm(BaseForm):
    delete = forms.BooleanField(widget=forms.HiddenInput, initial=True)


__all__: list[str] = []