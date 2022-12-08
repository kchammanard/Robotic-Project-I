#include <string.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x3F, 16, 2);

String incomingByte;
const int dirPin = 5;
const int stepPin = 6;

const int trigPin = 4;
const int echoPin = 7;

const int forwardPin = 9;
const int backwardPin = 10; //9
const int stepsPerRevolution = 200; //200

int rev = 50; //normally 200
int rev2 = 200;

int count = 0;
int gamestart = 0;

String currentplayer = "1";
String detection;

void setup() {
  // Declare pins as Outputs
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);

  pinMode(forwardPin, OUTPUT);
  pinMode(backwardPin, OUTPUT);

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.clear();
//  lcd.print("Robotic Project I");
}

void loop() {

  if (Serial.available() > 0) {

    incomingByte = Serial.readStringUntil('\n');
    writeString(incomingByte + ' ');

    String a = getValue(incomingByte, '/', 0);
    String b = getValue(incomingByte, '/', 1);
//    if ( 48 > b[0] || 57 < b[0]) {
//      b = "1";
//    }
    writeString(a + ' ');
    writeString(b + ' ');

    if (a == "start") {
      //lcd.clear();
      lcd.print("Robotic Project I");
    }
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
      for (int x = 0; x < 200 * 8; x++) {
        digitalWrite(dirPin, HIGH);
        digitalWrite(stepPin, HIGH);
        delayMicroseconds(1500);
        digitalWrite(stepPin, LOW);
      }
    }

    if (a == "shoot card") {

      writeString("shooting your ");
      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print("Shooting card...");
      delay(1000);
      for (int x = 0; x < rev2; x++) {
        digitalWrite(forwardPin, HIGH);
        digitalWrite(backwardPin, LOW);
        delayMicroseconds(100); // 100 microseconds give max speed
        digitalWrite(forwardPin, LOW);
      }
      Serial.write("shooting card");
      lcd.clear();
      lcd.print("Current player:");
      lcd.setCursor(0, 1);
      lcd.print("Player ");
      lcd.print(currentplayer);
      displayDetection();
    }

    else if (a == "next turn") {
      lcd.clear();
      lcd.print("Current player:");
      lcd.setCursor(0, 1);
      lcd.print("Player ");
      lcd.print(b);
      displayDetection();
      currentplayer = b;
      if (b[0] == '1') {
        for (int x = 0; x < (200 - rev) * 8; x++) {
          digitalWrite(dirPin, HIGH);
          digitalWrite(stepPin, HIGH);
          delayMicroseconds(2000);
          digitalWrite(stepPin, LOW);
        }
      }
      else {
        for (int x = 0; x < rev * 8; x++) {
          digitalWrite(dirPin, LOW);
          digitalWrite(stepPin, HIGH);
          delayMicroseconds(2500);
          digitalWrite(stepPin, LOW);
        }
      }
    }
    else {
      int num_players = (int)incomingByte[0] - 48;
      if (num_players > 10) {
        lcd.clear();
        lcd.print("Welcome to");
        lcd.setCursor(0, 1);
        lcd.print("GoHeng!");
        delay(2000);
        lcd.clear();
        delay(1000);
        lcd.print("Counting Players");
        lcd.setCursor(0, 1);
        for (int i = 0; i < 5; i++) {
          lcd.print(".");
          delay(2000);
        }
      }
      else {
        rev = (int) (stepsPerRevolution / num_players);
        lcd.clear();
        lcd.print(num_players);
        lcd.print(" Players");
        delay(1500);
        lcd.clear();
        lcd.print("Current player:");
        lcd.setCursor(0, 1);
        lcd.print("Player 1");
        //lcd.rightToLeft();
        //Serial.write(rev);
      }
      displayDetection();
    }
  }
}

String getValue(String data, char separator, int index)
{
  int found = 0;
  int strIndex[] = {0, -1};
  int maxIndex = data.length() - 1;

  for (int i = 0; i <= maxIndex && found <= index; i++) {
    if (data.charAt(i) == separator || i == maxIndex) {
      found++;
      strIndex[0] = strIndex[1] + 1;
      strIndex[1] = (i == maxIndex) ? i + 1 : i;
    }
  }
  return found > index ? data.substring(strIndex[0], strIndex[1]) : "";
}

void writeString(String stringData) { // Used to serially push out a String with Serial.write()
  for (int i = 0; i < stringData.length(); i++) {
    Serial.write(stringData[i]);   // Push each char 1 by 1 on each loop pass
  }
}

void displayDetection() {

    long duration, distance;
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);
    duration = pulseIn(echoPin, HIGH, 1000000);
    distance = (duration / 2) / 29.41;
    
//    if (distance >= 200 || distance <= 0) {
//      detection = "no";
//    }
    lcd.setCursor(12,1);
    if (distance >= 0 && distance <= 20) {
      lcd.print("(a)");
    }
    else {
      lcd.print("(n)");
    }
    delay(10);
}
