#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 09:57:45 2021

@author: esantisor23
"""
import socket
import cv2
import threading
from camera import RpiCam
from images_Rpi import ImagesRpi
from robot import RobotFeat

def main():
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 8200
    server_socket.bind(('192.168.1.100', port))
    server_socket.listen(3)
    
    # Socket Accept
    while True:
        client_socket,addr = server_socket.accept()
        print('GOT CONNECTION FROM:',addr)
        if client_socket:
            vid = RpiCam.open_cam()
            while(vid.isOpened()):
                
                RpiCam.cam_features() 
                ImagesRpi.sendall()
                ImagesRpi.message()
                
                key = cv2.waitKey(1) & 0xFF    
                if key ==ord('q'):
                    client_socket.close()
                    
if __name__ == '__main__':
    t = threading.Thread(target=RobotFeat.robotMOVE())
    t.start()
    main()
                
            