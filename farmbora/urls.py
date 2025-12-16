from django.contrib import admin
from django.urls import path
from django.urls import include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

schema_view=get_schema_view(
    openapi.Info(
        title="FarmBora API",
        default_version='v1',
        description="API documentation for FarmBora",
    ),
    public=True,
    permission_classes=[AllowAny],
    authentication_classes=[],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('user.urls')),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0)),
]


