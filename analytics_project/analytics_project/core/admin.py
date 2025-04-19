from django.contrib import admin
from .models import Dataset, TrainedModel

# Dataset Admin
class DatasetAdmin(admin.ModelAdmin):
    list_display = ('user', 'file', 'uploaded_at')
    search_fields = ('user__username', 'file')
    list_filter = ('user', 'uploaded_at')

# TrainedModel Admin
class TrainedModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'model_type', 'created_at', 'dataset')
    search_fields = ('user__username', 'name', 'model_type')
    list_filter = ('user', 'model_type', 'created_at')

# Register your models here
admin.site.register(Dataset, DatasetAdmin)
admin.site.register(TrainedModel, TrainedModelAdmin)