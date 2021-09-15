#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 09:56:06 2021

@author: esantisor23
"""
import time
import RPi.GPIO as GPIO
from AlphaBot2 import AlphaBot2
import threading
from beeps import Beeps


class RobotFeat():
    
    def __init__(self,Ab,BUZ,CODE_DICT):
        self.Ab = AlphaBot2()
        self.BUZ = 4
        self.CODE_DICT = {'0':'.','1':'-','2':'--','3':'---','4':'.--','5':'..-','6':'...','7':'-..','8':'--.','9':'.-','10':'-.'}

    def robot_beep(self, code):
        for i in code:
            if code[i] == '.':
                self.beep_on()
                time.sleep(0.25)
                Beeps.beep_off()
            elif code[i] == '-':
                self.beep_on()
                time.sleep(0.5)
                self.beep_off()
            elif code == '':
                self.beep_off()
    
    def beep_on(self):
        GPIO.output(self.BUZ,GPIO.HIGH)
        
    def beep_off(self):
        GPIO.output(self.BUZ,GPIO.LOW)
        
    def robotMOVE(self):
        
        t = threading.currentThread()
        t.do_run = True
        
        DR = 16
        DL = 19
        
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(DR,GPIO.IN,GPIO.PUD_UP)
        GPIO.setup(DL,GPIO.IN,GPIO.PUD_UP)
        GPIO.setup(self.BUZ,GPIO.OUT)
    
    
        while True:
            while getattr(t, "do_run", True):
                DR_status = GPIO.input(DR)
                DL_status = GPIO.input(DL)
                if((DL_status == 0)):
                    self.Ab.left()
                    time.sleep(0.002)
                    self.Ab.stop()
                
                elif((DR_status == 0)):
                    self.Ab.right()
                    time.sleep(0.002)
                    self.Ab.stop()
                
                else:
                    self.Ab.forward()
                    time.sleep(1)
                    self.Ab.left()
                    time.sleep(1)
                    self.Ab.right()
                    time.sleep(1)
                    self.Ab.stop()
            
            
            
    def robotMOVE2(self,centerX,faceX):
    
    
        if centerX > faceX:
            self.Ab.right()
            time.sleep(0.1)
            self.Ab.stop()
        elif centerX < faceX:
            self.Ab.left()
            time.sleep(0.1)
            self.Ab.stop()
            
