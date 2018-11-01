
import os
import glob
import numpy as np
import json
import matplotlib.pyplot as plt
import random
import h5py
import cPickle as pickle
import librosa
import sys
import util
import sys
print "#######################"
print "platform: " + sys.platform
print "#######################"

SR = 8000
DUR = 5 # sec
random.seed(9999)
TH_ACTIVE=40

#%%
if sys.platform in ["linux", "linux2"]: # on server
    path_data = "../../../data"
if sys.platform == "darwin":    # on local mac
    path_data = "/Users/bochen/Desktop/data"
    
path_set = os.path.join(path_data, "set_001")
path_feat = os.path.join(path_set, "feat")
path_h5 = os.path.join(path_set, "h5")
if not os.path.exists(path_h5):
    os.makedirs(path_h5)

data_types = ["train", "valid", "test"]
#data_types = ["train"]

for data_type in data_types:
    print "##### %s #####" % data_type
    path_feat_cur = os.path.join(path_feat, data_type)
        
    filenames = glob.glob(path_feat_cur + "/*.h5")
    filenames.sort()
    
    X = []
    Y = []
    info = {}
    idx_start = 0
    
    for filename in filenames:
        name = os.path.basename(filename).split(".")[0]
        print name
        
        f = h5py.File(filename)
        mag = np.array(f["mag"])
        mask = np.array(f["mask"])
        f.close()
        
        mag = mag.T
        mask = np.swapaxes(mask, axis1=0, axis2=2)
        X.append(mag)
        Y.append(mask)
        info[name] = [idx_start, mag.shape[0]]
        idx_start += mag.shape[0]
        
    X = np.concatenate(X, axis=0)
    Y = np.concatenate(Y, axis=0)
    info = sorted(info.items())
    
    mean_freq = np.mean(X, axis=0)
    std_freq = np.std(X, axis=0)
    mean_glob = np.mean(X)
    std_glob = np.std(X)
    
    filename_h5 = os.path.join(path_h5, data_type) + ".h5"
    if os.path.exists(filename_h5):
        os.remove(filename_h5)
    f = h5py.File(filename_h5)
    f["X"] = X
    f["Y"] = Y
    f["mean_freq"] = mean_freq
    f["std_freq"] = std_freq
    f["mean_glob"] = mean_glob
    f["std_glob"] = std_glob
    f.close()
    
    filename_pickle = os.path.join(path_h5, data_type) + ".pickle"
    pickle.dump(info, open(filename_pickle, "w"))
    
    
    
        
        
        


