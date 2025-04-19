from django.db import models
import os
from django.db import models
from django.contrib.auth.models import User

class UploadedDataset(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='datasets/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

def model_upload_path(instance, filename):
    return os.path.join('models', f'user_{instance.user.id}', filename)

class MLModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dataset = models.ForeignKey('UploadedDataset', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    version = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to=model_upload_path)

    class Meta:
        unique_together = ('user', 'name', 'version')