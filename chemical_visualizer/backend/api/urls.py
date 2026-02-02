from django.urls import path
from .views import DatasetDetail, DatasetReport, History, LatestDataset, UploadCSV

urlpatterns = [
    path('upload/', UploadCSV.as_view()),
    path('history/', History.as_view()),
    path('datasets/latest/', LatestDataset.as_view()),
    path('datasets/<int:pk>/', DatasetDetail.as_view()),
    path('report/<int:pk>/', DatasetReport.as_view()),
]
