import os
import json
from io import BytesIO
import numpy as np
import torch
import torchaudio
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings

from File_inference.utils.inference import (
    get_device,
    get_label_map,
    load_model,
)


class PredictionConsumer(AsyncWebsocketConsumer):
    
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

    async def connect(self):
        await self.accept()
            
    async def disconnect(self, close_code):
        # await self.channel_layer.group_discard(
        #     self.room_group_name,
        #     self.channel_name
        # )
        pass

    async def process_input(self, bytes_data):
        f = BytesIO(bytes_data)
        print(f)
        s = torchaudio.io.StreamReader(f)
        s.add_basic_audio_stream(132300)
        input = torch.concat([chunk[0] for chunk in s.stream()])
        
        print(input)

    async def receive(self, bytes_data):
        print(type(bytes_data))
        print(len(bytes_data))
        
        try:
            await self.process_input(bytes_data)
        except RuntimeError as err:
            print(err)

        prediction = "metal"
        self.send(text_data=json.dumps({"prediction": prediction}))