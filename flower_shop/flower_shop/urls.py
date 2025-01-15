from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.urls import path
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from user_auth.urls import router as user_roter
from catigories.urls import router as categories_router
urlpatterns =[
    path('admin/', admin.site.urls),
    path('api/', include(user_roter.urls)),
    path('api/',include(categories_router.urls)),

    # Генерация схемы OpenAPI
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    # Swagger UI
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # ReDoc UI (альтернативная документация)
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
  
]