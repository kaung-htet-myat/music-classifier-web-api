from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework import views
from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer

from File_inference.forms import UploadFileForm


class IndexView(TemplateView):
    template_name: str = 'File_inference/index.html'


class PredictView(views.APIView):
    template_name = 'File_inference/result.html'
    renderer_classes = [TemplateHTMLRenderer]
    
    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                return Response({'prediction': "Rock", 'file': request.FILES['song_file']}, status=status.HTTP_200_OK)
            except ValueError as err:
                return Response(str(err), status=status.HTTP_400_BAD_REQUEST)