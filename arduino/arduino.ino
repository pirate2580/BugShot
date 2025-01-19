#include <Servo.h>
#include <Stepper.h>

Servo fire1;  // create servo object to control a servo
Servo fire2;  // create servo object to control a 
Servo pitch;
const int stepsPerRevolution = 2048;
const int gearRatio = 7;
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
    if(pitch_current >= -5){
      pitch_current -= 5;
      pitch.write(40-pitch_current);
    }
    delay(100);
  } else if(digitalRead(12) == 0){
    fire1.write(180);
    fire2.write(180);
    delay(1200);
    fire1.write(0);
    fire2.write(0);
    delay(1200);
  } else {

    //loop here actual
    int goal_yaw = 0;
    int goal_pitch = 0;
    if(Serial.available() >= 2){
      goal_pitch = Serial.read();
      goal_yaw = Serial.read();
      Serial.println("Pitch...");
      Serial.println(goal_pitch);
      if(goal_pitch<=45){
        pitch_current = goal_pitch;
        pitch.write(goal_pitch);
        delay(1200);
      }

      Serial.println("Yaw...");
      Serial.println(goal_yaw);
      float bruh_yaw = 2048*((float)goal_yaw - 90)*7/360;
      float bruh_pitch = (float)goal_pitch;
      Serial.println(bruh_yaw);
      Serial.println((int)bruh_yaw);
      myStepper.step((int)bruh_yaw);
      fire1.write(180);
      fire2.write(180);
      delay(1000);
      fire1.write(0);
      fire2.write(0);
      delay(300);
      myStepper.step((int)-bruh_yaw);
      while(Serial.available() > 0){
        char temp = Serial.read();
      }
    }
    else if(Serial.available()==1){
      int temp = Serial.read();
    }
    delay(20);       //idle
  }
}