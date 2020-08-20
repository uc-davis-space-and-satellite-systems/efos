import numpy as np
from numpy import linalg
import matplotlib.pyplot as plt

def Bdot_Alg(I,k,magnetic_field_vector,angular_velocity):
    neg_angular_velocity = -1 * angular_velocity
    bdot_vec = np.cross(neg_angular_velocity,magnetic_field_vector)
    mag_dipole = -1.0 * k * bdot_vec
    if mag_dipole[0] > 2.0 or mag_dipole[1] > 2.0 or mag_dipole[2] > 2.0:
        mag_dipole[0] = 2.0
        mag_dipole[1] = 2.0
        mag_dipole[2] = 2.0
    control_torque = np.cross(mag_dipole,magnetic_field_vector)
    angular_accel = np.dot(np.linalg.inv(I), control_torque)
    return angular_accel

### Set Our Simulation Values

time =np.arange(1,step=0.001)
angular_velocity = np.array([0.604,0.760,0.684])    
magnetic_field_vector=np.array([1.0,1.0,1.0])
I = np.diag(np.array([0.33,0.37,0.35]))

xdata=[]
ydata=[]
zdata=[]

for i in time:
    angular_velocity = angular_velocity + i * Bdot_Alg(I=I,k=0.01,magnetic_field_vector=magnetic_field_vector,angular_velocity=angular_velocity)
    print(angular_velocity)
    xdata.append(angular_velocity[0])
    ydata.append(angular_velocity[1])
    zdata.append(angular_velocity[2])
    #if angular_velocity[0] <= 0 or angular_velocity[1] <= 0 or angular_velocity[2] <= 0: ## utilize mag instead of looking for 0 threshold 
        #break

# Graph of Simulation

fig,ax = plt.subplots(3)
fig.suptitle('lets get this shit to 0')
ax[0].plot(time,xdata)
ax[1].plot(time,ydata)
ax[2].plot(time,zdata)



plt.savefig("bdot_test1.png")


