from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def root_ping(request):  # debug helper
    return JsonResponse({"ok": True, "where": "career_backend.urls"})

urlpatterns = [
    path("admin/", admin.site.urls),
    path("ping/", root_ping),             
    path("api/", include("api.urls")),    
]
