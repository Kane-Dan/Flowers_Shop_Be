from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategotyViewSet

router = DefaultRouter()
router.register(r'categories', CategotyViewSet, basename='categories')

urlpatterns = [
    path('categories/', include(router.urls)),
]