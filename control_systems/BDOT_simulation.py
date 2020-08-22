import numpy as np
from numpy import linalg
import matplotlib.pyplot as plt
# When our magnitude of numbers goes past certain threshold we will arrive at inconclusive results

def Bdot_Alg(I,k,magnetic_field_vector,angular_velocity):

    neg_angular_velocity = -1.0 * angular_velocity
    bdot_vec = np.cross(neg_angular_velocity,magnetic_field_vector)
    mag_dipole = -1.0 * np.dot(k, bdot_vec)
    #if mag_dipole[0] > 2.0 or mag_dipole[1] > 2.0 or mag_dipole[2] > 2.0:
    #    mag_dipole[0] = 2.0
    #    mag_dipole[1] = 2.0
    #    mag_dipole[2] = 2.0
    control_torque = np.cross(mag_dipole,magnetic_field_vector)
    angular_accel = control_torque/I # this is our source of error right now! :")
    return angular_accel

### Set Our Simulation Values

time =np.arange(1.0,step=0.01)
angular_velocity = np.array([0.407281, 0.543041, 0.678795])    
magnetic_field_vector=np.array([3.0,4.0,5.0])
I = np.diag(np.array([0.33,0.37,0.35]))
xdata=[]
ydata=[]
zdata=[]


for i in time:
    angular_velocity = angular_velocity + i * Bdot_Alg(I=I,k=1.0,magnetic_field_vector=magnetic_field_vector,angular_velocity=angular_velocity)
    angular_velocity=np.around(angular_velocity, decimals = 4)
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


