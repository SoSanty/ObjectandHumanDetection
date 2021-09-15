#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 11:00:21 2021

@author: esantisor23
"""
import cv2
from robot import RobotFeat

class RpiTasks():
    
    def encrypt(message):

        if message[0] == '1':
            code = RobotFeat.CODE_DICT[message[2]]
        elif message[0] == '0':
            code = ''
        else:
            code = '..'
        RobotFeat.robot_beep(code)
    
    def humanDet(img):


        faceCascade = cv2.CascadeClassifier('/home/pi/opencv/data/haarcascades/haarcascade_frontalface_default.xml')
        img = cv2.flip(img, 1)
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        (H, W) = img.shape[:2]
        
        centerX = W // 2
        
        faces = faceCascade.detectMultiScale(
            gray,     
            scaleFactor=1.2,
            minNeighbors=5,     
            minSize=(20, 20)
        )
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            
        cv2.imshow('video',img)
        if len(faces) != 0:
            faceX = int(x + (w / 2.0))
            print(faceX)
            RobotFeat.robotMOVE2(centerX,faceX)