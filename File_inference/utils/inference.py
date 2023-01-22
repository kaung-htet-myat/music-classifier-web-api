import os
import json
import numpy as np
import torch
import torch.nn as nn
import torchaudio.transforms as T


def get_device():
    return "cuda" if torch.cuda.is_available() else "cpu"


def get_label_map(label_path):
    with open(label_path, 'r', encoding='utf-8') as label_file:
        labels = json.load(label_file)
    reverse_labels = {v:k for k, v in labels.items()}

    return labels, reverse_labels


def load_model(model_path):

    if not os.path.exists(model_path):
        raise OSError("Specified model path does not exists.")

    model = torch.jit.load(model_path)
    model.eval()

    return model


def _preprocess(
        segment,
        in_rate,
        sample_length,
        sample_rate,
        fft_size,
        hop_length,
        n_mels
    ):

    waveform = segment[:in_rate*sample_length]
    waveform = torch.from_numpy(waveform)
    resampler = T.Resample(in_rate, sample_rate, dtype=waveform.dtype)
    waveform = resampler(waveform)
    resampled = nn.functional.pad(waveform, (0, sample_rate*sample_length - waveform.size()[-1]), 'constant', 0.0)

    mel_spectrogram = T.MelSpectrogram(
                                sample_rate=sample_rate,
                                n_fft=fft_size,
                                hop_length=hop_length,
                                n_mels=n_mels,
                                center=True,
                                pad_mode='reflect',
                                norm="slaney",
                                onesided=True,
                                mel_scale="htk"
                            )
    resampled = mel_spectrogram(resampled)
    resampled = resampled.unsqueeze(axis=0)

    amp_to_db = T.AmplitudeToDB()
    resampled = amp_to_db(resampled)

    return resampled.numpy()


def get_input_segments(
        sample,
        in_rate,
        sample_length,
        sample_rate,
        fft_size,
        hop_length,
        n_mels
    ):

    segments = []
    start = 0

    while start < len(sample):
        end = start + in_rate*sample_length
        try:
            segment = sample[start:end]
        except IndexError as e:
            segment = sample[start:]
        segments.append(segment)
        start = end

    np_segments = [
        _preprocess(
            segment,
            in_rate,
            sample_length,
            sample_rate,
            fft_size,
            hop_length,
            n_mels
        ) for segment in segments]
    np_segments = np.array(np_segments, dtype=np.float32)
    input_segments = torch.from_numpy(np_segments)

    return input_segments


def get_result(predictions, label_map):
    results = np.argmax(predictions.detach().numpy(), axis=-1)
    results = [label_map[res] for res in results]
    sorted_results = sorted(set(results), key=results.count, reverse=True)
    return sorted_results[0]