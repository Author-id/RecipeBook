from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, URLPattern, URLResolver


urlpatterns: list[URLResolver | URLPattern] = [
    path("users/", include("django.contrib.auth.urls")),
    path("i18n/", include("django.conf.urls.i18n")),
    path("admin/", admin.site.urls),
    path("mdeditor/", include("mdeditor.urls")),
]

if settings.MEDIA_URL:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)
