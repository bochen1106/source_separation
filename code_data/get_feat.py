
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
path_single = os.path.join(path_data, "audio/single")
path_mix = os.path.join(path_data, "audio/set_001")

for data_type in ["train", "valid", "test"]:
    pass