#define L   A0
#define R   A1

const unsigned long fs = 300;
const unsigned long dt = 1000000/fs;
int reads;
char rcv;

void setup() {
  Serial.begin(115200);
 
  //analogReadResolution(12); 
}


void read(){
  unsigned long pre_micros;
  unsigned long current_micros;
  byte b1, b2;
  int left, right;
  
  current_micros = micros();
  pre_micros = current_micros;
 
  while(reads > 0){
    current_micros = micros();
    if((current_micros - pre_micros) > dt){
      pre_micros = current_micros;
      left = analogRead(L);
      right = analogRead(R);

      b1 = left & 0xFF;
      b2 = (left >> 8) & 0xFF;
      Serial.write(b1);
      Serial.write(b2);

      b1 = right & 0xFF;
      b2 = (right >> 8) & 0xFF;
      Serial.write(b1);
      Serial.write(b2);
      reads--;
      delayMicroseconds(100);
      }   
    }
}


void loop() {
  if(Serial.available() > 0){
    rcv = Serial.read();
    //Serial.print(rcv);
    if(rcv == '1'){
      reads = fs;
      read();
      delay(10);
    }
  }
}


/*
float test;

void loop(){
  test = analogRead(A0);
  test = (test*1.0/4095)*3.3;
  Serial.println(test);
  delay(1000/fs);

}

*/
