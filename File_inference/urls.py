from django.urls import path
from File_inference.views import IndexView, PredictView, HistoryView, StreamView

urlpatterns = [
    path('index/', IndexView.as_view(), name='file-index'),
    path('predict/', PredictView.as_view(), name='file-predict'),
    path('history/', HistoryView.as_view(), name='file-history'),
    path('stream/index', StreamView.as_view(), name='stream-index')
]