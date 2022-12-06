from django.contrib import admin
from django.contrib.staticfiles.views import serve
from django.templatetags.static import static
from django.urls import path, re_path
from django.views.generic import RedirectView


def serve_(*argv, **kwargs):
    return serve(*argv, insecure=True, **kwargs)


urlpatterns = [
    re_path('.*favicon.ico', RedirectView.as_view(url=static('favicon.ico'))),
    path('', admin.site.urls),
]
