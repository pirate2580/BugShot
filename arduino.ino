#include <Servo.h>
#include <Stepper.h>

Servo fire1;  // create servo object to control a servo
Servo fire2;  // create servo object to control a 
Servo pitch;
const int stepsPerRevolution = 2048;
//int potpin = 0;  // analog pin used to connect the potentiometer
//int val;    // variable to read the value from the analog pin
Stepper myStepper(stepsPerRevolution, 8, 10, 9, 11);
int pitch_current = 0;
void setup() {
  fire1.attach(6);  // attaches the servo on pin 9 to the servo object
  fire2.attach(5);
  pitch.attach(7);
  myStepper.setSpeed(15);
  Serial.begin(9600);

  fire1.write(0);
  fire2.write(0);
  pitch.write(45);
  delay(1000);
}

void loop() {
  //Serial.print(pitch_current);
  if(analogRead(A1) < 250){
    myStepper.step(-stepsPerRevolution/16);  // manual override, skip execution and loop again
  } else if(analogRead(A1) > 750){
    myStepper.step(stepsPerRevolution/16);
  } else if(analogRead(A0) < 250){
    if(pitch_current<=20){
      pitch_current += 5;
      pitch.write(40-pitch_current);
    }
    delay(100);
  } else if(analogRead(A0) > 750){
    if(pitch_current >= 5){
      pitch_current -= 5;
      pitch.write(40-pitch_current);
    }
    delay(100);
  } else {

  delay(20);       //idle
  }
}
﻿
Revan
r3v4n_421
𝓙υᖙᗩᔕ

when in doubt, reduce everything to single variable calculus