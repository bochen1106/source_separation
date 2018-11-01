
import os
import glob
import numpy as np
import json
import matplotlib.pyplot as plt
import random

import librosa
import sys
import util


SR = 8000
DUR = 5 # sec
random.seed(9999)

#%%
path_data = "/Users/bochen/Desktop/data"
#path_data = "../../../data"
path_seg = os.path.join(path_data, "audio_seg")
path_set = os.path.join(path_data, "set_001")
path_audio = os.path.join(path_set, "audio")
path_feat = os.path.join(path_set, "feat")

for data_type in ["train", "valid", "test"]:
    print "##### %s #####" % data_type
    path_audio_cur = os.path.join(path_audio, data_type)
    path_feat_cur = os.path.join(path_feat, data_type)
    if not os.path.exists(path_feat_cur):
        os.makedirs(path_feat_cur)
        
    filenames = glob.glob(path_audio_cur + "/*.wav")
    for filename in filenames[:5]:
        name = os.path.basename(filename).split(".")[0]
        name1, name2 = name.split("@")[1].split("-")
        filename1 = glob.glob(os.path.join(path_seg, name1) + "*.wav")[0]        
        filename2 = glob.glob(os.path.join(path_seg, name2) + "*.wav")[0]
        
        
        