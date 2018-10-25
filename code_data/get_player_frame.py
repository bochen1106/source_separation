
import os
import glob
import numpy as np
import json
import matplotlib.pyplot as plt

import cv2
import sys
sys.path.append("../../func")
import func_video

#%%
path_dataset = "/Users/bochen/Desktop/URMP"
path_dataset_video = os.path.join(path_dataset, "Dataset_video")
path_dataset_audio = os.path.join(path_dataset, "Dataset_audio_track")

path_data = "/Users/bochen/Desktop/data"
path_out = os.path.join(path_data, "video_player")
if not os.path.exists(path_out):
    os.makedirs(path_out)

filename_config = os.path.join(path_dataset, "config.json")
config = json.load(open(filename_config, "r"))
list_piece = config["list_piece"]
list_track = config["list_track"]
idx_tracks = config["idx_tracks"]
idx_vn = config["idx_vn"]

filename = "info/pos_player.txt"
pos_player = np.loadtxt(filename).astype("i")
filename = "info/offset_player.txt"
offset_player = np.loadtxt(filename).astype("i")

l = 100     # the size of the squared output video
#%%
for idx_track in idx_vn[20:21]:
        
    i_track = idx_track-1
    for i in range(44):
        if i_track+1 in idx_tracks[i]:
            i_piece = i
            break
    print "piece: %s" % list_piece[i_piece]
    print "track: %s" % list_track[i_track]
    #%%
    
    [x, y, a] = pos_player[i_track]
    
    name_piece = list_piece[i_piece]
    name_track = list_track[i_track]
    offset = offset_player[i_track]
    print "offset: %d" % offset
    filename_vid = os.path.join(path_dataset_video, name_piece) + ".mp4"
    filename_aud = os.path.join(path_dataset_audio, name_track) + ".wav"
    
    filename_out = os.path.join(path_out, name_track) + ".mp4"
    
    
    #filename_vid = "/Users/bochen/Desktop/URMP/Dataset_OpFls/ResultVideos/01_Jupiter_vn_vc.mp4"
    vid = cv2.VideoCapture(filename_vid)
    fps = vid.get(cv2.CAP_PROP_FPS)
    n_frame = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
    w = int( vid.get(cv2.CAP_PROP_FRAME_WIDTH) )
    h = int( vid.get(cv2.CAP_PROP_FRAME_HEIGHT) )
    
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    vid_out = cv2.VideoWriter(filename_out, fourcc, fps, (l, l))
    for fnum in range(offset):
        _ = vid.read()
    for fnum in range(n_frame-3-offset):
    #    print fnum
        if np.mod(fnum, 100) == 0:
            print "frame %d of %d" % (fnum, n_frame)
        _, img = vid.read()
        img_out = img[y:y+a, x:x+a, :]
        img_out = cv2.resize(img_out, (100,100))
        vid_out.write(img_out)
    vid_out.release()
    
    filename_tmp = filename_out[:-4] + "_silent.mp4"
    os.rename(filename_out, filename_tmp)
    func_video.add_audio_to_video(filename_tmp, filename_aud, filename_out)
    os.remove(filename_tmp)
    

