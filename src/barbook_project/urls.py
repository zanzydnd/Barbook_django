from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from barbook_app import urls
from django.urls import include
from barbook_api import urls as urls_api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(urls)),
    path("api/", include(urls_api)),
]

urlpatterns += [url(r"^silk/", include("silk.urls", namespace="silk"))]
