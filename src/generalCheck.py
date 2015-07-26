import sys    
import os
import re    
    
import atexit    
import time    
import psutil    
    
#function of Get CPU State    
def getCPUstate(interval=30):    
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

#compute system cpu/mem    
def poll(interval):    
    """Retrieve raw stats within an interval window."""        
    # get cpu state    
    cpu_state = getCPUstate(interval)    
    # get memory    
    memory_state = getMemorystate()    
    return (cpu_state,memory_state)
    
#print current n(=5) seconds #cpu state #memory      
def getSysInfo(interval=5):
    #interval = 3    
    os.system("cls")    
    """Print stats on screen."""    
    try:    
        args = poll(interval)
    except (KeyboardInterrupt, SystemExit):    
        pass    
    #print current time #cpu state #memory    
    print(time.asctime()+" | "+args[0]+" | "+args[1]) 
    
#get a process information var pid       
def getProcessInfo(pid):   
    instance = []
    if not psutil.pid_exists(pid):
        return instance
    all_processes = list(psutil.process_iter())
    #search process and get information
    for proc in all_processes:
        if pid==proc.pid:
            #get cpu info
            cpu=proc.get_cpu_percent(interval=0)
            #get mem info 
            rss, vms = proc.get_memory_info()
            #get process name    
            name=proc.name                      
            instance=[ str(pid), str(rss), str(vms), str(cpu),name.upper()]
    return instance
   
#get some processes information var a namelist
def getProcessesInfo(namelist):
    print "PID\tRSSMEM\tVIRMEM\tCPU\tNAME"
    pids=[]
    pinfos=[]
    for name in namelist:
        #get several pids var a process name
        pids += pnameToPid(name)
        #get all processes information var pids
    for pid in pids:
        pinfo = getProcessInfo(int(pid))
        pinfos.append(pinfo)
    return pinfos

#get severl pids var a name  
def pnameToPid(name):  
    procs = psutil.get_process_list()  
    pid=0
    pids = []
    for p in procs:  
        pstr = str(p)  
        tmp = re.compile(name,re.I)  
        if tmp.search(pstr): 
            pid=pstr.split('pid=')[1].split(',')[0]
            if pid:
                pids.append(pid)
    if pid==0:
        print "NO SUCH PROCESS",name
    return pids

if __name__ == '__main__':
    namelist=['liebao','syn']
    pinfos=getProcessesInfo(namelist)
    for pinfo in pinfos:
        print "\t".join(pinfo)