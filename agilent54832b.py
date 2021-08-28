# -*- coding: utf-8 -*-
"""
Created on Thu May 28 01:20:20 2020

@author: Jay Cordaro
based on a driver by 
https://github.com/astro313/gpib/blob/master/pygpib.py
"""

class agilent54832b(object):
    """
    driver for Agilent 54832B Oscilloscope
    """
    
    def __init__(self, addr=18, serial_dev="COM6", buffer_latency=0.2):
        self.gpib = Prologix(serial_dev,buffer_latency)
        self.addr = addr
        self.gpib.set_addr(addr)
        self.reset()
        self.errors()
        time.sleep(3.5)
    
    def reset(self):
        