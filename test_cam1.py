#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 13:14:30 2021

@author: esantisor23
"""

from camera import RpiCam
from yolo import loading
import os
import cv2


def test_file1():
    
   vid = RpiCam.open_cam() 
   assert vid.isOpened() == True
   
def test_file2():
    
    frame = RpiCam.cam_features()
    assert frame.width == 320
    assert frame.framerate == 15

def test_file3():
    
    assert os.path.isfile(loading.weightsPath) == True
    assert os.path.isfile(loading.configPath) == True

def test_file4():
    
    net = cv2.dnn.readNetFromDarknet(loading.configPath, loading.weightsPath)
    assert net.empty() == False