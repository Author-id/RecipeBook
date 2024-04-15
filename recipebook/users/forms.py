from typing import Any

from betterforms.multiform import MultiModelForm
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

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


class UserForm(UserChangeForm, BaseForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields.pop("password")

    class Meta(UserChangeForm.Meta):
        fields = ["first_name", "last_name"]


class ProfileForm(forms.ModelForm, BaseForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields[models.User.trusted.field.name].disabled = True
        self.fields[models.User.email.field.name].disabled = True

    class Meta:
        model = models.User
        fields = [
            models.User.email.field.name,
            models.User.trusted.field.name,
            models.User.image.field.name,
        ]


class UserProfileForm(MultiModelForm):
    form_classes = {
        "user": UserForm,
        "profile": ProfileForm,
    }


__all__ = []
