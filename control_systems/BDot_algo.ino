#include "MPU9250.h"

// An MPU9250 object with the MPU-9250 sensor on I2C bus 0 with address 0x68
MPU9250 IMU(Wire,0x68);

// Status of magnetometer
int status;
// Dummy variable to print out calibration vals
float value;
// K value of BDot algorithm
float k;
// Number of coil windings
int num_of_windings = 1;
// Surface area of torquerod/coil
float surface_area = 1.0;

// Output pin to power coil
int PWM_out_pin = 9;

float prev_value_x = 0;
float new_value_x = 0;

float prev_value_y = 0;
float new_value_y = 0;

float prev_value_z = 0;
float new_value_z = 0;

void setup() {
  // Setting PWM to Output mode
  pinMode(PWM_out_pin, OUTPUT);
  
  // serial to display data
  Serial.begin(115200);
  while(!Serial) {}

  // start communication with IMU 
  status = IMU.begin();
  if (status < 0) {
    Serial.println("IMU initialization unsuccessful");
    Serial.println("Check IMU wiring or try cycling power");
    Serial.print("Status: ");
    Serial.println(status);
    while(1) {}
  }
  
  // Start the magnetometer calibration
  Serial.println("Starting Magnetometer Calibration");
  Serial.println("***");
  Serial.println();
  delay(2000);

  // Calibrating
  Serial.println("Move in an 8 shape...");
  Serial.println("***");
  Serial.println();
  int cal = IMU.calibrateMag();

  if (cal > 0) {
    Serial.println("Calibration success!");
  } else {
    Serial.println("Calibration failure!");
  }

  // Printling the values
  Serial.println("Printing values");
  Serial.println("***");
  Serial.println();

  // Accel Bias and Factors
  value = IMU.getAccelBiasX_mss();
  Serial.print("Accel bias x: "); Serial.print(value);
  Serial.println();
  
  value = IMU.getAccelScaleFactorX();
  Serial.print("Accel factor x: "); Serial.print(value);
  Serial.println();
  
  value = IMU.getAccelBiasY_mss();
  Serial.print("Accel bias y: "); Serial.print(value);
  Serial.println();
  
  value = IMU.getAccelScaleFactorY();
  Serial.print("Accel factor y: "); Serial.print(value);
  Serial.println();
  
  value = IMU.getAccelBiasZ_mss();
  Serial.print("Accel bias z: "); Serial.print(value);
  Serial.println();
  
  value = IMU.getAccelScaleFactorZ();
  Serial.print("Accel factor z: "); Serial.print(value);
  Serial.println();

  // Mag Bias
  value = IMU.getMagBiasX_uT();
  Serial.print("Mag bias x: "); Serial.print(value);
  Serial.println();
  
  value = IMU.getMagScaleFactorX();
  Serial.print("Mag factor x: "); Serial.print(value);
  Serial.println();
  
  value = IMU.getMagBiasY_uT();
  Serial.print("Mag bias y: "); Serial.print(value);
  Serial.println();
  
  value = IMU.getMagScaleFactorY();
  Serial.print("Mag factor y: "); Serial.print(value);
  Serial.println();
  
  value = IMU.getMagBiasZ_uT();
  Serial.print("Mag bias z: "); Serial.print(value);
  Serial.println();
  
  value = IMU.getMagScaleFactorZ();
  Serial.print("Mag factor z: "); Serial.print(value);
  Serial.println();
  
  Serial.println("\n\n***\n\n");
  Serial.println("Reading Data\n");

}

float RateOfChange_X() {
  return new_value_x - prev_value_x;
}

float RateOfChange_Y() {
  return new_value_y - prev_value_y;
}

float RateOfChange_Z() {
  return new_value_z - prev_value_z;
}

float OutputCurrent_Calculate(float rate) {
  float current = (k * rate)/(num_of_windings * surface_area);
  return current;
}

void OutputCurrent_X() {
  Serial.print("\n Current on X\n");
  Serial.print(OutputCurrent_Calculate(RateOfChange_X()));
}

void OutputCurrent_Y() {
  Serial.print("\n Current on Y\n");
  Serial.print(OutputCurrent_Calculate(RateOfChange_Y()));
}

void OutputCurrent_Z() {
  Serial.print("\n Current on Z\n");
  Serial.print(OutputCurrent_Calculate(RateOfChange_Z()));
}

void loop() {
  byte PWM_out_level;


  PWM_out_level = 153;

  analogWrite( PWM_out_pin, PWM_out_level);
  
  // read the sensor
  IMU.readSensor();

  prev_value_x = new_value_x;
  prev_value_y = new_value_y;
  prev_value_z = new_value_z;

  Serial.print("\nMagX: ");  
  Serial.print(IMU.getMagX_uT(),6);
  new_value_x = IMU.getMagX_uT();

  Serial.print("  ");  
  Serial.print("MagY: ");
  Serial.print(IMU.getMagY_uT(),6);
  new_value_y = IMU.getMagY_uT();
  
  Serial.print("  ");
  Serial.print("MagZ: ");  
  Serial.println(IMU.getMagZ_uT(),6);
  new_value_z = IMU.getMagZ_uT();

  Serial.print("Rate Of Change for X axis: ");
  Serial.print(RateOfChange_X());
  Serial.print("\nRate Of Change for Y axis: ");
  Serial.print(RateOfChange_Y());
  Serial.print("\nRate Of Change for Z axis: ");
  Serial.print(RateOfChange_Z());

  OutputCurrent_X();
  OutputCurrent_Y();
  OutputCurrent_Z();
  
  Serial.print("\n****\n");

  delay(1000);
} 


 
