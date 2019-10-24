##communicate between Triad and PID 
#utilized in fos
import triad
import PID

def main(rotation):
    correction = np.array([0.0,0.0,0.0])
    correction[:,0]=PID(rotation[:,0])
    correction[:,1]=PID(rotation[:,1])
    correction[:,2]=PID(rotation[:,2])
    return correction
