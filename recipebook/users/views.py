from django.conf import settings
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext
from django.views.generic import FormView

from users.forms import SignUpForm


class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = SignUpForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form: SignUpForm) -> HttpResponse:
        user = form.save(commit=False)
        user.is_active = settings.DEFAULT_USER_IS_ACTIVE
        user.save()

        current_site = get_current_site(self.request)
        site_name = current_site.name
        domain = current_site.domain
        use_https = self.request.is_secure()
        email = form.cleaned_data["email"]
        mail_context = {
            "username": form.cleaned_data["username"],
            "domain": domain,
            "site_name": site_name,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": default_token_generator.make_token(user),
            "protocol": "https" if use_https else "http",
        }
        send_mail(
            gettext("signup__mail__subject"),
            render_to_string("users/signup_email.html", mail_context),
            None,
            [email],
            fail_silently=False,
        )
        messages.success(
            self.request,
            gettext("signup__success_message") % {"email": email},
        )
        return super().form_valid(form)


__all__: list[str] = []
