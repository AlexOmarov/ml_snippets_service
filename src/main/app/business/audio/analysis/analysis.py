#  Lib imports
import librosa
import librosa.display
import matplotlib.patches as mpatches
import numpy as np
from matplotlib import pyplot as plt
from numpy import ndarray
from werkzeug.datastructures import FileStorage

#  App imports
from business.util.ml_logger import logger
from presentation.api.audio_analysis_result import AudioAnalysisResult
from src.main.resource.config import Config

_log = logger.get_logger(__name__.replace('__', '\''))


def analyse(storage: FileStorage, frame_length: int, hop_length: int) -> AudioAnalysisResult:
    return AudioAnalysisResult(_extract_features(storage, frame_length, hop_length), frame_length, hop_length)


def _extract_features(storage: FileStorage, frame_length: int, hop_length: int) -> str:
    audio, sr = librosa.load(storage)

    ae = _get_amplitude_envelope(audio, frame_length, hop_length)
    zcr = _get_zcr(audio, frame_length, hop_length)
    rms = _get_rms(audio, frame_length=frame_length, hop_length=hop_length)

    return _build_plot(audio, ae, zcr, rms, storage.filename, sr, hop_length)


def _get_amplitude_envelope(signal, frame_length: int, hop_length: int) -> ndarray:
    result = []
    for i in range(0, len(signal), hop_length):
        current_ae = max(signal[i:i + frame_length])
        result.append(current_ae)
    return np.array(result)


def _get_zcr(audio, frame_length, hop_length):
    return librosa.feature.zero_crossing_rate(audio, frame_length=frame_length, hop_length=hop_length)[0]


def _get_rms(signal, frame_length, hop_length) -> ndarray:
    result = []
    for i in range(0, len(signal), hop_length):
        current_rms = np.sqrt(np.sum(signal[i:i + frame_length] ** 2) / frame_length)
        result.append(current_rms)
    return np.array(result)


def _build_plot(signal, ae, zcr, rms, filename: str, sr: int, hop_length: int) -> str:
    path = Config.MODEL_PATH + filename + '_features.png'
    frames = range(0, ae.size)
    t = librosa.frames_to_time(frames, hop_length=hop_length)
    plt.figure(figsize=(15, 17))

    plt.subplot(3, 1, 1)

    red_patch = mpatches.Patch(color='red', label='Amplitude envelope')
    blue_patch = mpatches.Patch(color='blue', label='Waveform')
    green_patch = mpatches.Patch(color='green', label='RMS energy')
    yellow_patch = mpatches.Patch(color='yellow', label='Zero crossing rate')
    plt.legend(handles=[red_patch, blue_patch, green_patch, yellow_patch], fontsize=10, shadow=True, framealpha=0.5,
               edgecolor='b',
               title='Legend')

    librosa.display.waveshow(signal, sr=sr, alpha=0.5)
    plt.plot(t, ae, color="r")
    plt.plot(t, rms, color="g")
    plt.plot(t, zcr, color="y")
    plt.title(filename)
    plt.ylim((-1, 1))
    plt.savefig(path)
    return path