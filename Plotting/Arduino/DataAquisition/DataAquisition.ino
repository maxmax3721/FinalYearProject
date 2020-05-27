//https://www.arduino.cc/ for arudino coding support
//Data Aquisition Arduino Code
//Pin Assigments
//Digital Output Pins to MOSFETS
const byte r8 = 2;
const byte r7 = 3;
const byte r6 = 4;
const byte r5 = 5;
const byte r4 = 6;
const byte r3 = 7;
const byte r2 = 8;
const byte r1 = 9;
//Relay digital Out pin 
const byte Relay = 10;

//Assign Resistor Values
const float R1= .032;
const float R2 = .058;
const float R3 = .121;
const float R4 = .246;
const float R5 = .500;
const float R6 = .991;
const float R7 = 2.183;
const float R8 = 4.680;  

//Create Array of Resistor Values
float res[]={R8,R7,R6,R5,R4,R3,R2,R1};

//Initialise Voltage and Current Variables
//Measured Voltage on Analogue In
float vOUT = 0.0;
//Calculated Panel Current and Voltage
float vIN = 0.0;
float iIN = 0.0;
//Assign Voltage Divider Resistor Values
float R9 = 3820000;
float R10 = 998000;


////Variables for Timing Investigation
//unsigned long start=0;
//unsigned long finish=0;
//unsigned long t=0;
////Start Code Timer
//start=micros()
////
////{code to be timed}
////
////Stop code timer
//finish=micros()
////Calculate code execution time which can be printed to serial port
//t=finish-start

void setup() {               
  // initialize the digital pins as an outputs.
  pinMode(r8, OUTPUT);
  pinMode(r7, OUTPUT);
  pinMode(r6, OUTPUT);
  pinMode(r5, OUTPUT);
  pinMode(r4, OUTPUT);
  pinMode(r3, OUTPUT);
  pinMode(r2, OUTPUT);
  pinMode(r1, OUTPUT);
  pinMode(Relay, OUTPUT);
 // Switch Relay to Connect Panel to Operating Load
 digitalWrite(Relay,HIGH);

}

void loop() {

  Serial.begin(9600);
  
  while(Serial){
    //if there is data to be read on serial port
    if(Serial.available()>0){
      //read serial input
      char SerIn=Serial.read();

      //Wait for command to take new characteristic from Server Machine 
      if(SerIn=='s'){

        //Switch relay to connect panel accross Variable Resistance
        digitalWrite(Relay,LOW);
        
        //Vary Resistance Values and print V and I at each point to serial port 
        ResSweep(0,21,1);

        //Switch relay back to reconnect panel to operating load
        digitalWrite(Relay,HIGH);

       // delay while operating load settles to operating voltage 
       //neccesary delay is dependant on transient behaviour of operating load
        delay(100);

        //Measure and calculate operating voltage
        vOUT = analogRead(A0)*(5.0/ 1024.0);
        vIN = vOUT / (R10/(R10+R9));
        //print operating voltage to serial port
        Serial.print(vIN);
        Serial.print ("\n");
      }
      
    }
  } 
}

//Resistance Sweep Function, specify start value, finish value and step size for Rbyte in decimal e.g. ResSweep(1,131,10) used 13 resistance values
void ResSweep(int startVal,int finishVal,int stepSize) {

  //Increment 8 bit binary value (Rbyte) by step (stepSize) between (startVal) and (finishVal)
  for(byte Rbyte=startVal; Rbyte <= finishVal; Rbyte=Rbyte+stepSize){
    
    
    //Each Bit of Byte used to assigns output value to gate of MOSFET (Turn MOSFET on or off)
    digitalWrite(r1, bitRead(Rbyte,7)); 
    digitalWrite(r2, bitRead(Rbyte,6));
    digitalWrite(r3, bitRead(Rbyte,5));
    digitalWrite(r4, bitRead(Rbyte,4));
    digitalWrite(r5, bitRead(Rbyte,3));
    digitalWrite(r6, bitRead(Rbyte,2));
    digitalWrite(r7, bitRead(Rbyte,1));
    digitalWrite(r8, bitRead(Rbyte,0));
 
    
    delay(4);
    
   
    //Measure Voltage On analogue pin
    vOUT = analogRead(A0)*(5.0/ 1024.0);
    //Calculate Panel voltage from voltage divider resistances  
    
    
    vIN = vOUT / (R10/(R10+R9));
    //Apply corrections from voltage calibration
    vIN=0.925*vIN+0.01;
   
    //Calculate Resistance from Parallel combination of resistors
    float reciprocal=1/(R9+R10);
      for (int i=0; i<8 ; i++){
        if (bitRead(Rbyte,i)== 1){
          reciprocal+=1/res[i];
        } 
      }  
      float R =1/reciprocal;
      
      //Calculate Current from resistance and voltage  
      iIN=vIN/(R);
      
    //Send voltage and current values to server machine through serial port in CSV format
    Serial.print(vIN);
    Serial.print(",");
    Serial.print(iIN,0);

    // end of csv record
    Serial.print ("\n");
   }
}
