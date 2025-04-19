from django.urls import path
from .views import UploadCSVView, EDAView, PredictView, TrainAndSaveModelView, PredictSavedModelView, ListUserModelsView, DeleteModelView, RenameModelView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView

urlpatterns = [
    path('upload/', UploadCSVView.as_view(), name='upload'),
    path('eda/<int:dataset_id>/', EDAView.as_view(), name='eda'),
    path('predict/<int:dataset_id>/', PredictView.as_view(), name='predict'),
    path('train/<int:dataset_id>/', TrainAndSaveModelView.as_view(), name='train_model'),
    path('predict-saved/', PredictSavedModelView.as_view(), name='predict_saved'),
    path('auth/register/', RegisterView.as_view(), name='auth_register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('models/', ListUserModelsView.as_view()),
    path('models/delete/<int:pk>/', DeleteModelView.as_view()),
    path('models/rename/<int:pk>/', RenameModelView.as_view()),
]