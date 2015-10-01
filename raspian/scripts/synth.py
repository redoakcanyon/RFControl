#!/usr/bin/env python
################################################################################
#
# Module:   synth.py
# Location: C:\Python27\Lib\site-packages
# Edited:   D F
# Date:     8/21/2014
#
# Description:
#  Controls the TPI version 4 USB synthesizer
#  www.rf-tools4u.com
#  The unit is uses Analog Devices ADF4351 PLL synthesizer (frequency range is 35 to 4400 MHz with an RF output adjustable from -55 to +10 dBm. in 1 dB steps)
#
# Dependancies:
#    import subprocess
#    from subprocess import Popen, PIPE, STDOUT
#    import time
#    import telnetlib
#    import os
#    requires C:\Program Files (x86)\SynthMachine\RFControl.exe
#    
# Examples
#
# S1 is synthesizer one,  S2 is synthesizer two
#   import synth
#   S1= synth("AH01SZBD")
#   S2= synth("AH01SZEN")
#   within idle S2= synth.synth("AH01SZEN")
#   S1.syn_cmd("clkint")
#   S2.syn_cmd("setfreq 2200")
#   S1.syn_cmd("setfreq 2100")
#   S2.syn_cmd("setpwr -10")
#   S1.syn_cmd("setpwr -10")
#   S1.syn_cmd("rfon")
#   S1.syn_cmd("rfoff")
#   S1.syn_cmd("shutdown")
#   syn_close(self)
#    SG1.syn_frq_pwr(frq[0],-10)
#    SG2.syn_frq_pwr(frq[2],-10)
#    SG3.syn_frq_pwr(frq[4],-10)
#    SG4.syn_frq_pwr(frq[6],-10)
#    SG1.rfon()
#    SG2.rfon()
#    SG3.rfon()
#    SG4.rfon()
#  note: Invoke this class with the serial number of the synthesizer you have connected (assuming the key is on the list below)
#       issue S1.syn_cmd("cmd") where cmd is any valid synthesizer command
#
import subprocess
from subprocess import Popen, PIPE, STDOUT
import time
import telnetlib
import os
import pprint

class  synth():
    def __init__( self, sn ):
        self.ctrl = self.start_syn(sn)

    def start_syn(self, sn):
        key = self.key_list(sn)
        ## command to run - RFControl and the key for the unit serial number from the list ##
        cmd = ["C:\\\\Program Files (x86)\\\\Synthmachine\\\\RFControl.exe", key]
        print key
        p = subprocess.Popen(cmd, shell = True, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
        time.sleep(1)
        r= '';   out = ''
        while out <> '\r':
            out = p.stdout.read(1)
            if out == '' and p.poll() != None:
                #print out;
                break
            if out != '':
                r = r + out
        print r        
        port = r[16:-1]
        prt = port
        return port

    def key_list(self,sn):
        keys = {
                        "A701UWMF" : "26c115c578d90a7d",
                        "AH01SZA3" : "7f71add803916610",
                        "AH01SZBD" : "eb70d1369c45885b",
                        "AH01SZBM" : "1fb52643048d03fb",
                        "AH01SZBR" : "0936885f1eadb146",
                        "AH01SZC3" : "11fc1883898b54a9",
                        "AH01SZCG" : "7824ec9d3e97a08c",
                        "AH01SZD6" : "8cdaaed921384032",
                        "AH01SZE6" : "15211486768a17be",
                        "AH01SZED" : "95856a1f02a7fbf1",
                        "AH01SZEN" : "a12b2b157cd720f0",
                        "AH01SZGC" : "a8a41e59f6b877c4",
                        "AH009M6C" : "d95611bea1a4f6fc",  # D F pers key
                        "AH01SZDR" : "3dbbce8f0a2a5b56"   # D F pers key
                }
        key =  keys.get(sn)
        if sn == 'show' : pprint.pprint(keys)
        return key

    def read_prompt(self, port):
        global tn
        tn = telnetlib.Telnet('127.0.0.1',port)
        for p in xrange(1, 3, 1):
            line =  tn.read_until("RFControl Ready",0.3)
            print line
        return line
    
    def wrt_cmd(self, cmd):
        global tn
        tn.write(cmd + '\n')
        r = tn.read_until('\n',0.3)
        print r

    def syn_cmd(self, cmd):
         self.read_prompt(self.ctrl)
         self.wrt_cmd(cmd)

    def syn_close(self):
        os.system('taskkill /im ' + "RFControl.exe")
        
    def freq(self, f):
         self.read_prompt(self.ctrl)
         self.wrt_cmd("setfreq " + str(f))
         
    def dbm(self, dbm):
         self.read_prompt(self.ctrl)
         self.wrt_cmd("setpwr " + str(dbm))

    def syn_frq_pwr(self, f, dbm):
         self.read_prompt(self.ctrl)
         self.wrt_cmd("setpwr " + str(dbm))
         self.wrt_cmd("setfreq " + str(f))         

    def set_output_off(self):
         self.read_prompt(self.ctrl)
         self.wrt_cmd("rfoff")
         
    def set_output_on(self):
         self.read_prompt(self.ctrl)
         self.wrt_cmd("rfon")

    def rfoff(self):
         self.read_prompt(self.ctrl)
         self.wrt_cmd("rfoff")

    def rfon(self):
         self.read_prompt(self.ctrl)
         self.wrt_cmd("rfon")

    def clkint(self):
         self.read_prompt(self.ctrl)
         self.wrt_cmd("clkint")

    def pwr_swp(self, dbmin, dbmax, step, t):
         self.read_prompt(self.ctrl)
         self.wrt_cmd("stop scan")
         self.wrt_cmd("setpwrfrom " + str(dbmin))
         self.wrt_cmd("setpwrto " + str(dbmax))
         self.wrt_cmd("setpwrstep " + str(step))
         self.wrt_cmd("setpwrdelay " + str(t))         
         self.wrt_cmd("pwrscan")

    def pwr_swp_set(self, dbmin, dbmax, step, t):
         self.read_prompt(self.ctrl)
         self.wrt_cmd("stop scan")
         self.wrt_cmd("setpwrfrom " + str(dbmin))
         self.wrt_cmd("setpwrto " + str(dbmax))
         self.wrt_cmd("setpwrstep " + str(step))
         self.wrt_cmd("setpwrdelay " + str(t))         

    def stopscan(self):
         self.read_prompt(self.ctrl)
         self.wrt_cmd("stop scan")

    def startscan(self):
         self.read_prompt(self.ctrl)
         self.wrt_cmd("pwrscan")

    def init(self, f, dbm):
        self.read_prompt(self.ctrl)
        self.wrt_cmd("stop scan")
        self.wrt_cmd("clkint")
        self.syn_frq_pwr(f, dbm)
        self.pwr_swp_set(-9, -8, 1, 1)
        self.wrt_cmd("rfon")

    def show_sn(self):
        r =  self.key_list("show")

#S1= synth("AH01SZBD")
#S1.show_sn()