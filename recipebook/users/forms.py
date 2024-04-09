from typing import Any

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
        model = models.User
        fields = ["username", "email"]


__all__ = []
