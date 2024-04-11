from django.contrib import admin

from feedback import models


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Rate)
class RateAdmin(admin.ModelAdmin):
    pass


__all__ = []
