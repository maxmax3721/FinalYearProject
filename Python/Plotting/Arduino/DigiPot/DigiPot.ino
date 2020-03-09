//Variable Resistor
const byte R8 = 2;
const byte R7 = 3;
const byte R6 = 4;
const byte R5 = 5;
const byte R4 = 6;
const byte R3 = 7;
const byte R2 = 8;
const byte R1 = 9;
const byte Relay = 10;
const byte CharacterisationMOS = 10;
const byte OperationMOS = 11;

const float r1 = .047;
const float r2 = .468;
const float r3 = .991;
const float r4 = 2.183;
const float r5 = 4.680;
const float r6 = 9.410;
const float r7 = 15.940;
const float r8 = 33.450;


float res[]={r8,r7,r6,r5,r4,r3,r2,r1};

//voltage sense
const int voltageSensor = A0;
float vOUT = 0.0;
float vIN = 0.0;
float r10 = 998000;
float r11 = 241000;

//current sense
float iIN = 0.0;

void setup() {               
  // initialize the digital pins as an outputs.
  pinMode(R8, OUTPUT);
  pinMode(R7, OUTPUT);
  pinMode(R6, OUTPUT);
  pinMode(R5, OUTPUT);
  pinMode(R4, OUTPUT);
  pinMode(R3, OUTPUT);
  pinMode(R2, OUTPUT);
  pinMode(R1, OUTPUT);
  pinMode(Relay, OUTPUT);

 digitalWrite(Relay,HIGH);

}

void loop() {

  Serial.begin(9600);
  
  while(Serial){
    if(Serial.available()>0){
      char SerIn=Serial.read();
 
      if(SerIn=='s'){
        digitalWrite(Relay,LOW);
        
        ResSweep(0,68,4);
        ResSweep(70,130,10);

        digitalWrite(Relay,HIGH);

        delay(500);
        
        vOUT = analogRead(A0)*(5.0/ 1024.0);
        vIN = vOUT / (r11/(r10+r11));
        Serial.print(vIN);
        Serial.print ("\n");

      }else{
        vOUT = analogRead(A0)*(5.0/ 1024.0);
        vIN = vOUT / (r11/(r10+r11));
        Serial.print(vIN);
        Serial.print ("\n");
      }
    }
  } 
}

void ResSweep(int StartCount,int FinishCount,int StepSize) {
  
  for(byte count=StartCount; count <= FinishCount; count=count+StepSize){

    digitalWrite(R1, bitRead(count,7)); 
    digitalWrite(R2, bitRead(count,6));
    digitalWrite(R3, bitRead(count,5));
    digitalWrite(R4, bitRead(count,4));
    digitalWrite(R5, bitRead(count,3));
    digitalWrite(R6, bitRead(count,2));
    digitalWrite(R7, bitRead(count,1));
    digitalWrite(R8, bitRead(count,0));
   
    delay(5);
  
  //Voltage
  
    vOUT = analogRead(A0)*(5.0/ 1024.0);
    vIN = vOUT / (r11/(r10+r11));
  
  //Current
    float reciprocal=0;
      for (int i=0; i<8 ; i++){
        if (bitRead(count,i)== 1){
          reciprocal+=1/res[i];
        } 
      }
      
      float R =1/reciprocal;
      iIN=vIN/(R);
    
    Serial.print(vIN);
    Serial.print(",");
    Serial.print(iIN);
    
    
    // end of csv record
    Serial.print ("\n");
   }
}
