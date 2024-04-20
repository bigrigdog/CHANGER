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

    if trim_silence and webrtcvad:
        wav = trim_long_silences(wav)

    return wav



import librosa
import numpy as np
from encoder.params_data import *

def wav_to_mel_spectrogram(wav, sampling_rate=22050, n_fft=2048, hop_length=512, n_mels=128, min_length=128):
    """
    Converts a waveform array into a mel spectrogram (non-logarithmic), ready to be used by
    the encoder for voice synthesis. Ensures a minimum width for the output spectrogram.
    """
    if len(wav) < hop_length:
        raise ValueError("Input waveform is too short for the specified hop_length.")

    # Ensure the waveform length is a multiple of hop_length to maintain consistency
    wav = wav[:len(wav) - (len(wav) % hop_length)]

    spectrogram = librosa.feature.melspectrogram(
        y=wav,
        sr=sampling_rate,
        n_fft=n_fft,
        hop_length=hop_length,
        n_mels=n_mels
    )

    # Pad the spectrogram to ensure it has at least `min_length` time steps
    padding_needed = max(0, min_length - spectrogram.shape[1])
    if padding_needed > 0:
        spectrogram = np.pad(spectrogram, ((0, 0), (0, padding_needed)), mode='constant')

    return np.asfortranarray(spectrogram.T, dtype=np.float32)



def trim_long_silences(wav):
    """
    Removes long silences from a waveform using Voice Activity Detection (VAD) with specified aggressiveness.
    """
    samples_per_window = (vad_window_length * sampling_rate) // 1000
    wav = wav[:len(wav) - (len(wav) % samples_per_window)]
    pcm_wave = struct.pack(f"{len(wav)}h", *(np.round(wav * int16_max).astype(np.int16)))

    vad = webrtcvad.Vad(3)  # High aggressiveness
    voice_flags = [vad.is_speech(pcm_wave[i * 2 * samples_per_window:(i + 1) * 2 * samples_per_window], 
                                 sample_rate=sampling_rate) for i in range(len(wav) // samples_per_window)]

    voice_flags = np.array(voice_flags, dtype=np.bool_)
    smoothed_voice_flags = binary_dilation(voice_flags, np.ones(vad_max_silence_length + 1))
    smoothed_voice_flags = np.repeat(smoothed_voice_flags, samples_per_window)

    return wav[smoothed_voice_flags[:len(wav)]]

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
