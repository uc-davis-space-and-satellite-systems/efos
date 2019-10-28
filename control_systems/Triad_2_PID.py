##communicate between Triad and PID 
#utilized in fos
import triad
import PID from PID
import numpy as np

def correct(rotation,target):
    if rotation == 0 : ## TODO calculate range of values, 0 is too tight of an interval for power consumption 
        pass
    else:
        correction = np.array([0.0,0.0,0.0])
        correction[:,0]=PID.update(rotation[:,0])
        correction[:,1]=PID.update(rotation[:,1])
        correction[:,2]=PID.update(rotation[:,2])
    return correction

def clear():
    PID.clear()
    return 