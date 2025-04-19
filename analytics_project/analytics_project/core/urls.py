from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DatasetViewSet, TrainedModelViewSet, RegisterUser

router = DefaultRouter()
router.register(r'datasets', DatasetViewSet, basename='dataset')
router.register(r'models', TrainedModelViewSet, basename='trainedmodel')

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('', include(router.urls)),
]
