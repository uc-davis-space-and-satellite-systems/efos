import pyIGRF, math, datetime
import numpy as np

class IGRF_Reference:

    def __init__(self):
        self.latitude = 0
        self.longitude = 0
        self.altitude = 0
        
    #set current latitude
    def set_latitude(self, new_latitude):
        self.latitude = new_latitude

    #set current longitude
    def set_longitude(self, new_longitude):
        self.longitude = new_longitude
    
    #set current altitude
    def set_altitude(self,new_altitude):
        self.altitude = new_altitude

    #converts a datetime to a decimal date
    def decimal_date(self, d):
        return (float(d.strftime("%j"))-1) / 366 + float(d.strftime("%Y"))

    #get julian date
    def jd_2000(self):
        jd = (datetime.datetime.now() - datetime.datetime(2000,1,1,12,0,0)).total_seconds() / 86400.0;
        return jd

    #get angle in radians for measure of Earth's rotation
    def get_angle(self):
        return 4.89496121274+(6.30038809899*self.jd_2000())

    #convert a 3-dimensional vector to a unit vector
    def unit_vector(self, vector):
        magnitude = math.sqrt(math.pow(vector[0], 2) + math.pow(vector[1], 2) + math.pow(vector[2], 2))
        unit_vec = np.array([vector[0]/magnitude, vector[1]/magnitude, vector[2]/magnitude])
        return unit_vec
    
    #get reference vector in earth-centered earth-fixed frame
    def mag_vector_ecef(self):
        value = pyIGRF.igrf_value(self.latitude, self.longitude, self.altitude, self.decimal_date(datetime.datetime.now()))
        return np.array([value[3], value[4], value[5]])
        
    #convert reference vector frame from earth-centered-earth-fixed to earth-centered-inertial
    def mag_vector_eci(self):
        theta = self.get_angle()
        r1 = np.array([math.cos(theta), -1*math.sin(theta), 0])
        r2 = np.array([math.sin(theta), math.cos(theta), 0])
        r3 = np.array([0, 0, 1])
        matrix = np.array([r1, r2, r3])
        ecef = self.mag_vector_ecef()
        return np.matmul(matrix, self.mag_vector_ecef())
        
#main routine
if __name__ == "__main__":
    ref = IGRF_Reference()
    ref.set_latitude(float(input("Latitude N > ")))
    ref.set_longitude(float(input("Longitude E > ")))
    ref.set_altitude(float(input("Altitude (km) > ")))
    vector = ref.mag_vector_eci();
    print("Unit vector in Earth-Centered Inertial Frame: {0}".format(ref.unit_vector(vector)))
