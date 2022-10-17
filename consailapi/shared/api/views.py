from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.permissions import AllowAny


class MySpectacularAPIView(SpectacularAPIView):
    permission_classes = (AllowAny,)


class SwaggerView(SpectacularSwaggerView):
    permission_classes = (AllowAny,)
