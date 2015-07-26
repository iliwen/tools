#    
# Copyright (c) 2014, Lambo Wang, All rights reserved.    
# Use of this source code is governed by a GNU v2 license that can be    
# found in the LICENSE file.    
#   
# Logs:  
# Transplant to NT system by Lambo Wang, 2012-11-28    
# Add function of get cpu state and get memory state by Lambo Wang,2012-11-29    
# first add to Git of OSChina,2014-10-24 by Lambo Wang   
"""  
Shows real-time NT system statistics.  
Author: Lambo Wang <lambo.wang@icloud.com>  
"""    
    
import sys    
import os    
    
import atexit    
import time    
import psutil    
    
#print "Welcome,current system is",os.name," 3 seconds late start to get data..."    
time.sleep(3)    
     
line_num = 1    
    
#function of Get CPU State    
def getCPUstate(interval=1):    
    return (" CPU: " + str(psutil.cpu_percent(interval)) + "%")    
#function of Get Memory    
def getMemorystate():    
    phymem = psutil.phymem_usage()    
    buffers = getattr(psutil, 'phymem_buffers', lambda: 0)()    
    cached = getattr(psutil, 'cached_phymem', lambda: 0)()    
    used = phymem.total - (phymem.free + buffers + cached)    
    line = " Memory: %5s%% %6s/%s" % (    
        phymem.percent,    
        str(int(used / 1024 / 1024)) + "M",    
        str(int(phymem.total / 1024 / 1024)) + "M"    
    )       
    return line    
def bytes2human(n):    
    """  
    >>> bytes2human(10000)  
    '9.8 K'  
    >>> bytes2human(100001221)  
    '95.4 M'  
    """    
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')    
    prefix = {}    
    for i, s in enumerate(symbols):    
        prefix[s] = 1 << (i+1)*10    
    for s in reversed(symbols):    
        if n >= prefix[s]:    
            value = float(n) / prefix[s]    
            return '%.2f %s' % (value, s)    
    return '%.2f B' % (n)    
    
    
def poll(interval):    
    """Retrieve raw stats within an interval window."""    
    tot_before = psutil.network_io_counters()    
    pnic_before = psutil.network_io_counters(pernic=True)    
    # sleep some time    
    time.sleep(interval)    
    tot_after = psutil.network_io_counters()    
    pnic_after = psutil.network_io_counters(pernic=True)    
    # get cpu state    
    cpu_state = getCPUstate(interval)    
    # get memory    
    memory_state = getMemorystate()    
    return (tot_before, tot_after, pnic_before, pnic_after,cpu_state,memory_state)    
    
def refresh_window(tot_before, tot_after, pnic_before, pnic_after,cpu_state,memory_state):    
    os.system("cls")    
    """Print stats on screen."""        
    #print current time #cpu state #memory    
    print(time.asctime()+" | "+cpu_state+" | "+memory_state)    
try:    
    interval = 2    
    #while 1:    
    args = poll(interval)    
    refresh_window(*args)  
        #interval = 1    
except (KeyboardInterrupt, SystemExit):    
    pass  