# -*- coding: utf-8 -*-
"""
Created on Thu May 28 01:20:20 2020

@author: Jay Cordaro
Control Tektronix 2521G power supply using Prologix GPIB Controller
"""
import sys
import math
import time
import threading

import gpib_drv

class tek2521g(object):
    def __init__(self, addr=8, serial_dev='/dev/ttyUSB0', buffer_latency=0.2):
        self.gpib = gpib_drv.Prologix(serial_dev,buffer_latency)
        self.addr = addr
        self.gpib.set_addr(addr)
        self.reset()
#        self.errors()
        time.sleep(3.5)

        try:
            self.name = self.gpib.cmd('*IDN?')  # get the ID
            self.gpib.cmd("++read eoi")
            if (self.name != "TEKTRONIX,PS2521G, ,SCPI:94.0 FW:.15"):
                self.fail("TEK 2521G Failure (" + self.name + ")")
            print(self.name + "\n")
        except:
            raise RuntimeError("Error Getting ID of Tek 2521G")
            self.ser.close()
            
    def clear_status(self):
        self.gpib.cmd("*CLS")
    
    def get_ese(self):
        """
        *ESE?

        Returns
        -------
        Returns the bits in the Event Status Enable Register

        """
            
        ese_status = self.gpib_cmd("*ESE?")
        self.gpib.cmd("++read eoi")
        return(ese_status)
    
    def set_ese(self, value=''):
        """
        Sets bits in the Event Status Enable Register
        specified by value, an 8-bit integer
        Returns
        -------
        None.

        """
        txt = "*ESE "
        txt += str(value) 
        txt += "\n"
        self.gpib.cmd(txt)
    
    def reset(self):
        self.gpib.cmd("*RST")
        self.gpib.cmd("*CLS")
        self.gpib.cmd("*SRE 0")
        
    def sys_test(self):
        """
        sys_test Tests RAM, ROM, DAC, and ADC components.

        Returns
        -------
        sys_stat :   0 == test passed
                  -300 == test failed
        """
        
        sys_stat = self.gpib.cmd("*TST?")
        self.gpib.cmd("++read eoi")
        return sys_stat
    
    def sel_output(self, output_no=1):
        """

        Parameters
        ----------
        output_no : int 
           Selects Output 1, Output 2, or Output3. An output must be selected
           before it can be configured and only one output may be selected at a
           time.

        Returns
        -------
        None.

        """
        if output_no in range(1,3):
            txt = "INST:NSEL "
            txt += str(output_no) 
            txt += "\n"
            self.gpib.cmd(txt)
        else:
            print("Error: Ouput must be 1, 2, or 3")
            
    def get_output(self):
        """
        
        """
        status = self.gpib.cmd("INST:SEL?")
        self.gpib.cmd("++read eoi")  
        return(status)
        
    def en_output(self, output_state=0):
        if output_state == 1:
            self.gpib.cmd("OUTP:STAT ON")
        else:
            self.gpib.cmd("OUTP:STAT OFF")
            
    def set_tracking_mode(self, mode='NONE'):
        """
        
        Parameters
        ----------
        mode : Sets tracking mode:
            NONE -- independent mode (default)
            PARallel is parallel-tracking mode
            SERies is series-tracking mode
        Returns
        -------
        None.

        """
        
        
    def meas_current(self):
        """
        Returns actual output current
        """
        
        current_meas = self.gpib.cmd("MEAS:SCAL:CURR?")
        self.gpib.cmd("++read eoi")  
        return current_meas
    
    def meas_voltage(self):
        """
        

        Returns
        -------
        Returns actual output voltage or sense input voltage.

        """
        self.voltage_meas = self.gpib.cmd("MEAS:SCAL:VOLT?")
        self.gpib.cmd("++read eoi")  
        return self.voltage_meas
    
    def set_voltage(self, voltage):
        # txt = "SOUR:VOLT:LEVEL:IMM:AMP "
        txt = "SOUR:VOLT "
        txt += str(voltage)
        self.gpib.cmd(txt)
    
    def set_current(self, current):
        # txt = "SOUR:VOLT:LEVEL:IMM:AMP "
        txt = "SOUR:CURR "
        txt += str(current)
        self.gpib.cmd(txt)
            
    def get_error(self):
        """
        get_error

        Returns
        -------
        err -- any system errors
           

        """
        self.err=self.gpib.cmd("SYSTem:ERRor?\n")
        self.gpib.cmd("++read eoi")      
        return self.err
    
    def set_volt_protect(self, vlevel=0, query = 1):
        if query == 1:
            txt ="SOUR:VOLT:PROT:LEV?"
            status=self.gpib.cmd(txt)
            self.gpib.cmd("++read eoi")
            return(status)
        else:
            txt ="SOUR:VOLT:PROT:LEV "
            txt += str(vlevel)
            self.gpib.cmd(txt)
        
        
    def set_curr_protect(self, clevel=0, query = 1):
        if query == 1:
            txt ="SOUR:CURR?"
            status=self.gpib.cmd(txt)
            self.gpib.cmd("++read eoi")
            return(status)
        else:
            txt ="SOUR:CURR "
            txt += str(clevel)
            self.gpib.cmd(txt)
            
    def clear_output_protection(self):
        """
        Clears output protection

        Returns
        -------
        None.

        """
        self.gpib.cmd("OUTP:PROT:CLE")
        
    def en_curr_protect(self, clevel, query =1):
        """
        Enables current protection

        Parameters
        ----------
        clevel : TYPE
            DESCRIPTION.
        query : TYPE, optional
            DESCRIPTION. The default is 1.

        Returns
        -------
        None.

        """
        txt = "CURR:PROT:STAT"
        if query == 1:
            txt+= "?"
            self.gpib.cmd(txt)
            self.gpib.cmd("++read eoi")
        else:
            txt+= " " + str(clevel)
            self.gpib.cmd(txt)
        
        
    def set_output(self, state):
        """
        

        Parameters
        ----------
        state : 0 = OFF
              : 1 = on
           The default is '0'.

        Returns
        -------
        None.

        """
        txt = "OUTP:STAT "
        txt += str(state)
        self.gpib.cmd(txt)
        
    def get_output_state(self):
        txt="OUTP:STAT?"
        output_state=self.gpib.cmd(txt)
        self.gpib.cmd("++read eoi")
        return(output_state)
            
#    def record_c_v(self):
    
    
        
