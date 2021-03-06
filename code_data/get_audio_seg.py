
import os
import glob
import numpy as np
import json
import matplotlib.pyplot as plt

import librosa
import sys
print "#######################"
print "platform: " + sys.platform
print "#######################"


SR = 8000
DUR = 5 # sec
#%%
if sys.platform in ["linux", "linux2"]: # on server
    path_data = "../../../data"
if sys.platform == "darwin":    # on local mac
    path_data = "/Users/bochen/Desktop/data"
 
path_track = os.path.join(path_data, "audio_track")
path_seg = os.path.join(path_data, "audio_seg")
if not os.path.exists(path_seg):
    os.makedirs(path_seg)

filenames = glob.glob(path_track + "/*.wav")
filenames.sort()

i_sample = 0
for filename in filenames:
    
    print filename
    name = os.path.basename(filename).split(".")[0]
    name_trk = name.split("@")[0]
    
    wav, sr = librosa.core.load(filename, SR)
    duration = len(wav) / sr
    n_seg = duration / DUR
    for j in range(n_seg):
        data = wav[j*DUR*sr : (j+1)*DUR*sr]
        name_dur = "%03d-%03d" % (j*DUR, (j+1)*DUR)
        name_out = "vn%04d"%i_sample + "@" + name_trk + "@" + name_dur
        i_sample += 1
        filename_out = os.path.join(path_seg, name_out) + ".wav"
        librosa.output.write_wav(filename_out, data, sr)

