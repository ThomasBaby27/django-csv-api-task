from django.urls import path
from .views import UserUploadView

urlpatterns = [
    path('upload-csv/', UserUploadView.as_view(), name='user-upload'),
]