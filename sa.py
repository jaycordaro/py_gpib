# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 08:53:33 2020

@author: Joseph
"""

class sa(object):
    """
    HP8594E Spectrum analyzer
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

        self.scpi = {'start' : ['FA','MHz',float],
                     'stop'  : ['FB','MHz',float],
                     'center': ['CF','MHz',float],
                     'span'  : ['SP','MHz',float],
                     'pts'   : [':SENS:SWE:POIN',None,int],
                     'att'   : [':SENS:POW:RF:ATT',None,float],
                     'rbw'   : [':SENS:BWID:RES','kHz',float],
                     'vbw'   : [':SENS:BWID:VID','kHz',float]
            }


    def reset(self):
        self.gpib.cmd("IP")
    
    def errors(self):
        r = False
        while True: 
            x = self.gpib.cmd("ERR")
            if (x == "0,0,0,0"):
                break
            print("Error: " + x + "\n")
            r = True
        return r
    
    def set_sa(self, start_freq, stop_freq, points, rbw, vbw):
        
       
        
    def set_sa_cf(self, center_freq, span_freq, points, rbw, vbw):
        s = "CF "
        s += center_freq
        self.gpib.cmd(s)
        
        s = "SP "
        s += span_freq
        self.gpib.cmd(s)
        
    def set_ref_lvl(self, ref_lvl):
		s = "RL "
		s += ref_lvl
		self.gpib.cmd(s)
	
	def get_ref_lvl(self):
	    s = "RL?"
		ref_lvl = self.gpib.cmd(s)
		return(ref_lvl)
		
    def get_sa(self):
        x=self.gpib.cmd("FB?")
        
        
            
    def spec(self,unit='MHz',plot=True):

        a = self.gpib.cmd(':TRAC:DATA? TRACE1')
        start = self.gpib.cmd(':SENS:FREQ:START?')
        try:
            start = float(start)/units[unit]
        except ValueError:
            print('Error in start: '+start)
        stop = self.gpib.cmd(':SENS:FREQ:STOP?')
        try:
            stop = float(stop)/units[unit]
        except ValueError:
            print('Error in stop:  '+stop )

        pts = self.gpib.cmd(':SENS:SWE:POIN?')
        try:
            pts = int(pts)
        except ValueError:
            print('Error in pts:  '+pts)
            pts = 1
        step = (stop - start)/ pts   # resolution
        print('%f - %f %s (%d points)' % (start,stop,unit,pts) )
        b = a.split(',')
        spec = []
        for i,s in enumerate(b):
            freq = start + i*step
            spec.append([freq,float(s)])
        spec = np.array(spec)    # 2 cols 
        if plot:
            plt.plot(spec[:,0],spec[:,1])
            plt.xlabel('Freq [MHz]')
            plt.ylabel('dB')
            plt.show()
        return spec


    def getv(self,par,unit=None):
        s = self.gpib.cmd(self.scpi[par][0]+'?')    # scpi query of that 'par'
        if unit is None:
            unit = self.scpi[par][1]
        global sa
        
        try:
            sa = self.scpi[par][2](s)      
        except ValueError:
            print('Error reading '+par+':  '+s) 
        if unit is not None:
            sa = sa/units[unit]
        return sa, unit


    def setv(self,par,value,unit=None):
        svalue = str(value)
        if unit is None:
            unit = self.scpi[par][1]
        if unit is not None:
            scpi = '%s %s %s' % (self.scpi[par][0],svalue,unit)
        else:
            scpi = '%s %s' % (self.scpi[par][0],svalue)
        s = self.gpib.cmd(scpi)   # output from sending the scpi
        sa = self.getv(par,unit=unit)   # confirm scpi command interacted with instrument
        if value is float or value is int:
            if abs(sa[0] - value)/value > 0.02:
                print('Mismatch between set %s (%f) and sa %s (%f)' % (par,value,par,sa))
        return sa


def saveresult(sa_class, start_fq, stop_fq, unit_fq, atten, pts, rbw, unit_rbw):

    sa_class.setv('start', start_fq, unit_fq)
    sa_class.setv('stop', stop_fq, unit_fq)

    spec_start.setv('att', atten)
    spec_start.setv('pts', pts)
    spec_start.setv('rbw', rbw, unit_rbw)
    result_trace = sa_class.spec(plot=False)

    from datetime import datetime
    hdr = 'start_fq: %s %s, stop_fq: %s %s, \nattenuation: %s, number of points: %s, \nbandwidth resolution: %s %s, \n%s, \nFrequency [%s], dB' \
        %(str(start_fq), unit_fq, str(stop_fq), unit_fq, str(atten), str(pts), str(rbw), unit_rbw, str(datetime.now()), unit_fq) 

    foname = 'Trace%s%s-%s.csv' %(str(start_fq), str(stop_fq), str(datetime.now().time())[:5])
    np.savetxt(foname, result_trace, delimiter=',', header=hdr)
    print('---Saved %s.----' %foname)
    

#========================================================
if __name__ == '__main__':
    spec_start = sa()
    freq_dict = {'range1': [100, 200, 'MHz'],
                    'range2': [120, 130, 'MHz'],
                    'range3': [155, 160, 'MHz'],
                    'range4': [165, 175, 'MHz']
                    }
    atten = 20
    pts = 801
    rbw = 100
    unit_rbw = 'kHz'
    
    saveresult(spec_start, freq_dict['range1'][0], \
                freq_dict['range1'][1], freq_dict['range1'][2], atten, pts, rbw, unit_rbw)
#        saveresult(spec_start, freq_dict['range2'][0], \
#            freq_dict['range2'][1], freq_dict['range2'][2], atten, pts, rbw, unit_rbw)
#        saveresult(spec_start, freq_dict['range3'][0], \
#            freq_dict['range3'][1], freq_dict['range3'][2], atten, pts, rbw, unit_rbw)
#        saveresult(spec_start, freq_dict['range4'][0], \
#            freq_dict['range4'][1], freq_dict['range4'][2], atten, pts, rbw, unit_rbw)
#        time.sleep(300)
