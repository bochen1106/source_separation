
import os
import glob
import numpy as np
import json
import matplotlib.pyplot as plt

import librosa
import sys
sys.path.append("../../func")
import func_video

SR = 8000
DUR = 5 # sec
#%%
path_data = "/Users/bochen/Desktop/data"
path_track = os.path.join(path_data, "audio_track")
path_single = os.path.join(path_data, "single")

filenames = glob.glob(path_track + "/*.wav")
filenames.sort()

idx_valid = [0, 2, 15, 18]
idx_test = [1, 3, 12, 17]
idx_train = [x for x in range(len(filenames)) if x not in idx_valid+idx_test ]
idx = {}
idx["train"] = idx_train
idx["valid"] = idx_valid
idx["test"] = idx_test


for data_type in ["train", "valid", "test"]:
    print "##### %s #####" % data_type
    path_cur = os.path.join(path_single, data_type)
    if not os.path.exists(path_cur):
        os.makedirs(path_cur)
    for i in idx[data_type]:
        filename = filenames[i]
        print filename
        name = os.path.basename(filename).split(".")[0]
        name_trk = name.split("@")[0]
        
        wav, sr = librosa.core.load(filename, SR)
        duration = len(wav) / sr
        n_seg = duration / DUR
        for j in range(n_seg):
            data = wav[j*DUR*sr : (j+1)*DUR*sr]
            name_dur = "%03d-%03d" % (j*DUR, (j+1)*DUR)
            name_out = "vn%04d"%j + name_trk + "@" + name_dur
            filename_out = os.path.join(path_cur, name_out) + ".wav"
            librosa.output.write_wav(filename_out, data, sr)
            
#%% get info
for data_type in ["train", "valid", "test"]:
    path_cur = os.path.join(path_single, data_type)
    filenames = glob.glob(path_cur + "/*.wav")
    print "sample number in %s set: \t%d" % ( data_type, len(filenames) )
    