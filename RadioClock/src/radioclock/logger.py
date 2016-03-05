'''
Created on 09.02.2016

@author: hardy
'''
from datetime import datetime

logfile = None

def log(text):
    if not logfile == None:
        l = open(logfile,'a') 
        l.write(datetime.now().strftime('%Y.%m.%d %H:%M:%S') + ": " + text + '\n')
        l.close()
        
