from rest_framework import viewsets, generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from .models import Dataset, TrainedModel
from .serializers import DatasetSerializer, TrainedModelSerializer, UserSerializer
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Dataset
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import joblib
import os
from django.conf import settings

class RegisterUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.create(user=user)
        return Response({'token': token.key, 'user': UserSerializer(user).data})

class DatasetViewSet(viewsets.ModelViewSet):
    serializer_class = DatasetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Dataset.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TrainedModelViewSet(viewsets.ModelViewSet):
    queryset = TrainedModel.objects.all()
    serializer_class = TrainedModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TrainedModel.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def eda_summary(request, dataset_id):
    try:
        dataset = Dataset.objects.get(id=dataset_id, user=request.user)
    except Dataset.DoesNotExist:
        return Response({"error": "Dataset not found"}, status=404)

    df = pd.read_csv(dataset.file.path)

    summary = {
        'shape': df.shape,
        'columns': list(df.columns),
        'dtypes': df.dtypes.astype(str).to_dict(),
        'missing_values': df.isnull().sum().to_dict(),
        'description': df.describe(include='all').fillna("").to_dict(),
    }

    return Response(summary)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def eda_visuals(request, dataset_id):
    try:
        dataset = Dataset.objects.get(id=dataset_id, user=request.user)
    except Dataset.DoesNotExist:
        return Response({"error": "Dataset not found"}, status=404)

    df = pd.read_csv(dataset.file.path)

    visuals = {}
    for col in df.select_dtypes(include=['number']).columns[:3]:  # Limit to 3 columns
        plt.figure(figsize=(5, 4))
        sns.histplot(df[col].dropna(), kde=True)
        plt.title(f'Distribution of {col}')
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()
        plt.close()
        visuals[col] = f"data:image/png;base64,{image_base64}"

    return Response(visuals)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def train_model(request, dataset_id):
    try:
        dataset = Dataset.objects.get(id=dataset_id, user=request.user)
    except Dataset.DoesNotExist:
        return Response({"error": "Dataset not found"}, status=404)

    df = pd.read_csv(dataset.file.path)

    target = request.data.get('target')
    if target not in df.columns:
        return Response({"error": "Target column not found"}, status=400)

    X = df.drop(columns=[target])
    y = df[target]

    X = pd.get_dummies(X)
    y = y.astype('int') if y.dtypes == 'bool' else y

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    model = DecisionTreeClassifier()
    model.fit(X_train, y_train)

    acc = accuracy_score(y_test, model.predict(X_test))

    model_name = f"model_user{request.user.id}_dataset{dataset.id}.pkl"
    model_path = os.path.join(settings.MEDIA_ROOT, 'models', model_name)
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(model, model_path)

    from .models import TrainedModel
    trained = TrainedModel.objects.create(user=request.user, name=model_name, model_file=f"models/{model_name}")

    return Response({"model_id": trained.id, "accuracy": acc})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def predict_model(request, model_id):
    try:
        model_entry = TrainedModel.objects.get(id=model_id, user=request.user)
    except TrainedModel.DoesNotExist:
        return Response({"error": "Model not found"}, status=404)

    model = joblib.load(model_entry.model_file.path)
    input_data = request.data.get('input')

    if not isinstance(input_data, dict):
        return Response({"error": "Invalid input"}, status=400)

    df = pd.DataFrame([input_data])
    df = pd.get_dummies(df)

    prediction = model.predict(df)[0]
    return Response({"prediction": prediction})
