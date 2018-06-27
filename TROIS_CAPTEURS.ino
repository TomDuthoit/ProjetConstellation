//---------------------------------------------------------------------------------------------------------------
//                                             LIBRARIES
//---------------------------------------------------------------------------------------------------------------
#include <ArduinoJson.h>
#include <OneWire.h>                              //Library for OneWire sensors
#include <DallasTemperature.h>                    //Library of DS18B20 sensor
//---------------------------------------------------------------------------------------------------------------
//                                             DEFINES
//---------------------------------------------------------------------------------------------------------------
#define CO2Input     A0                           //CO2 sensor input (MQ135)
#define SoundInput    A1                          //Sound sensor input
#define LedRedOutput    5
#define LedGreenOutput  4
#define LedBlueOutput   3
#define CO2Calibration     30                     //CO2 calibration measurement
OneWire oneWire(2);                               //One Wire sensor input (DS18B20)
DallasTemperature sensors(&oneWire);              //Using the Onewire bus for temperature sensor
DeviceAddress sensorDeviceAddress;                //Check the compatibility of the temperature sensor with the library

//---------------------------------------------------------------------------------------------------------------
//                                             SETUP
//---------------------------------------------------------------------------------------------------------------
void setup() {
  
   // output pin configuration
  pinMode (LedGreenOutput,OUTPUT);
  pinMode (LedRedOutput,OUTPUT);
  pinMode (LedBlueOutput,OUTPUT);
  pinMode(CO2Input,INPUT);                        //Set the CO2 pin as input
  pinMode (SoundInput, INPUT);                    // Set the sound pin as input   
  Serial.begin(9600);                             //sets the serial port to 9600
   // Settings of the temperature sensor
  sensors.begin();                                //Activation of the temperature sensor
  sensors.getAddress(sensorDeviceAddress, 0);     //Request sensor address at bus index 0
  sensors.setResolution(sensorDeviceAddress, 12); //Choose the resolution
}
//for LED lighting
int data;                                         // int for the value input (a=turn on & e=turn off)
int color;                                        // int for the color number
int LEDstate=0;                                   // 0 (led turn off), 1 (led turn on)


//---------------------------------------------------------------------------------------------------------------
//                                             MAIN LOOP
//---------------------------------------------------------------------------------------------------------------
void loop() {
  
int Measure_num = 100;                            //int number of measurements

int CO2Sample;                                    //int for the value read CO2 sensor
int CO2Raw = 0;                                   //int for raw value of co2
int CO2Comp = 0;                                  //int for compensated co2 
int CO2ppm = 0;                                   //int for calculated ppm
int CO2Average = 0;                               //int for averaging

long SoundSample;                                 //long for the value read Sound Sensor   
long SoundSum = 0 ;                               //long for sum of all samples
long SoundLevel = 0;                              //long for the avarage value
int dB = 0;                                       // int for the value converts into dB


for (int i = 0; i<Measure_num ; i++)              //taking samples of CO2 and sum all
{
    CO2Sample=analogRead(CO2Input);
    CO2Average =CO2Average + CO2Sample; 
    
  }

CO2Raw = CO2Average/Measure_num;                  //average samples
CO2Comp = CO2Raw - CO2Calibration;                //compensate the value
CO2ppm = map(CO2Comp,0,1023,400,5000);            //calibration in the right value range

for ( int i = 0 ; i <Measure_num; i ++)           //taking samples of sound level and sum all
  {  
   SoundSample = analogRead (SoundInput);  
   SoundSum = SoundSum + SoundSample;  
  }  

SoundLevel = SoundSum / Measure_num;              // Calculate the average value
dB=10*log(SoundLevel);                            // COnvert into dB

sensors.requestTemperatures();                    //Ask the temperature to the sensor

// we are waiting for data on the serial
if (Serial.available()>0) {  
  // read the data received (in the "data" variable)
  data=Serial.read();
  Serial.println(data);
  }

// if the data is "e", we turn off the led L
if (data==101) {
   LEDstate=0;
   digitalWrite(LedRedOutput,0);
   digitalWrite(LedGreenOutput,0);
   digitalWrite(LedBlueOutput,0);
   }
     
// if the data is at "a", turn on the led L
if (data==97) {
    LEDstate=1;
    color = nightlight(color);
    color++;
    }  

StaticJsonBuffer<200> jsonBuffer;                 // print the value in JSON format
JsonObject& root = jsonBuffer.createObject();
root["CO2Level"] = CO2ppm;
root["SoundLevel"] = dB;
root["Temperature"] =sensors.getTempCByIndex(0) ;
root["Ledstate"] =LEDstate ;
root.printTo(Serial);
Serial.println(" ");
delay(1000);
}

//---------------------------------------------------------------------------------------------------------------
//                                             OTHER FUNCTIONS
//---------------------------------------------------------------------------------------------------------------

//---- function for progressive color variation ----

void ledRGBpwm(int pwmRed, int pwmGreen, int pwmBlue) { // receives value between 0 and 255 per color

 analogWrite(LedRedOutput, pwmRed);                 // desired width pulse on the pin 0 = 0% and 255 = 100% high
 analogWrite(LedGreenOutput, pwmGreen);    
 analogWrite(LedBlueOutput, pwmBlue);      

}

int nightlight(int color){
  switch(color){
    case 1:
          // Add red
          for (int i=0; i<=255; i++) { // scrolls from 0 to 255
            ledRGBpwm(i,0,0); // generates desired pulse width for color
            delay(10); //pause
          }
          // Remove red
          for (int i=0; i<=255; i++) {
            ledRGBpwm(255-i,0,0); 
            delay(10); 
          }
          ledRGBpwm(0,0,0);
          break;
    case 2:
          // Add magenta
          for (int i=0; i<=255; i++) { 
            ledRGBpwm(i,0,i); 
            delay(10); 
          }
          // Remove magenta
          for (int i=0; i<=255; i++) { 
            ledRGBpwm(255-i,0,255-i); 
            delay(10); 
          }
          ledRGBpwm(0,0,0);
          break;
    case 3:
       // Add blue
          for (int i=0; i<=255; i++) { 
            ledRGBpwm(0,0,i); 
            delay(10); 
          }
          // Remove blue
          for (int i=0; i<=255; i++) { 
            ledRGBpwm(0,0,255-i); 
            delay(10); 
          }
          ledRGBpwm(0,0,0);
          break;
    case 4:
       // Add cyan
          for (int i=0; i<=255; i++) { 
            ledRGBpwm(0,i,i); 
            delay(10); 
          }
          // Remove cyan
          for (int i=0; i<=255; i++) { 
            ledRGBpwm(0,255-i,255-i); 
            delay(10); 
          }
          ledRGBpwm(0,0,0);
          break;
    case 5:
       // Add green
          for (int i=0; i<=255; i++) { 
            ledRGBpwm(0,i,0); 
            delay(10); 
          }
          // Remove green
          for (int i=0; i<=255; i++) { 
            ledRGBpwm(0,255-i,0); 
            delay(10); 
          }
          ledRGBpwm(0,0,0);
          break;
    case 6:
       // Add yellow
          for (int i=0; i<=255; i++) { 
            ledRGBpwm(i,i,0); 
            delay(10); 
          }
          // Remove yellow
          for (int i=0; i<=255; i++) { 
            ledRGBpwm(255-i,255-i,0); 
            delay(10); 
          }
          color=0;
          ledRGBpwm(0,0,0);
          break;
    default:
         color=0;
         ledRGBpwm(0,0,0);
         break;
  }
  return color;
}




