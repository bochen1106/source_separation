
import os
import glob
import numpy as np
import json
import matplotlib.pyplot as plt
import random

import librosa
import sys


SR = 8000
DUR = 5 # sec
#%%
path_data = "../../../data"
path_single = os.path.join(path_data, "audio/single")
path_mix = os.path.join(path_data, "audio/mix")
n_sample = {}
n_sample["train"] = 2000
n_sample["valid"] = 500
n_sample["test"] = 500

for data_type in ["train", "valid", "test"]:
    print "##### %s #####" % data_type
    path_single_cur = os.path.join(path_single, data_type)
    path_mix_cur = os.path.join(path_data, data_type)
    if not os.path.exists(path_mix_cur):
        os.makedirs(path_mix_cur)
    filenames = glob.glob(path_single_cur + "*.wav")
    filenames.sort()
    
    names_mix = []
    for i in range(n_sample[data_type]):
        
        filename1, filename2 = random.sample(filenames, 2).sort()
        name1 = filename1.split("@")[0]
        name2 = filename2.split("@")[0]
        name_mix = name1 + "@" + name2
        if name_mix in names_mix:
            continue
        else:
            names_mix.append(name_mix)
        
        name_out = "%06d" % i + "@" + name_mix
        filename_out = os.path.join(path_mix_cur, name_out) + ".wav"
        
        wav1, sr = librosa.core.load(filename1, SR)
        wav2, sr = librosa.core.load(filename2, SR)
        data = wav1 + wav2
        librosa.output.write_wav(filename_out, data, sr)
        
