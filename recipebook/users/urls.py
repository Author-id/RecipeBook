from django.contrib.auth import views
from django.contrib.auth.forms import AuthenticationForm
from django.urls import path

from core.forms import add_styles_to_form


app_name = "users"

urlpatterns = [
    path(
        "login/",
        views.LoginView.as_view(
            template_name="users/login.html",
            form_class=add_styles_to_form(AuthenticationForm),
        ),
        name="login",
    ),
    path(
        "logout/",
        views.LogoutView.as_view(),
        name="logout",
    ),
]


__all__: list[str] = []
