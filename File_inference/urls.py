from django.urls import path
from File_inference.views import IndexView, PredictView, HistoryView

urlpatterns = [
    path('index/', IndexView.as_view(), name='file-index'),
    path('predict/', PredictView.as_view(), name='file-predict'),
    path('history/', HistoryView.as_view(), name='file-history'),
]