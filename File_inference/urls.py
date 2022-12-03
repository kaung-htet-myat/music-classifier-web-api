from django.urls import path
from File_inference.views import IndexView, PredictView

urlpatterns = [
    path('index/', IndexView.as_view()),
    path('predict/', PredictView.as_view()),
]