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
from util import *
from reader import Reader
import func_model

#%%
import sys
print "#######################"
print "platform: " + sys.platform
print "#######################"


class Trainer(object):
    
    def __init__(self, config, logger):
        
        self.config = config
        self.logger = logger
        logger.log("================================================")
        logger.log("initialize the TRAINER")
        logger.log("================================================")
        
    def load_data(self):
        
        config = self.config
        logger = self.logger
        logger.log("load the data from h5 files")
        
        if sys.platform in ["linux", "linux2"]: # on server
            path_data = "../../../data"
        if sys.platform == "darwin":    # on local mac
            path_data = "/Users/bochen/Desktop/data"
            
        set_idx = config.get("set_idx")
        path_set = os.path.join(path_data, set_idx)
        path_h5 = os.path.join(path_set, "h5")
        
        filename_data = os.path.join(path_h5, "train.h5")
        filename_info = os.path.join(path_h5, "train.pickle")
        self.data_train = Reader(filename_data, filename_info, config=config)
        logger.log("finish loading train data from: " + filename_data)
        
        filename_data = os.path.join(path_h5, "valid.h5")
        filename_info = os.path.join(path_h5, "valid.pickle")
        self.data_valid = Reader(filename_data, filename_info, config=config)
        logger.log("finish loading valid data from: " + filename_data)
        
        filename_data = os.path.join(path_h5, "test.h5")
        filename_info = os.path.join(path_h5, "test.pickle")
        self.data_test = Reader(filename_data, filename_info, config=config)
        logger.log("finish loading test data from: " + filename_data)
        
    def build_model(self):
        
        config = self.config
        logger = self.logger
        logger.log("build the model")
        
        model = func_model.build_dpcl()
        logger.log("model summary:")
        model.summary()
        if hasattr("logger", "file"):
            model.summary(print_fn=lambda x: logger.file.write(x + '\n'))
            
        self.model = model
        logger.log("finish building the model")
        
        
        
#%%
from util.config import Config
from util.logger import Logger


if __name__ == "__main__":
    
    if len(sys.argv) > 1:
        exp_idx = sys.argv[1]  
    else:
        exp_idx = "001"
    
    filename_config = "../config/config_" + exp_idx + ".json"
        
    config = Config(filename_config)
    config.set("exp_idx", exp_idx)
    
    filename_log = os.path.join(config.get("path_exp"), exp_idx, "log.txt")
    logger = Logger(filename_log)
    
    t = Trainer(config, logger)
    t.build_model()

