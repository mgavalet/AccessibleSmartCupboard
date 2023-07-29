#include <Adafruit_VL6180X.h> // distance sensor located at the deep of cupboard
#include <TMCStepper.h>

#define SW_RX             2 // SoftwareSerial receive pin
#define SW_TX             3 // SoftwareSerial transmit pin
#define R_SENSE 0.11f // Match to your driver
#define STALL_VALUE      50 // [0... 255]

TMC2209Stepper driver [3] = {TMC2209Stepper(SW_RX, SW_TX, R_SENSE, 0b00),
                             TMC2209Stepper(SW_RX, SW_TX, R_SENSE, 0b01),
                             TMC2209Stepper(SW_RX, SW_TX, R_SENSE, 0b10)
                            };

using namespace TMC2209_n;


const int STEPS_PER_MM =  10;
const int HOMING_AVERAGING_PULSES = 100; // starting value = 5 


int stepsDelay[3] = {2000,2000,500}; // x,y,d was 500 
int stepsDelayHigh[3] = {15000,15000,1800}; // x,y,d      d was 2500 now is 2300

int stepPin[3] = {11, 8, 5}; // x,y,d
int dirPin[3] = {10, 7, 6}; // x,y,d
int enablePin[3] = {12, 9, 4}; // x,y,d
int rmsCurrent[3] = {1200, 500, 800}; //x,y,d

int threshold[3] = {80, 50, 150}; //x,y,d 
                                  // d was 50 -> now is 80 --> now 120


long currentPos[3] = {0, 0, 0}; // initialize

boolean hommingDir[3] = {false, true, false}; //x,y,d

Adafruit_VL6180X vl = Adafruit_VL6180X(); // distance sensor located at the deep of cupboard

String InputString ;
const int MOTOR_X = 0, MOTOR_Y = 1, MOTOR_D = 2;

String doorStatus_before ; // define doorStatus --- 1. moving , 2. closed , 3. open , 4. semi-open
String doorStatus_after ; 



