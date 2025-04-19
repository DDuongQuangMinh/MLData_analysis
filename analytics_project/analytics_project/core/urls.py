from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DatasetViewSet, TrainedModelViewSet, RegisterUser
from .views import eda_summary, eda_visuals
from .views import train_model
from .views import predict_model

router = DefaultRouter()
router.register(r'datasets', DatasetViewSet, basename='dataset')
router.register(r'models', TrainedModelViewSet, basename='trainedmodel')

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('eda/<int:dataset_id>/', eda_summary, name='eda-summary'),
    path('eda/<int:dataset_id>/visuals/', eda_visuals, name='eda-visuals'),
    path('train/<int:dataset_id>/', train_model, name='train-model'),
    path('predict/<int:model_id>/', predict_model, name='predict-model'),
    path('', include(router.urls)),
]
