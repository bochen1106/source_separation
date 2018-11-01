
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
import sys
print "#######################"
print "platform: " + sys.platform
print "#######################"

NORMAL_TYPE = "glob"    # either "glob" or "freq" or None
SEED = 999
DIM_FEAT = 129
NUM_FRAME = 646
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
        self.index_start = 0
        self.start()
        
    def reset(self):
        
        self.index_start = 0
        
    def run(self):
        
        dim_feat = DIM_FEAT
        num_frame = NUM_FRAME
        batch_size = BATCH_SIZE
        data_flow = self.data_flow
        
        while self.running:
            
            if self.data_buffer is None:
                
                if self.index_start + batch_size <= len(data_flow):
                    batch_index = data_flow[self.index_start : self.index_start + batch_size]
                    self.index_start += batch_size
                    
                elif self.index_start < len(data_flow):
                    batch_index = data_flow[self.index_start:]
                    self.rng.shufffle(data_flow)
                    self.index_start = 0
                    
                else:
                    
                    self.rng.shuffle(data_flow)
                    batch_index = data_flow[0:batch_size]
                    self.index_start = batch_size
                
                data = np.zeros((batch_size, num_frame, dim_feat))
                label = np.zeros((batch_size, num_frame, dim_feat, 2))
                names = []
                
                index_sample = 0
                for idx in batch_index:
                    name, [idx_start, idx_end] = self.info[idx]
                    data_tmp = self.f['X'][index_start: index_start+, ...]
                
            
        
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
    
    reader = Reader(filename_info, filename_info)
    