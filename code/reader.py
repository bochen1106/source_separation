# this code is not guaranteed

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
import threading
from time import sleep

import sys
print "#######################"
print "platform: " + sys.platform
print "#######################"

NORMAL_TYPE = "glob"    # either "glob" or "freq" or None
SEED = 999
DIM_FEAT = 129
NUM_FRAME = 626
BATCH_SIZE = 64
  
class Reader(threading.Thread):
    
    def __init__(self, filename_data, filename_info):
        
        threading.Thread.__init__(self)
        
        self.f = f = h5py.File(filename_data)
        self.info = info = pickle.load(open(filename_info, "r"))
        
        if NORMAL_TYPE == "glob":
            data_mean = np.array(f["mean_glob"])
            data_mean = data_mean[None, ...]
            data_std = np.array(f["std_glob"])
            data_std = data_std[None, ...]
        if NORMAL_TYPE == "freq":
            data_mean = np.array(f["mean_freq"])
            data_mean = np.array(f["std_freq"])
        
        self.rng = np.random.RandomState(seed=SEED)
        self.data_flow = range(len(info))
        self.rng.shuffle(self.data_flow)
        
        self.running = True
        self.data_buffer = None
        self.lock = threading.Lock()
        self.idx_flow = 0
        self.start()
        
    def reset(self):
        
        self.idx_flow = 0
        
    def run(self):
        
        dim_feat = DIM_FEAT
        num_frame = NUM_FRAME
        batch_size = BATCH_SIZE
        data_flow = self.data_flow
        
        while self.running:
            
            if self.data_buffer is None:
                
                if self.idx_flow + batch_size <= len(data_flow):
                    # we are still in this epoch
                    idx_batch = data_flow[self.idx_flow : self.idx_flow + batch_size]
                    self.idx_flow += batch_size
                    
                elif self.idx_flow < len(data_flow):
                    # approach to the end of this epoch
                    # take the rest data, shuffle the flow
                    print "finish the current epoch, take the rest data"
                    idx_batch = data_flow[self.idx_flow:]
                    self.rng.shufffle(data_flow)
                    self.idx_flow = 0
                    
                else:
                    # we are just at the end point of this epoch (all finished)
                    # shuffle the flow
                    print "finish the current epoch"
                    self.rng.shuffle(data_flow)
                    idx_batch = data_flow[0:batch_size]
                    self.idx_flow = batch_size
                
                data = np.zeros((batch_size, num_frame, dim_feat))
                label = np.zeros((batch_size, num_frame, dim_feat, 2))
                names = []
                
                idx_sample = 0  # the data index within each batch
                for idx in idx_batch:
                    name, [idx_start, length] = self.info[idx]
                    data_tmp = self.f["X"][idx_start: idx_start+length, ...]
                    label_tmp = self.f["Y"][idx_start: idx_start+length, ...]
                    data[idx_sample, ...] = data_tmp
                    label[idx_sample, ...] = label_tmp
                    names.append(name)
                    idx_sample += 1
                
                with self.lock:
                    self.data_buffer = data, label, names
                sleep(0.0001)

    def iterate_batch(self):
        
        while self.data_buffer is None:
            sleep(0.0001)
        
        data, label, names = self.data_buffer
        data = np.array(data, dtype=np.float32)
        label = np.array(label, dtype=np.float32)
        with self.lock:
            self.data_buffer = None
            
        return data, label, names
    
    def close(self):
        
        self.running = False
        self.join()
        self.f.close()
        
#%%
        
if __name__ == "__main__":
    
    if sys.platform in ["linux", "linux2"]: # on server
        path_data = "../../../data"
    if sys.platform == "darwin":    # on local mac
        path_data = "/Users/bochen/Desktop/data"
    
    path_set = os.path.join(path_data, "set_001")
    path_h5 = os.path.join(path_set, "h5")
    filename_data = os.path.join(path_h5, "test.h5")
    filename_info = os.path.join(path_h5, "test.pickle")

    reader = Reader(filename_data, filename_info)
    
    for i in range(5):
        
        data, label, names = reader.iterate_batch()
        print('%d-th batch' % (i+1))
        print data.shape
        print label.shape
        
    reader.close()
    
#%%
idx = 0
mag = data[idx, ...]
mask = label[idx, ...]
name = names[idx]
mag = mag.T
mask_1 = mask[:, :, 0].T
mask_2 = mask[:, :, 1].T
fig, ax = plt.subplots(3, 1)
ax[0].imshow(mag)
ax[1].imshow(mask_1)
ax[2].imshow(mask_2)


path_feat = os.path.join(path_set, "feat", "test")
filename_feat = os.path.join(path_feat, name) + ".h5"
f = h5py.File(filename_feat)
mag = np.array(f["mag"])
mask = np.array(f["mask"])
f.close()
mask_1 = mask[0, ...]
mask_2 = mask[1, ...]

fig, ax = plt.subplots(3, 1)
ax[0].imshow(mag)
ax[1].imshow(mask_1)
ax[2].imshow(mask_2)
 
    
    
    
    
    
    