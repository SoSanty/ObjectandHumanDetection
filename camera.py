#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 09:55:10 2021

@author: esantisor23
"""
import cv2
import imutils

class RpiCam():
    
    def open_cam():
        vid = cv2.VideoCapture(0)
        return vid
    
    def cam_features(vid):
        img,frame = vid.read()
        frame = imutils.resize(frame,width=320)
        frame.framerate(15)  
        return frame
