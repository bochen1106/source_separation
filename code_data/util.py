
import os
import glob
import numpy as np
import json
import matplotlib.pyplot as plt
import random

import librosa
import sys

SR = 8000
FRAME_LEN = 0.032
FRAME_HOP = 0.008
N_FFT = 256
DIM_FEAT = 129
TH_ACTIVE = 40

#%%

def cal_spec_mask(y, y1, y2):
    
    spec = librosa.core.stft(y=y, n_fft=N_FFT,
                             hop_length=int(np.floor(FRAME_HOP * SR)),
                             win_length=int(np.floor(FRAME_LEN * SR)),
                             window=np.sqrt(np.hanning(N_FFT)), center='True', pad_mode='constant')

    spec1 = librosa.core.stft(y=y1, n_fft=N_FFT,
                             hop_length=int(np.floor(FRAME_HOP * SR)),
                             win_length=int(np.floor(FRAME_LEN * SR)),
                             window=np.sqrt(np.hanning(N_FFT)), center='True', pad_mode='constant')

    spec2 = librosa.core.stft(y=y2, n_fft=N_FFT,
                             hop_length=int(np.floor(FRAME_HOP * SR)),
                             win_length=int(np.floor(FRAME_LEN * SR)),
                             window=np.sqrt(np.hanning(N_FFT)), center='True', pad_mode='constant')

    mag, pha = librosa.core.magphase(spec)
    mag1, pha2 = librosa.core.magphase(spec1)
    mag2, pha2 = librosa.core.magphase(spec2)
    
    # We don't use 'top_db' here since we will
    # mask out the silent parts later
    mag = librosa.core.amplitude_to_db(S=mag, ref=1, amin=1e-10, top_db=None)
    mag1 = librosa.core.amplitude_to_db(S=mag1, ref=1, amin=1e-10, top_db=None)
    mag2 = librosa.core.amplitude_to_db(S=mag2, ref=1, amin=1e-10, top_db=None)
    
    mask = [(mag1 >= mag2), (mag1 < mag2)]
    mask_active = mag >= (mag.max() - TH_ACTIVE)
    mask = mask_active[None, ...] * mask
    
    return mag, pha, mask
