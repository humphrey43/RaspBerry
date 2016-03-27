'''
Created on 09.02.2016

@author: hardy
'''
from datetime import datetime

logfile = None
console = False

def log(text):
    if not logfile == None:
        l = open(logfile,'a') 
        logtext = datetime.now().strftime('%Y.%m.%d %H:%M:%S') + ": " + text
        l.write(logtext)
        if (logtext[-1] <> '\n'):
            l.write('\n')
        l.close()
        if console:
            print logtext
        
def logvalue(name, value):
    log(name + ": " + str(value))
       
