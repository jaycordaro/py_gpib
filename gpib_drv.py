# -*- coding: utf-8 -*-
"""
Created on Thu May 28 01:20:20 2020

@author: Jay Cordaro
based on a driver by 
https://github.com/astro313/gpib/blob/master/pygpib.py
"""

'''interact with the Prologix USB to GPIB Adapter
'''

import sys
import serial
import time
import numpy as np
import matplotlib.pyplot as plt

class Prologix(object):
    """
    GPIB communication over prologix USB adapter
    """
    def __init__(self, serial_dev='/dev/ttyUSB0',buffer_latency=0.2):
        """
        buffer_latency is the 'one size fits all'; whereas smaller buffer reads (e.g. :STAR) may allow shorter
        """
        try:
            self.ser = serial.Serial(port=serial_dev,
                                     baudrate=460800,
                                     parity=serial.PARITY_NONE,
                                     stopbits=serial.STOPBITS_ONE,
                                     bytesize=serial.EIGHTBITS,
                                     timeout=1)
            
            self.initialize_prologix(buffer_latency)
        
        except:
            raise RuntimeError("Error: Unable to Open Com Port" + serial_dev)
                


    def initialize_prologix(self,buffer_latency):
        """
        Issue a reset and put Prologix interface in control mode
        """
        print("Initializing Prologix USB-GPIB card")
        self.buffer_latency = buffer_latency
        self.cmd("++rst")  # POR of controller
        print("Waiting 5 sec after Prologix reset...")
        time.sleep(5)
        prologix = self.cmd("++ver")
        print(prologix)

        self.cmd("++mode 1")  # controller mode
        self.cmd("++auto 1")  # address instrument to TALK
        self.cmd("++savecfg 0") # disable setting config param in EEPROM

    def cmd(self,cmd_str,verbose=False):
        buff = self.get_buffer()   # check if anything in buffer before sending the command
        if len(buff)>0:    # got the stuff out of buffer
            print('Cleared buffer:  '+buff)   # cleared the junk

        self.write_buffer(cmd_str)
        buff = self.get_buffer()
        if verbose:
            print("sent: %s\nreply: %s" %(cmd_str, buff))
        buff = buff.strip()
        return buff

    def set_addr(self,addr):
        self.addr = addr
        self.write_buffer('++addr %d' % (self.addr))

    def write_buffer(self,cmd_str):
        cmd_str = cmd_str.strip()
        cmd_str2 = (cmd_str + "\n").encode()
        self.ser.write(cmd_str2)

    def get_buffer(self):

        time.sleep(self.buffer_latency)
        output = ''
        data_in_buffer = self.ser.inWaiting()
        while data_in_buffer:
            output += self.ser.read(data_in_buffer).decode('ascii')
            time.sleep(self.buffer_latency+2)
            data_in_buffer = self.ser.inWaiting()
        return output     
    
    def close(self):
        self.ser.close();
        return;
        

