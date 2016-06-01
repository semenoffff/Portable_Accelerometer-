#include "Wire.h"
#include "Stream.h"
#include "stdint.h"
#include "stdio.h"

#define LSM6DS3 0x6B // LSM6DS3 I2C address when SDO pulled to Vdd
#define CTRL1_XL 0x10
#define CTRL2_G 0x11
#define CTRL9_XL 0x18
#define CTRL10_C 0x19
#define INT1_CTRL 0x0D
#define STATUS_REG 0x1E // read only
#define CTRL5_C 0x14

int masterClock = 0;         // counts rising edge clock signals
int seconds = 0;             // variable
int minutes = 0;             // variable

void setup() {
  Wire.begin(); //join I2C bus
  Serial.begin(9600); //initialize serial
  delay(1000);
  attachInterrupt(digitalPinToInterrupt(3), clockCounter, RISING); //  clockInt is our interrupt, 
  //clockCounter function is called when invoked on a RISING clock edge
  analogReference(DEFAULT);
  analogWrite(3, 125);   // this starts our PWM 'clock' with a 50% duty cycle
  accelerometerSetup(); // configure accelerometer registers to colect data
  gyroscopeSetup(); // configure gyroscope registers to collect data
  registerWrite(INT1_CTRL, 0x03); // quick fix on INT1_CTRL value
  registerWrite(CTRL5_C, 0x60); //rounding of accelerometer and gyroscope data    
}

void loop() {
  /*Collecting data from accelerometer registers*/
  int8_t statusRegValue = registerRead(STATUS_REG); // check the value of STATUS_REG
  char buff[100];
  
  //  Serial.println(statusRegValue);
  if (statusRegValue & 0x01) {       // check XLDA bit (XLDA bit 1 --> accelerometer data ready)
    int16_t X_L_XL = registerRead(0x28); // read X axes lower 8 bits
    int16_t X_H_XL = registerRead(0x29); // read X axes higher 8 bits
    int16_t Y_L_XL = registerRead(0x2A); // read Y axes lower 8 bits
    int16_t Y_H_XL = registerRead(0x2B); // read Y axes higher 8 bits
    int16_t Z_L_XL = registerRead(0x2C); // read Z axes lower 8 bits
    int16_t Z_H_XL = registerRead(0x2D); // read Z axes higher 8 bits
   
    int16_t X_HL_XL = (X_H_XL << 8) |  X_L_XL; // concatinate lower and higher register values for X axes
    int16_t Y_HL_XL = (Y_H_XL << 8) |  Y_L_XL; // concatinate lower and higher register values for Y axes
    int16_t Z_HL_XL = (Z_H_XL << 8) |  Z_L_XL; // concatinate lower and higher register values for Z axes

    int16_t X_L_G = registerRead(0x22);
    int16_t X_H_G = registerRead(0x23);
    int16_t Y_L_G = registerRead(0x24);
    int16_t Y_H_G = registerRead(0x25);
    int16_t Z_L_G = registerRead(0x26);
    int16_t Z_H_G = registerRead(0x27);
    int16_t X_HL_G = (X_H_G << 8) |  X_L_G;
    int16_t Y_HL_G = (Y_H_G << 8) |  Y_L_G;
    int16_t Z_HL_G = (Z_H_G << 8) |  Z_L_G;
    
    delay(1000);
    sprintf(buff, "%04X %04X %04X %04X %04X %04X %d", X_HL_XL, Y_HL_XL, Z_HL_XL, X_HL_G, Y_HL_G, Z_HL_G, seconds);
    Serial.println(buff);    
  }
  else
    Serial.println("Wait a second for data to be ready...");
}
void clockCounter()      // called by interrupt
{
  masterClock ++;        // with each clock rise add 1 to masterclock count
  if(masterClock == 489) // 490Hz reached     
  {                         
    seconds ++;          // after one 490Hz cycle add 1 second 
    masterClock = 0;     // Reset after 1 second is reached
   }
  return;
}
void accelerometerSetup(void) {
  /* Accelerometer setup sequance*/
  registerWrite(CTRL9_XL, 0x38); // Write to CTRL9_XL; Accelerometer X, Y, Z, axes enabled
  registerWrite(CTRL1_XL, 0x60); // Write to CTRL1_XL; Accelerometer @416Hz High-Performance mode
  registerWrite(INT1_CTRL, 0x01); // Write to INT1_CTRL; Accelerometer Data Ready interrupt on INT1
}
void gyroscopeSetup(void) {
  /*Gyroscope setup sequance*/
  registerWrite(CTRL10_C, 0x38); // Write to CTRL10_C; Gyroscope X, Y, Z, axes enabled
  registerWrite(CTRL2_G, 0x60); // Write to CTRL2_G; Gyroscope runs @416Hz (High-Performance Mode)
  registerWrite(INT1_CTRL, 0x02); // Write to INT1_CTRL; Gyroscope data ready interupt on INT1
}
void registerWrite(uint8_t addr, uint8_t val) {
  Wire.beginTransmission(LSM6DS3); // Select device on I2C bus
  Wire.write(addr); // Begin Transmission to a register
  Wire.write(val); // Write val to a register
  Wire.endTransmission();
}

int16_t registerRead (uint8_t offset) {
  Wire.beginTransmission(LSM6DS3); //Select device on I2C bus
  Wire.write(offset); // select register
  if (Wire.endTransmission() != 0) {
    Serial.println("Something went worng:(");
  }
  else {
    Wire.requestFrom(LSM6DS3, 1); // request one byte from the device on I2C bus
    while (Wire.available()) {
      int16_t b = Wire.read(); // read the value and store it in variable b
      return (b);
    }
  }
  Wire.endTransmission();

}
void registerCheck (uint8_t offset, String regName) {
  Wire.beginTransmission(LSM6DS3); //Select device on I2C bus
  Wire.write(offset); // select register
  if (Wire.endTransmission() != 0) {
    Serial.println("Something went worng:(");
  }
  else {
    Wire.requestFrom(LSM6DS3, 1);
    while (Wire.available()) {
      int16_t regVal = Wire.read(); // read the value and store it in variable b
      char buf[16];
      sprintf(buf, "%02X", regVal);
      Serial.print(regName + " Register value>>> ");
      Serial.println(buf); // output register value to serial monitor
      delay(1000);
    }
  }
  Wire.endTransmission();
}




