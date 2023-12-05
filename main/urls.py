from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from product.views import ProductViewSet, AddToCartView, ViewCartView, RemoveFromCartView, ClearCartView

schema_view = get_schema_view(
   openapi.Info(
      title="Shop",
      default_version='v1',
      description="",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


product = [
    path("add-cart/", AddToCartView.as_view()),
    path("get-cart/", ViewCartView.as_view()),
    path('remove-from-cart/<int:product_id>/', RemoveFromCartView.as_view()),
    path("remove-all/", ClearCartView.as_view()),
]

router = DefaultRouter()
router.register(r'product', ProductViewSet, basename='user')
urlpatterns = router.urls


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path("api/v1/", include(product))
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT,
    )
if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT,
    )
