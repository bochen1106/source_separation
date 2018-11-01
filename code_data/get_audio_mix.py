
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
random.seed(9999)

#%%
#path_data = "/Users/bochen/Desktop/data"
path_data = "../../../data"
path_track = os.path.join(path_data, "audio_track")
path_seg = os.path.join(path_data, "audio_seg")
path_set = os.path.join(path_data, "set_002")
if not os.path.exists(path_set):
    os.makedirs(path_set)
path_mix = os.path.join(path_set, "audio")


#%% split set
print "split train/valid/test for the audio segments"

filenames = glob.glob(path_track + "/*.wav")
filenames.sort()
idx_valid = [0, 2, 15, 18]
idx_test = [1, 3, 12, 17]
idx_train = [x for x in range(len(filenames)) if x not in idx_valid+idx_test ]
id_train = ["trk%02d"%x for x in idx_train]
id_valid = ["trk%02d"%x for x in idx_valid]
id_test = ["trk%02d"%x for x in idx_test]

filenames = glob.glob(path_seg + "/*.wav")
names_train = []
names_valid = []
names_test = []
for filename in filenames:
    name = os.path.basename(filename).split(".")[0]
    id_trk = name.split("@")[1]
    if id_trk in id_train:
        names_train.append(name)
    if id_trk in id_valid:
        names_valid.append(name)
    if id_trk in id_test:
        names_test.append(name)
names_train.sort()
names_valid.sort()
names_test.sort()

filename = os.path.join(path_set, "names_train.txt")
fid = open(filename, "w")
fid.writelines(["%s\n" % x  for x in names_train])
fid.close()
filename = os.path.join(path_set, "names_valid.txt")
fid = open(filename, "w")
fid.writelines(["%s\n" % x  for x in names_valid])
fid.close()
filename = os.path.join(path_set, "names_test.txt")
fid = open(filename, "w")
fid.writelines(["%s\n" % x  for x in names_test])
fid.close()

#%%
print "generate audio mixtures"

n_sample = {}
n_sample["train"] = 2000
n_sample["valid"] = 500
n_sample["test"] = 500

for data_type in ["train", "valid", "test"]:
    print "##### %s #####" % data_type
    path_mix_cur = os.path.join(path_mix, data_type)
    if not os.path.exists(path_mix_cur):
        os.makedirs(path_mix_cur)
    
    filename = os.path.join(path_set, "names_"+data_type+".txt")
    names = [x.strip() for x in open(filename,"r").readlines()]
    names.sort()
    
    names_mix = []
    i_sample = 0
    while i_sample < n_sample[data_type]:
        tmp = random.sample(names, 2)
        tmp.sort()
        name1, name2 = tmp
        name_mix = name1.split("@")[0] + "-" + name2.split("@")[0]
        if name_mix in names_mix:
            continue
        else:
            names_mix.append(name_mix)
        name_out = "%06d" % i_sample + "@" + name_mix
        i_sample += 1
        
        filename1 = os.path.join(path_seg, name1) + ".wav"
        filename2 = os.path.join(path_seg, name2) + ".wav"
        filename_out = os.path.join(path_mix_cur, name_out) + ".wav"
        
        wav1, sr = librosa.core.load(filename1, SR)
        wav2, sr = librosa.core.load(filename2, SR)
        data = wav1 + wav2
        librosa.output.write_wav(filename_out, data, sr)


