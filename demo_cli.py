import librosa
import numpy as np
from scipy.ndimage import binary_dilation
from encoder.params_data import *
from pathlib import Path
from typing import Union, Optional
from warnings import warn
import struct

try:
    import webrtcvad
except ImportError:
    warn("Unable to import 'webrtcvad'. This package enables noise removal and is highly recommended.")
    webrtcvad = None

int16_max = (2 ** 15) - 1

def preprocess_wav(fpath_or_wav: Union[str, Path, np.ndarray],
                   source_sr: Optional[int] = None,
                   normalize: Optional[bool] = True,
                   trim_silence: Optional[bool] = True) -> np.ndarray:
    """
    Preprocesses the waveform by loading it (if a path is provided), resampling to the target
    sample rate, optionally normalizing volume, and trimming silences.
    """
    if isinstance(fpath_or_wav, (str, Path)):
        wav, source_sr = librosa.load(str(fpath_or_wav), sr=None)  # Load with native sampling rate
    else:
        wav = fpath_or_wav

    if source_sr is not None and source_sr != sampling_rate:
        wav = librosa.resample(wav, orig_sr=source_sr, target_sr=sampling_rate)

    if normalize:
        wav = normalize_volume(wav, target_dBFS=audio_norm_target_dBFS, increase_only=True)

    if trim_silence:
        wav = trim_silences(wav)
        
    return wav


def trim_silences(wav):
    """
    Removes silent parts from the waveform based on energy thresholding.
    """
    energy = np.sum(wav ** 2, axis=0)
    threshold = np.max(energy) * 0.01  # Adjust the threshold as needed
    non_silent_indices = np.where(np.atleast_1d(energy) > threshold)[0]
    if non_silent_indices.size > 0:
        start_index = non_silent_indices[0]
        end_index = non_silent_indices[-1]
        return wav[start_index:end_index+1]
    else:
        return wav


def normalize_volume(wav, target_dBFS, increase_only=False, decrease_only=False):
    """
    Normalizes the volume of a waveform to a target decibel Full Scale (dBFS).
    Allows specification to only increase or decrease the volume.
    """
    rms = np.sqrt(np.mean(wav**2))
    desired_gain = 10 ** ((target_dBFS - 20 * np.log10(rms)) / 20)
    
    if (desired_gain < 1.0 and increase_only) or (desired_gain > 1.0 and decrease_only):
        return wav
    return wav * desired_gain


if __name__ == "__main__":
    # Path to the audio file
    audio_file_path = r'C:\Users\wyatt\CLONE\Real-Time-Voice-Cloning-GUI\Real-Time-Voice-Cloning\test.mp3'
    
    try:
        # Load the audio file
        audio_data, sampling_rate = librosa.load(audio_file_path, sr=None)

        # Preprocess the audio data
        preprocessed_audio = preprocess_wav(audio_data, source_sr=sampling_rate)

        # You can inspect the preprocessed audio data or perform further processing with it
        print("Shape of preprocessed audio:", preprocessed_audio.shape)
    except Exception as e:
        print("Error occurred:", e)
