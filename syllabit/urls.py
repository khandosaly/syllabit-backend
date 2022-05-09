from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from syllabit import settings

urlpatterns = [
    path("api/v1.0/admin/", admin.site.urls),
    path('api/v1.0/auth/', include("users.urls")),
    path('api/v1.0/syllabus/', include("syllabus.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
