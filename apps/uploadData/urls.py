# apps/uploadData/urls.py
from django.urls import path
from .views import UploadFileView, CreateTableView

urlpatterns = [
    path('', UploadFileView.as_view(), name='upload-file'),  # Ruta raíz para api/upload/
    path('create-table/', CreateTableView.as_view(), name='create-table'),
]