String getSubstring(String data, char separator, int index)
{
  int found = 0;
  int strIndex[] = { 0, -1 };
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


void setupMotorDriver(int motorId) {

  driver[motorId].beginSerial(115200);     // SW UART drivers

  driver[motorId].begin();                 // UART: Init SW UART (if selected) with default 115200 baudrate
  driver[motorId].toff(5);                 // Enables driver in software
  driver[motorId].rms_current(rmsCurrent[motorId]);        // Set motor RMS current
  driver[motorId].microsteps(2);          // Set microsteps to 1/16th

  driver[motorId].en_spreadCycle(false);   // Toggle spreadCycle on TMC2208/2209/2224
  driver[motorId].pwm_autoscale(true);     // Needed for stealthChop

  driver[motorId].TCOOLTHRS(0xFFFFF); // 20bit max
  driver[motorId].semin(5);
  driver[motorId].semax(2);
  driver[motorId].sedn(0b01);
  driver[motorId].SGTHRS(STALL_VALUE);


  //  Serial.print("\nTesting connection driver ..."); // change
  uint8_t result = driver[motorId].test_connection();

  if (result) {

    switch (result) {
      case 1: Serial.println("loose connection"); break; 
      case 2: Serial.println("no power"); break; 
    }

    // We need this delay or messages above don't get fully printed out
    delay(100);
    abort();
  }

  pinMode(stepPin[motorId], OUTPUT);
  pinMode(dirPin[motorId], OUTPUT);
  pinMode(enablePin[motorId], OUTPUT);

  digitalWrite(dirPin[motorId], LOW); // direction
  digitalWrite(enablePin[motorId], LOW); // enable

}


void moveAccordingToDistance(long mm, int motorId, boolean dir) {

  if (dir == hommingDir[motorId]) {
    currentPos[motorId] -= mm ;
  }
  else {
    currentPos[motorId] += mm ;
  }

  digitalWrite(dirPin[motorId], dir ? LOW : HIGH); // direction
  long steps = STEPS_PER_MM * mm ;

  long accelerationSteps = steps / 4;

  for (long i = 0 ; i < accelerationSteps; i++) {
    long d = stepsDelayHigh[motorId] - i * (stepsDelayHigh[motorId] - stepsDelay[motorId]) / accelerationSteps;
    givePulse(motorId, d);
  }


  for (long i = 0 ; i < steps - 2 * accelerationSteps ; i++) {
    givePulse(motorId, stepsDelay[motorId]);
  }

  for (long i = 0 ; i < accelerationSteps ; i++) {
    long d = stepsDelay[motorId] + i * (stepsDelayHigh[motorId] - stepsDelay[motorId]) / accelerationSteps;
    givePulse(motorId, d);
  }

}



void showPos() {

  Serial.print("DoorPosition,"); // write to buffer RPI
  Serial.println(currentPos[2]); 
}


void givePulse(int motorId, long d) {
  digitalWrite(stepPin[motorId], HIGH);
  delayMicroseconds(d);
  digitalWrite(stepPin[motorId], LOW);
  delayMicroseconds(d);
}


void motor_homing(int motorId) {
  currentPos[motorId] = 0 ;
  digitalWrite(dirPin[motorId], hommingDir[motorId] ? LOW : HIGH); // direction
  

  while (true) {
    long sum = 0 ;
    for (int i = 0 ; i < HOMING_AVERAGING_PULSES ; i++) {
      givePulse(motorId, stepsDelay[motorId]);
      sum += driver[motorId].SG_RESULT();
    }

    long average_sg = sum / HOMING_AVERAGING_PULSES ;
    
    Serial.print("Door average_sg is : ") ; 
    Serial.println(average_sg) ; 

    if (average_sg < threshold[motorId]) {
      break;
    }
  }
}


// First set of 3 functions

void moveToPosition(long x, long y) {
  if (x >= 0 && y >= 0 && x <= 380 && y <= 400) {
    long Dx = currentPos[0] - x ;
    long Dy = currentPos[1] - y ;
    boolean dir_x ;
    boolean dir_y ;

    if (Dx > 0) {
      dir_x = hommingDir[0]; // go to home
    }
    else {
      dir_x = !hommingDir[0]; // go opposite to home
    }

    if (Dy > 0) {
      dir_y = hommingDir[1]; // go to home
    }
    else {
      dir_y = !hommingDir[1]; // go opposite to home
    }

    moveAccordingToDistance(abs(Dx), MOTOR_X, dir_x); 
    moveAccordingToDistance(abs(Dy), MOTOR_Y, dir_y); 

  }
  else {
    Serial.print("x coordinate must be at range 0-380 and y at 0-400: "); 
    Serial.print(x);
    Serial.print(" ");
    Serial.println(y); 
  }

}

void moveToHor (long x) {
  if (x >= 0 && x <= 380) {
    long Dx = currentPos[0] - x ;
    boolean dir_x ;
    if (Dx > 0) {
      dir_x = hommingDir[0]; // go to home
    }
    else {
      dir_x = !hommingDir[0]; // go opposite to home
    }
    moveAccordingToDistance(abs(Dx), MOTOR_X, dir_x); // use of abs()

  }
  else {
    Serial.println("x must be at range 0-380");
  }
}

void moveToVer(long y) {
  if (y >= 0 && y <= 400) {
    long Dy = currentPos[1] - y ;
    boolean dir_y ;
    if (Dy > 0) {
      dir_y = hommingDir[1]; // go to home
    }
    else {
      dir_y = !hommingDir[1]; // go opposite to home
    }

    moveAccordingToDistance(abs(Dy), MOTOR_Y, dir_y); 
  }
  else {
    Serial.println("y must be at range 0-400");
  }
}

// Second set of 3 functions

void moveBothBy(long x, long y) {
  boolean dir_x ;
  boolean dir_y ;

  if (x > 0) {
    dir_x = !hommingDir[0]; // go opposite to home
  }
  else {
    dir_x = hommingDir[0]; // go to home
  }

  if (y > 0) {
    dir_y = !hommingDir[1]; // go opposite to home
  }
  else {
    dir_y = hommingDir[1]; // go to home
  }

  moveAccordingToDistance(abs(x), MOTOR_X, dir_x); // use of abs()
  moveAccordingToDistance(abs(y), MOTOR_Y, dir_y); // use of abs()

  // maybe MUST check always while moving if it gets a obstacle !!
}

void moveHorBy(long x) {

  boolean dir_x;
  if (x > 0) {
    dir_x = !hommingDir[0]; // go opposite to home
  }
  else {
    dir_x = hommingDir[0]; // go to home
  }
  moveAccordingToDistance(abs(x), MOTOR_X, dir_x); // use of abs()

  // maybe MUST check always while moving if it gets a obstacle !!
}

void moveVerBy(long y) {

  boolean dir_y ;
  if (y > 0) {
    dir_y = !hommingDir[1]; // go opposite to home
  }
  else {
    dir_y = hommingDir[1]; // go to home
  }
  moveAccordingToDistance(abs(y), MOTOR_Y, dir_y);

  // maybe MUST check always while moving if it gets a obstacle !!

}


///////////////////////////////////////////////////////////////
///////// Cupboard Motor functionalities //////////////////////
///////////////////////////////////////////////////////////////

void moveCupboardToPosition(long x) {
  if (x >= 0 && x <= 420) {
    long Dx = currentPos[2] - x ;
    boolean dir_x ;
    if (Dx > 0) {
      dir_x = hommingDir[2]; // go to home
    }
    else {
      dir_x = !hommingDir[2]; // go opposite to home
    }

    moveAccordingToDistance(abs(Dx), MOTOR_D, dir_x);

  }
  else {
    Serial.print("x coordinate must be at range 0-380");
    Serial.print(x);
  }
}


void moveCupboardBy(long x) {
  boolean dir_x ;
  if (x > 0) {
    dir_x = !hommingDir[2]; // go opposite to home
  }
  else {
    dir_x = hommingDir[2]; // go to home
  }
  moveAccordingToDistance(abs(x), MOTOR_D, dir_x);
}


void checkDoorStatusChanges(String doorStatus_current , String doorStatus_new){
  if (doorStatus_new != doorStatus_current){
    Serial.print("DoorStatus,");                      // WRITE // 
    Serial.println(doorStatus_new); // write the doorStatus change event in the serial buffer
  }
}

void executionCompleted(String command){
    Serial.print("ExecOk,");
    Serial.println(command); // write that ExecutionCompleted
}


void setup() {

  Serial.begin(115200); // baud rate of Arduino Motor = 115200
  while (!Serial);              // Wait for serial port to connect


  // Set up distance sensor Adafruit VL6180 
  Serial.println("Adafruit VL6180x test!"); 
  if (! vl.begin()) {
    Serial.println("Failed to find sensor"); 
    while (1);
  }
  Serial.println("Sensor found!"); 

  // end of setup of distance sensor Adafruit VL6180

  setupMotorDriver(MOTOR_X);
  setupMotorDriver(MOTOR_Y);
  setupMotorDriver(MOTOR_D);

  doorStatus_before = "Closed" ; 
  
  Serial.print("DoorStatus,"); 
  Serial.println(doorStatus_before); // write the doorStatus change event in the serial buffer
  
  
  Serial.flush() ; // wait until all the data is written in the serial buffer
}


void loop() {

  //////     READ  //////

  //Serial.available() -------> Get the number of bytes (characters) available for reading from the serial port.
  //This is data that’s already arrived and stored in the serial receive buffer (which holds 64 bytes).

  if (Serial.available() > 0) { // see above comments --- if there are data to READ
    InputString = Serial.readString();

    String firstToken = getSubstring(InputString, '_', 0);
    String secondToken = getSubstring(InputString, '_', 1);
    String thirdToken = getSubstring(InputString, '_', 2); // if input : moveToHor_300 then thirdToken = 0

    if (firstToken == "moveHorBy") {
      moveHorBy(secondToken.toInt());
      executionCompleted(firstToken);
    }
    else if (firstToken == "moveVerBy") {
      moveVerBy(secondToken.toInt());
      executionCompleted(firstToken);
    }
    else if (firstToken == "moveBothBy") {
      moveBothBy(secondToken.toInt() , thirdToken.toInt());
      executionCompleted(firstToken);
    }
    else if (firstToken == "moveToPosition") {
      moveToPosition(secondToken.toInt() , thirdToken.toInt());
      executionCompleted(firstToken);
    }
    else if (firstToken == "moveToHor") {
      moveToHor(secondToken.toInt());
      executionCompleted(firstToken);
    }
    else if (firstToken == "moveToVer") {
      moveToVer(secondToken.toInt());
      executionCompleted(firstToken);
    }
    else if (firstToken == "cameraHoming") { 
      moveAccordingToDistance(30, MOTOR_X, true);
      moveAccordingToDistance(30, MOTOR_Y, false);
      motor_homing(MOTOR_Y);
      motor_homing(MOTOR_X);
      executionCompleted(firstToken);
    }
    
    ////////////////////////////////////////////////////////////////////////////////////////////////////
    else if (firstToken == "cupboardHoming") { 
      doorStatus_after = "Closed" ;  
      checkDoorStatusChanges(doorStatus_before,doorStatus_after); 
      doorStatus_before = doorStatus_after ; 
    
      motor_homing(MOTOR_D);
      executionCompleted(firstToken);
    }
    else if (firstToken == "openTotally" && doorStatus_before != "Opened") {
      doorStatus_after = "Moving" ;  
      checkDoorStatusChanges(doorStatus_before,doorStatus_after);
      doorStatus_before = doorStatus_after ; // update
      moveCupboardToPosition(420);
      doorStatus_after = "Opened" ; 
      checkDoorStatusChanges(doorStatus_before,doorStatus_after);
      doorStatus_before = doorStatus_after ; // update
      executionCompleted(firstToken);
    }
    else if (firstToken == "closeTotally" && doorStatus_before != "Closed") {
      doorStatus_after = "Moving" ;  
      checkDoorStatusChanges(doorStatus_before,doorStatus_after);
      doorStatus_before = doorStatus_after ; // update 
      moveCupboardToPosition(0); // not 0 !! 
      doorStatus_after = "Closed" ;  
      checkDoorStatusChanges(doorStatus_before,doorStatus_after);
      doorStatus_before = doorStatus_after ; // update 
      executionCompleted(firstToken);
    }
    else if (firstToken == "moveCupboardBy") {
      doorStatus_after = "Moving" ; 
      checkDoorStatusChanges(doorStatus_before,doorStatus_after);
      doorStatus_before = doorStatus_after ; // update 
      moveCupboardBy(secondToken.toInt());
      doorStatus_after = "Opened" ;  
      checkDoorStatusChanges(doorStatus_before,doorStatus_after);
      doorStatus_before = doorStatus_after ; // update
      executionCompleted(firstToken);
    }
    else if (firstToken == "moveCupboardTo") {
      doorStatus_after = "Moving" ; 
      checkDoorStatusChanges(doorStatus_before,doorStatus_after);
      doorStatus_before = doorStatus_after ; // update 
      moveCupboardToPosition(secondToken.toInt());
      doorStatus_after = "Opened" ;  
      checkDoorStatusChanges(doorStatus_before,doorStatus_after);
      doorStatus_before = doorStatus_after ; // update 
      executionCompleted(firstToken);
    }
    else if (firstToken == "semiOpen" && doorStatus_before != "Semi-opened") {
      doorStatus_after = "Moving" ;  
      checkDoorStatusChanges(doorStatus_before,doorStatus_after);
      doorStatus_before = doorStatus_after ; // update 
      moveCupboardToPosition(200) ; // 20 cm open --- maybe change that !
      doorStatus_after = "Semi-opened" ; 
      checkDoorStatusChanges(doorStatus_before,doorStatus_after);
      doorStatus_before = doorStatus_after ; // update 
      executionCompleted(firstToken);
    }
    else if (firstToken == "getDoorPosition" ) { 
      showPos() ; 
    }
  }
} // end of void loop()