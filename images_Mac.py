#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 10:06:44 2021

@author: esantisor23
"""

import struct
import pickle

class RecvImg():
    
    def receiving(data,payload_size,client_socket):
        
        while len(data) < payload_size:
            packet = client_socket.recv(4*1024) # 4K
            if not packet: break
            data+=packet
        packed_msg_size = data[:payload_size] 
        data = data[payload_size:] 
        msg_size = struct.unpack("Q",packed_msg_size)[0] 
        
        while len(data) < msg_size: 
            data += client_socket.recv(4*1024) 
        frame_data = data[:msg_size] 
        data  = data[msg_size:] 
        frame = pickle.loads(frame_data)
        return frame