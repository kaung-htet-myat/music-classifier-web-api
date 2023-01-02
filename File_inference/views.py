import os
import librosa
from django.conf import settings
from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from rest_framework import views
from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer

from File_inference.models import FileInferenceModel
from File_inference.forms import UploadFileForm
from File_inference.utils.inference import (
    get_device,
    get_label_map,
    load_model,
    get_input_segments,
    get_result,
)


class IndexView(TemplateView):
    template_name: str = 'File_inference/index.html'


class PredictView(views.APIView):
    template_name = 'File_inference/result.html'
    renderer_classes = [TemplateHTMLRenderer]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.device = get_device()
        model_path = os.path.join(settings.MODEL_DIR, settings.MODEL_FILENAME)
        self.model = load_model(model_path)
        self.model.to(self.device)

        _, self.label_map = get_label_map(settings.LABEL_PATH)

        self.sample_length = settings.SAMPLE_LENGTH
        self.sample_rate = settings.SAMPLE_RATE
        self.fft_size = settings.FFT_SIZE
        self.hop_length = settings.HOP_LENGTH
        self.n_mels = settings.N_MELS
    
    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                sample, in_rate = librosa.load(request.FILES['song_file'], sr=None)

                input_segments = get_input_segments(
                                    sample,
                                    in_rate,
                                    self.sample_length,
                                    self.sample_rate,
                                    self.fft_size,
                                    self.hop_length,
                                    self.n_mels,
                                )
                input_segments = input_segments.to(self.device)

                predictions = self.model(input_segments)
                predictions = predictions.to('cpu')

                result = get_result(predictions, self.label_map)

                file_inference_obj = FileInferenceModel(
                                        file=request.FILES['song_file'],
                                        prediction=result
                                    )
                file_inference_obj.save()

                return Response({'prediction': result, 'file': request.FILES['song_file']}, status=status.HTTP_200_OK)
            except ValueError as err:
                return Response(str(err), status=status.HTTP_400_BAD_REQUEST)


class HistoryView(TemplateView):

    template_name = 'File_inference/history.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['inference_list'] = FileInferenceModel.objects.all()
        return context


class StreamView(TemplateView):
    template_name: str = 'File_inference/stream.html'