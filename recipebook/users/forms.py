from typing import Any

from django import forms
from django.contrib.auth.forms import UserCreationForm

from core.forms import BaseForm
from users import models


class SignUpForm(UserCreationForm, BaseForm):
    def clean(self) -> dict[str, Any]:
        email = self.cleaned_data["email"]
        email = models.UserManager.normalize_email(email)
        self.cleaned_data["email"] = email

        return self.cleaned_data

    class Meta(UserCreationForm.Meta):
        fields = ["username", "email"]
        widgets = {
            "email": forms.EmailInput(attrs={"required": "required"}),
        }


__all__: list[str] = []
