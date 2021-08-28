# -*- coding: utf-8 -*-
"""
Created on Thu May 28 01:20:20 2020

@author: Jay Cordaro
based on a driver by 
https://github.com/astro313/gpib/blob/master/pygpib.py
"""

class hp53110a(object):
    """
    HP 53310A Modulation Domain Analyzer Driver
    """
     def __init__(self, addr=18, serial_dev="COM6", buffer_latency=0.2):

        self.gpib = Prologix(serial_dev,buffer_latency)
        self.addr = addr
        self.gpib.set_addr(addr)
        self.reset()
        self.errors()
        time.sleep(3.5)

        self.name = self.gpib.cmd('ID')  # get the ID
        if (self.name != "HP8591E"):
			self.fail("HP8591E ID failure (" + self.name + ")")
        print(self.name + "\n")
        
    def reset(self):
        self.gpib.cmd("*RST")
        self.gpib.cmd("*CLS")
        self.gpib.cmd("*SRE 0")
        
    def autoscale(self):
        self.gpib.cmd("CONF:XTIM:FREQ")
        
    def grab_timedat(self):
        self.gpib.cmd("INIT")
        self.gpib.cmd("*WAI")
        freq_dim_scale = self.gpib.cmd("DIM:SCAL?")
        freq_offset = self.gpib.cmd("DIM:OFFS?")
        time_dim_scale = self.gpib.cmd("DIM2:SCAL?")
        time_offset = self.gpib.cmd("DIM2:OFFS?")
        
        a = self.gpib.cmd("FETC:XTIM:FREQ?")
        
        
        