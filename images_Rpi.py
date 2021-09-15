#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 09:56:18 2021

@author: esantisor23
"""
import struct
import cv2
import pickle
from rpi_tasks import RpiTasks

class ImagesRpi():
    
    def sendall(frame,client_socket):
        
        a = pickle.dumps(frame)
        message = struct.pack("Q",len(a))+a
        client_socket.sendall(message)
        
        cv2.imshow('TRANSMITTING VIDEO',frame)
        
    def message(client_socket,t,frame):
        
        message = pickle.loads(client_socket.recv(4096))
        RpiTasks.encrypt(message)

        if message.count('0') > 1:
            t.do_run = False
            RpiTasks.humanDet(frame)
            
        elif message.count('0') == 1 :
            t.do_run = True
    
    