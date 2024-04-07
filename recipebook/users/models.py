import sys
from typing import Any, cast

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import User as AuthUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy
from sorl.thumbnail import get_thumbnail


UserBase = get_user_model()  # type: Any
if "makemigrations" not in sys.argv and "migrate" not in sys.argv:
    f: Any = AuthUser._meta.get_field("email")
    f._unique = True


class UserManager(BaseUserManager):
    @classmethod
    def normalize_email(cls, email: str | None) -> str:
        email = super().normalize_email(email)
        if "@" not in email:
            return email

        email = email.lower()
        username, domain = email.split("@")

        if domain == "ya.ru":
            domain = "yandex.ru"

        if "+" in username:
            username = username.split("+")[0]

        if domain == "gmail.com":
            username = username.replace(".", "")

        if domain == "yandex.ru":
            username = username.replace(".", "-")

        return f"{username}@{domain}"

    def get_queryset(self) -> models.query.QuerySet:
        return (
            super()
            .get_queryset()
            .select_related(
                AuthUser.profile.related.name,
            )
        )

    def active(self) -> models.query.QuerySet:
        return self.get_queryset().filter(is_active=True)

    def by_mail(self, mail: str) -> "User | None":
        mail = self.normalize_email(mail)
        try:
            return cast(User, self.get_queryset().get(email=mail))
        except User.DoesNotExist:
            return None

    def by_username(self, username: str) -> "User | None":
        try:
            return cast(User, self.get_queryset().get(username=username))
        except User.DoesNotExist:
            return None


class User(UserBase):
    objects: UserManager["User"] = UserManager()

    class Meta:
        proxy = True


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name=gettext_lazy("users__model__profile__user"),
        on_delete=models.CASCADE,
        related_name="profile",
        related_query_name="profile",
    )
    email = models.EmailField(
        verbose_name=gettext_lazy("users__model__profile__email"),
        unique=True,
    )
    password = models.CharField(
        verbose_name=gettext_lazy("users__model__profile__email"),
        max_length=128,
    )
    name = models.CharField(
        verbose_name=gettext_lazy("users__model__profile__name"),
        max_length=255,
        blank=True,
        null=True,
    )
    image = models.ImageField(
        verbose_name=gettext_lazy("users__model__profile__image"),
        upload_to="users/profile/",
        null=True,
        blank=True,
    )
    trusted = models.BooleanField(
        verbose_name=gettext_lazy("users__model__profile__trusted"),
        default=False,
    )
    date_joined = models.DateTimeField(
        verbose_name=gettext_lazy("users__model__profile__date_joined"),
        default=timezone.now,
    )
    is_superuser = models.BooleanField(
        verbose_name=gettext_lazy("users__model__profile__is_superuser"),
        default=False,
    )
    is_active = models.BooleanField(
        verbose_name=gettext_lazy("users__model__profile__is_active"),
        default=True,
    )
    attempts_count = models.PositiveIntegerField(
        verbose_name=gettext_lazy("users__model__profile__attempts_count"),
        default=0,
    )
    deactivation_date = models.DateTimeField(
        verbose_name=gettext_lazy("users__model__profile__deactivation_date"),
        null=True,
        blank=True,
    )

    def get_image_32x32(self):
        if not self.image:
            return None

        return get_thumbnail(
            self.image,
            "32x32",
            crop="center",
            quality=85,
            format="PNG",
        )

    def get_image_128x128(self):
        if not self.image:
            return None

        return get_thumbnail(
            self.image,
            "128x128",
            crop="center",
            quality=85,
            format="PNG",
        )

    def __str__(self) -> str:
        return f"#{self.pk}"

    class Meta:
        verbose_name = gettext_lazy("users__model__profile__verbose_name")
        verbose_name_plural = gettext_lazy(
            "users__model__profile__verbose_name_plural",
        )


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
@receiver(post_save, sender=User)
def post_save_receiver(
    sender: str,
    instance: User,
    created: bool = False,
    **kwargs: Any,
) -> None:
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()


__all__: list[str] = []
