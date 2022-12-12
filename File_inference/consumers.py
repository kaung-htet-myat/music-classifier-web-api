import os
import json
import random
import scipy
import librosa
import audiosegment
import soundfile as sf
from io import BytesIO
import base64
import numpy as np
import torch
import torchaudio
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings

from File_inference.utils.inference import (
    get_device,
    get_label_map,
    load_model,
    get_input_segments,
    get_result,
)


class PredictionConsumer(AsyncWebsocketConsumer):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.device = get_device()
        model_path = os.path.join(settings.MODEL_DIR, settings.MODEL_FILENAME)
        self.model = load_model(model_path)
        self.model.to(self.device)

        _, self.label_map = get_label_map(settings.LABEL_PATH)

        self.in_rate = 44100
        self.sample_length = settings.SAMPLE_LENGTH
        self.sample_rate = settings.SAMPLE_RATE
        self.fft_size = settings.FFT_SIZE
        self.hop_length = settings.HOP_LENGTH
        self.n_mels = settings.N_MELS

    async def connect(self):
        await self.accept()
            
    async def disconnect(self, close_code):
        pass

    async def predict(self, input):
        input_segments = get_input_segments(
                            input,
                            self.in_rate,
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
        return result

    async def process_input(self, bytes_data):

        f = BytesIO(bytes_data)
        s = torchaudio.io.StreamReader(f)
        s.add_basic_audio_stream(66150)
        input = torch.concat([chunk[0] for chunk in s.stream()])
        input = input.squeeze(-1).numpy()
        return input

    async def receive(self, bytes_data):
        try:
            input = await self.process_input(bytes_data)
            prediction = await self.predict(input)
            await self.send(text_data=json.dumps({"prediction": str(prediction)}))
        except RuntimeError as err: 
            print(err)