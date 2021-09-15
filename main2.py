#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 11:38:50 2021

@author: esantisor23
"""
import argparse
import socket
import struct
from yolo import YoloFeat

def main():
    # Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
    # all interfaces)    
    client_socket = socket.socket()
    client_socket.connect(('192.168.1.100',8200)) # a tuple
    data = b""
    payload_size = struct.calcsize("Q")
    
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--confidence", type=float, default=0.5,
    	help="minimum probability to filter weak detections")
    ap.add_argument("-t", "--threshold", type=float, default=0.3,
    	help="threshold when applyong non-maxima suppression")
    args = vars(ap.parse_args())

    YoloFeat.loading()
    YoloFeat.layers(client_socket,data,payload_size,args)
    
    client_socket.close()
    
if __name__ == '__main__':
 main()  
