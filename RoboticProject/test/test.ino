#include <string.h>
String incomingByte;
const int dirPin = 5;
const int stepPin = 6;

const int forwardPin = 8;
const int backwardPin = 9;
const int stepsPerRevolution = 200; //200

int rev = 50; //normally 200
int rev2 = 200 * 50;
void setup() {
  // Declare pins as Outputs
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);

  pinMode(forwardPin, OUTPUT);
  pinMode(backwardPin, OUTPUT);

}

void loop() {

  if (Serial.available() > 0) {
    incomingByte = Serial.readStringUntil('\n');
    writeString(incomingByte + ' ');
    
    String a = getValue(incomingByte, '/', 0);
    String b = getValue(incomingByte, '/', 1);

    writeString(a + ' ');
    writeString(b + ' ');

    if (a == "reset") {
      
//      for (int x = 0; x < rev*8; x++) {
//        digitalWrite(dirPin, LOW);
//        digitalWrite(stepPin, HIGH);
//        delayMicroseconds(2500);
//        digitalWrite(stepPin, LOW);
//      }
//
//      for (int x = 0; x < rev2; x++) {
//        digitalWrite(forwardPin, HIGH);
//        digitalWrite(backwardPin, LOW);
//        delayMicroseconds(100); // 100 microseconds give max speed
//        digitalWrite(forwardPin, LOW);
//      }
//      
      // writeString("resetting");
      for (int x = 0; x < 200*8; x++) {
        digitalWrite(dirPin, HIGH);
        digitalWrite(stepPin, HIGH);
        delayMicroseconds(1500);
        digitalWrite(stepPin, LOW);
      }
    }
    
    if (a == "shoot card") {

      writeString("shooting your ass");

      for (int x = 0; x < rev2; x++) {
        digitalWrite(forwardPin, HIGH);
        digitalWrite(backwardPin, LOW);
        delayMicroseconds(100); // 100 microseconds give max speed
        digitalWrite(forwardPin, LOW);
      }
      Serial.write("shooting card");
    } 

    else if (a == "next turn") {
      for (int x = 0; x < rev*8; x++) {
        digitalWrite(dirPin, LOW);
        digitalWrite(stepPin, HIGH);
        delayMicroseconds(2500);
        digitalWrite(stepPin, LOW);
      }
    }
    else {
      int num_players = (int)incomingByte[0]-48;
      rev = (int) (stepsPerRevolution / num_players);
      //Serial.write(rev);
    }
  }
}

String getValue(String data, char separator, int index)
{
  int found = 0;
  int strIndex[] = {0, -1};
  int maxIndex = data.length()-1;
  
  for (int i=0; i<=maxIndex && found<=index; i++){
    if(data.charAt(i)==separator || i==maxIndex){
        found++;
        strIndex[0] = strIndex[1]+1;
        strIndex[1] = (i == maxIndex) ? i+1 : i;
    }
  }
  return found>index ? data.substring(strIndex[0], strIndex[1]) : "";
}

void writeString(String stringData) { // Used to serially push out a String with Serial.write()
  for (int i = 0; i < stringData.length(); i++) {
    Serial.write(stringData[i]);   // Push each char 1 by 1 on each loop pass
  }
}
