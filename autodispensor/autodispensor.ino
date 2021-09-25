#include <VarSpeedServo.h>
#define PIR_PIN 7
#define SERVO_PIN 8
VarSpeedServo myservo;
bool checkHumanExist();
void moveDispensor();

void setup() {
  Serial.begin(9600);
  pinMode(PIR_PIN, INPUT_PULLUP);
  myservo.attach(SERVO_PIN,500,2300);
}

void loop() {
  delay(250);         // メインループスリープ
  
  static bool isHumanExistFlag = false;//RIP検出済みフラグ
  
  if(isHumanExistFlag == false){
    //フラグTrueの状態で動きが検出されたら、Trueへ＋ディスペンサーを動かす
    if(checkHumanExist()== true){
       isHumanExistFlag = true;
       moveDispensor();
       delay(3000);
    }
  }else{
      //フラグTrueの状態で動きがなくなったら、Falseへ
      if(checkHumanExist() == false){
       isHumanExistFlag = false;
    }
  }
}

bool checkHumanExist(){
  if (digitalRead(PIR_PIN) == HIGH){
      Serial.println("動き検知!");
      return true;
  }else{
      Serial.println("動きがありません");
      return false;
  }
}

void moveDispensor(){
    myservo.write(10,100,true);
    delay(500);
    myservo.write(80,100,true);
}
