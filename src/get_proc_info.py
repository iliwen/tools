import psutil

import time  
  
import re  
  
import sys 
  

def getProcessInfo(pid):   
    #pid=int(pnameToPid(name))
    instances = []
    #if pid==0:
    #    return instances
    if not psutil.pid_exists(pid):
        return instances
    all_processes = list(psutil.process_iter())
    for proc in all_processes:
        if pid==proc.pid:
            cpu=proc.get_cpu_percent(interval=0) 
            rss, vms = proc.get_memory_info()    
            name=proc.name                      
            instance=[ str(pid), str(rss), str(vms), str(cpu),name.upper()]
            #print "\t".join(instance)
            instances.append(instance)
    return instances
   

def getProcessesInfo(namelist):
    print "PID\tRSSMEM\tVIRMEM\tCPU\tNAME"
    for name in namelist:
        pids = pnameToPid(name)
        if not pids:
            print "No Such Process!",name
            continue
        for pid in pids:
            infos = getProcessInfo(int(pid))
            for pinfo in infos:
                print "\t".join(pinfo)
  
def pnameToPid(name):  
    procs = psutil.get_process_list()  
    pid=0
    pids = []
    for p in procs:  
        pstr = str(p)  
        f = re.compile(name,re.I)  
        if f.search(pstr): 
            pid=pstr.split('pid=')[1].split(',')[0]
            pids.append(pid)
    return pids

if __name__ == '__main__':
    namelist=['360','ora_','eSpace','eclipse']
    getProcessesInfo(namelist)