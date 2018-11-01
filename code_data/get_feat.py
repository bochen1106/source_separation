
import os
import glob
import numpy as np
import json
import matplotlib.pyplot as plt
import random
import h5py
import librosa
import sys
import util


SR = 8000
DUR = 5 # sec
random.seed(9999)
TH_ACTIVE=40

#%%
#path_data = "/Users/bochen/Desktop/data"
path_data = "../../../data"
path_seg = os.path.join(path_data, "audio_seg")
path_set = os.path.join(path_data, "set_001")
path_audio = os.path.join(path_set, "audio")
path_feat = os.path.join(path_set, "feat")

data_types = ["train", "valid", "test"]
#data_types = ["train"]

for data_type in data_types:
    print "##### %s #####" % data_type
    path_audio_cur = os.path.join(path_audio, data_type)
    path_feat_cur = os.path.join(path_feat, data_type)
    if not os.path.exists(path_feat_cur):
        os.makedirs(path_feat_cur)
        
    filenames = glob.glob(path_audio_cur + "/*.wav")
    filenames.sort()
    for filename in filenames:
        name = os.path.basename(filename).split(".")[0]
        print name
        name1, name2 = name.split("@")[1].split("-")
        filename1 = glob.glob(os.path.join(path_seg, name1) + "*.wav")[0]        
        filename2 = glob.glob(os.path.join(path_seg, name2) + "*.wav")[0]
        wav, sr = librosa.core.load(filename, SR)
        wav1, sr = librosa.core.load(filename1, SR)
        wav2, sr = librosa.core.load(filename2, SR)
        mag, pha, mask = util.cal_spec_mask(wav, wav1, wav2, th_active=TH_ACTIVE)
        
        filename_feat = os.path.join(path_feat_cur, name) + ".h5"
        f = h5py.File(filename_feat)
        f["mag"] = mag
        f["pha"] = pha
        f["mask"] = mask
        f.close()
        
        













