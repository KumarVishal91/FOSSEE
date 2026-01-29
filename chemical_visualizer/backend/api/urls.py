from django.urls import path
from .views import UploadCSV, History

urlpatterns = [
    path('upload/', UploadCSV.as_view()),
    path('history/', History.as_view()),
]
