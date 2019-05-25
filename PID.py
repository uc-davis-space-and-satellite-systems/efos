##Referenced https://github.com/ivmech/ivPID/blob/master/PID.py and ht tps://en.wikipedia.org/wiki/PID_controller#Manual_tuning
import time
import matplotlib.pyplot as plt
class PID: 
    def __init__(self, current_yaw, set_yaw): ##P will need tuning, but a good starting point is 1 divided by the ‘encoder ticks per sample’ 
        self.clear()
        self.plotp = []
        self.ploti = []
        self.plotd = []
        self.value = current_yaw
        self.Kp = 0.1
        self.Ki = 0.0
        self.Kd = 0.025
        self.set = set_yaw##make this value about 75% of the ‘encoder ticks per sample’
        self.settime = 1.0 ## can change this to create larger or smaller intervals
        self.currenttime = time.time()
        self.lasttime = self.currenttime

        

    def clear(self): ##setting everything to zero..

        self.set = 0.0
        self.PTerm = 0.0
        self.ITerm = 0.0
        self.DTerm = 0.0
        self.preverror = 0.0
        self.int_error = 0.0
        #self.windup_guard = 10.0 ##subject to change based on what we  
        self.output = 0.0
    
    def update(self) : ##values from.. sun sensor.. reaction wheels... anything else? will have to modify this body of code to accomdate for more data points
        ##Insert PID calculation in order to visualize how PID is working in unison with hardware
        error = self.set - self.value
        self.currenttime = time.time()
        deltime = self.currenttime - self.lasttime #delta time!
        delerror = error - self.preverror #delta error!

        if deltime >= self.settime :
            self.PTerm = self.Kp * error
            # self.ITerm += error * deltime 
            # if (self.ITerm < -self.windup_guard):
            #     self.ITerm = -self.windup_guard
            # elif (self.ITerm > self.windup_guard):
            #     self.ITerm = self.windup_guard
            self.DTerm = 0.0
            if deltime > 0 :
                self.DTerm = delerror / deltime
            
            self.lasttime = self.currenttime
            self.preverror = error

            self.output = self.PTerm + (self.Ki * self.ITerm) + (self.Kd * self.DTerm)
        ###PLOTTING PID
        #p = self.plotp.append(self.PTerm)
        #i = self.ploti.append(self.ITerm)
        #d = self.plotd.append(self.DTerm)
        #plt.plot((p,i,d,self.output),self.currenttime)
        #plt.show
        return self.output

    ##def setKp(self, prop_gain) :
        ##self.Kp = prop_gain
    ##def setKi(self, int_gain) :
        ##self.Ki = int_gain 
    ##def setKd(self, der_gain) :
        ##self.Kd = der_gain
    #def setWindup(self, windup):
        """Integral windup, also known as integrator windup or reset windup,
        refers to the situation in a PID feedback controller where
        a large change in setpoint occurs (say a positive change)
        and the integral terms accumulates a significant error
        during the rise (windup), thus overshooting and continuing
        to increase as this accumulated error is unwound
        (offset by errors in the other direction).
        The specific problem is the excess overshooting.
        """
        #self.windup_guard = windup

    def setsampleTime(self, sample_time):
        self.sample_time = sample_time

##Find other samples of code to decide if this option is the best! Think about a wrapper code to tie all these functions together THURSDAY
##store values from each term into a list and write a function to graph these Values FRIDAY https://www.geeksforgeeks.org/graph-plotting-in-python-set-1/