import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import UploadedDataset
from .serializers import UploadedDatasetSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from sklearn.linear_model import LinearRegression
import joblib
import os
from rest_framework.permissions import IsAuthenticated
from .models import MLModel
from .serializers import MLModelSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserSerializer
from rest_framework import generics
from .models import MLModel
from .serializers import MLModelSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from rest_framework import authentication

class UploadCSVView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, format=None):
        file_obj = request.FILES['file']
        dataset = UploadedDataset.objects.create(name=file_obj.name, file=file_obj)
        serializer = UploadedDatasetSerializer(dataset)
        return Response(serializer.data)

class EDAView(APIView):
    def get(self, request, dataset_id):
        dataset = UploadedDataset.objects.get(id=dataset_id)
        df = pd.read_csv(dataset.file.path)

        return Response({
            "shape": df.shape,
            "columns": list(df.columns),
            "head": df.head().to_dict(),
            "describe": df.describe().to_dict(),
            "nulls": df.isnull().sum().to_dict(),
        })
    
class PredictView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, dataset_id):
        target = request.data.get("target")
        dataset = UploadedDataset.objects.get(id=dataset_id)
        df = pd.read_csv(dataset.file.path)
        df = df.dropna()

        X = df.drop(columns=[target])
        y = df[target]

        model = LinearRegression()
        model.fit(X, y)

        prediction = model.predict(X)

        return Response({
            "target": target,
            "predictions": prediction.tolist()
        })
    
class TrainAndSaveModelView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, dataset_id):
        target = request.data.get("target")
        model_name = request.data.get("model_name")

        dataset = UploadedDataset.objects.get(id=dataset_id)
        df = pd.read_csv(dataset.file.path).dropna()
        X = df.drop(columns=[target])
        y = df[target]

        model = LinearRegression()
        model.fit(X, y)

        # Versioning
        last_model = MLModel.objects.filter(user=request.user, name=model_name).order_by('-version').first()
        version = last_model.version + 1 if last_model else 1

        # Save to disk
        model_dir = f'media/models/user_{request.user.id}'
        os.makedirs(model_dir, exist_ok=True)
        model_path = f'{model_dir}/{model_name}_v{version}.pkl'
        joblib.dump(model, model_path)

        # Save in DB
        ml_model = MLModel.objects.create(
            user=request.user,
            dataset=dataset,
            name=model_name,
            version=version,
            file=model_path
        )

        serializer = MLModelSerializer(ml_model)
        return Response(serializer.data)
    
    def broadcast_log(user, message):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"train_logs_{user.id}",
            {"type": "send_log", "message": message}
        )
    
class PredictSavedModelView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        model_name = request.data.get('model_name')
        version = request.data.get('version')
        input_data = request.data.get('input')  # Expect list of dicts

        ml_model = MLModel.objects.get(user=request.user, name=model_name, version=version)
        model = joblib.load(ml_model.file.path)

        df_input = pd.DataFrame(input_data)
        preds = model.predict(df_input)

        return Response({"predictions": preds.tolist()})

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = []
    authentication_classes = []
    serializer_class = UserSerializer

class ListUserModelsView(generics.ListAPIView):
    serializer_class = MLModelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MLModel.objects.filter(user=self.request.user)

class DeleteModelView(generics.DestroyAPIView):
    serializer_class = MLModelSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        return MLModel.objects.filter(user=self.request.user)
    
class RenameModelView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        new_name = request.data.get("new_name")
        model = MLModel.objects.get(pk=pk, user=request.user)
        model.name = new_name
        model.save()
        return Response({"status": "renamed", "new_name": new_name})
