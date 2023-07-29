#include "Adafruit_MPR121.h" // touch sensor
#include <Adafruit_NeoPixel.h> // leds
#include <Q2HX711.h> // weight sensor

const int NUMPIXELS_LED1 = 22;  // how many leds are on the Led Stripe 1
const int NUMPIXELS_LED2 = 150; // how many leds are on the Led Stripe 2 ---> change to 113
const long TOUCH_THRESHOLD = 80 ; // threshold
const long WEIGHT_THRESHOLD = 10 ; // threshold weight
const int CAP_SENSOR_ID = 0; // first touch sensor
const int DELAYVAL = 400;       // in milliseconds
long const A = 414.663461538 ; //weight
long const B = 8595500 ; // weight 

const int vibrPin = 3;
const int led1Pin = 4;
const int led2Pin = 8;
const int proximityPin = 5; // CHANGE THAT IF NEEDED !!!!

String InputString;
int touchState_before;
int touchState_after; 

int proximityState_before ; 
int proximityState_after ; 

int scaleStatus_before ; 
int scaleStatus_after ; 

bool learningOn; 
int currentLed ; 

Adafruit_MPR121 cap = Adafruit_MPR121(); // pins SDA:A4, SCL:A5

Adafruit_NeoPixel ledStripe[2] = {Adafruit_NeoPixel(NUMPIXELS_LED1, led1Pin, NEO_GRB + NEO_KHZ800), // front door led stripe (small one)
                                  Adafruit_NeoPixel(NUMPIXELS_LED2, led2Pin, NEO_GRB + NEO_KHZ800)
                                 }; // shelf led stripe (big one)

Q2HX711 hx711(6, 7); // weight sensor pins DT:A2, SCK:A3    CHANGE THAT IF NEEDED !!!!


uint32_t RGB2Color(uint8_t r, uint8_t g, uint8_t b)
{
  return ((uint32_t)r << 16) | ((uint32_t)g << 8) | b;
}

uint32_t red = RGB2Color(128, 0, 0);
uint32_t yellow = RGB2Color(128, 69, 0); // orange
uint32_t green = RGB2Color(0, 128, 0);
uint32_t blue = RGB2Color(0, 0, 128);

void setup()
{
  learningOn = false; // initialize 
  currentLed = 21 ; // initialize

  Serial.begin(9600);
  pinMode(led1Pin, OUTPUT);
  pinMode(led2Pin, OUTPUT);
  pinMode(vibrPin, OUTPUT);
  pinMode(proximityPin, INPUT);

  // Default address is 0x5A, if tied to 3.3V its 0x5B
  // If tied to SDA its 0x5C and if SCL then 0x5D
  if (!cap.begin(0x5A)) {
    Serial.println("MPR121 not found, check wiring?");
    while (1);
  }
  Serial.println("MPR121 found!"); // why this line is printed twice ?

  // give some time to load and cap to start
  delay(500);

  ledStripe[0].begin(); // INITIALIZE NeoPixel strip object (REQUIRED)
  ledStripe[1].begin(); // INITIALIZE NeoPixel strip object (REQUIRED)

  ledStripe[0].clear();
  ledStripe[0].show(); 

  ledStripe[1].clear(); 
  ledStripe[1].show(); 
}

void loop()
{

    //weight
    scaleStatus_after = addRemoveItemCheck() ;
    if (scaleStatus_after != scaleStatus_before){
        Serial.print("ScaleStatus,");
        Serial.println(scaleStatus_after);    
    }

    scaleStatus_before = scaleStatus_after ; 
    
// Proximity
  proximityState_after = proximityCheck(); // read proximity sensor - ALWAYS


  if (proximityState_after != proximityState_before) { // if there was a change-event in the proximity sensor then send that info to RPI
    Serial.print("ProximityStatus,");
    Serial.println(proximityState_after); // always write in serial buffer the change-proximityEvent
  }

  proximityState_before = proximityState_after ; // update variables


//Touch
  touchState_after = touchSensorGetStatus(); // read touch sensor - ALWAYS


  if (touchState_after != touchState_before) { // if there was a change-event in the touch sensor then send that info to RPI
    Serial.print("TouchSensorState,");
    Serial.println(touchState_after); // always write in serial buffer the change-touchEvent
  }

  touchState_before = touchState_after ; // update variables

  if (Serial.available() > 0) // get the number of bytes in the receive buffer
  {
    InputString = Serial.readStringUntil(';'); // read the bytes as string

    Serial.print("InputString is : "); 
    Serial.println(InputString) ; 

    String firstToken = getSubstring(InputString, '_', 0);
    String secondToken = getSubstring(InputString, '_', 1);
    String thirdToken = getSubstring(InputString, '_', 2);
    String forthToken = getSubstring(InputString, '_', 3);
    String fifthToken = getSubstring(InputString, '_', 4);
    String sixthToken = getSubstring(InputString, '_', 5); 
    String seventhToken = getSubstring(InputString, '_', 6); 
    
    Serial.print("Command : [");
    Serial.print(firstToken);
    Serial.println("]");

    Serial.print("arg1 : [");
    Serial.print(secondToken);
    Serial.println("]");
    
    if (firstToken == "lightSpecificLed") // lightSpecificLed_12_0_red_
    {
      lightSpecificLedId(secondToken.toInt(), thirdToken.toInt(), string2Color(forthToken)); // int ledId,  int ledStripeId, uint32_t color,
    }
    else if (firstToken == "switchoff") // switchoff_0
    {
      switchoff(secondToken.toInt()); // ledStripeID
    }
    else if (firstToken == "c1") // lightConstantFromToLedIDs_4_15_red_0
    {
      lightUp_seirial(secondToken.toInt(), thirdToken.toInt(), string2Color(forthToken), 0, fifthToken.toInt());
      // startLed, int endLed, uint32_t color, long duration, int ledStripeID
    }
    else if (firstToken == "lightConstantlyShelf") // lightConstantlyShelf_up_green_
    {
      lightSpecificShelf_Constant(secondToken, string2Color(thirdToken)); // (String Shelf, uint32_t color)
    }
    else if (firstToken == "lightConstantDoor") // lightConstantDoor_green_
    {
      lightFrontDoor_Constant(string2Color(secondToken));
    }
    else if (firstToken == "lightLedByLed") // only for the DOOR // lightLedByLed_12_blue_4000
    {
      lightLedByLed(secondToken.toInt(), string2Color(thirdToken), forthToken.toInt()); // (int reachLed, uint32_t color, long duration)
      // duration in msec
    }


    else if (firstToken == "vibSteady") // vibSteady_2000
    {
      vibrateSteady(secondToken.toInt()); // VibrationDuration
    }
    else if (firstToken == "vibPeriodically") // vibPeriodically_5000_6000
    {
      vibratePeriodically(secondToken.toInt(), thirdToken.toInt()); // vibratePeriodically(long vibrationDuration, long EventDuration)
    }
    else if (firstToken == "vibTimes") // vibTimes_3_2000
    {
      vibrateSpecificNumberOfTimes(secondToken.toInt(), thirdToken.toInt()); // times , vibrationDuration
    }
    else if (firstToken == "touchStatus") // TOUCH touchStatus_
    {
      Serial.print("TouchSensorState," );
      Serial.println(touchSensorGetStatus());
    }
    else if (firstToken == "weightStatus") // weight // weightStatus_
    {
      long y = hx711.read() ;
      long weight_load = calcWeight(y) ;

      Serial.print("WeightStatus,");
      Serial.println(weight_load);
    }
    else if (firstToken == "proximityStatus") // proximity // proximityStatus_
    {
      Serial.print("ProximityStatus,");
      Serial.println(proximityCheck());
    }
    else if (firstToken == "lightOneMoreLed") // only for the DOOR // lightLedByLed_12_blue_4000
    {
      doorLightSolidLeds(secondToken.toInt());
    }
    else if (firstToken == "c2"){ 
      doorLearningInterruption();
    }
    else if (firstToken == "blinkSomeLeds"){
      blinkingSomeLeds(secondToken.toInt(), thirdToken.toInt(),string2Color(forthToken), fifthToken.toInt(), sixthToken.toInt(),seventhToken.toInt());
    }
    else if (firstToken == "setLearning"){ 
      setLearning(secondToken); 
    else {
      Serial.print("Error ... : "); 
    }
  }
  if (learningOn){
    blinkingLed(currentLed,yellow,1000,0);
  }
}



uint32_t string2Color(String color)
{
  if (color.equals("red"))
  {
    return red;
  }
  else if (color == "blue")
  {
    return blue;
  }
  else if (color == "green")
  {
    return green;
  }
  else if (color == "yellow")
  {
    return yellow;
  }
  else
  {
    Serial.println("ERROR_ColorError"); // debug
    Serial.print("color is ["); //debug
    Serial.print(color); //debug
    Serial.println("]") ;
  }
}


void lightSpecificShelf_Constant(String Shelf, uint32_t color)
{
  if (Shelf == "up")
  {
    lightUp_seirial(1, 56, color, 0, 1);
  }
  else if (Shelf = "down")
  {
    lightUp_seirial(57, 113, color, 0, 1);
  }
}

void lightFrontDoor_Constant(uint32_t color)
{
  lightUp_seirial(1, NUMPIXELS_LED1, color, 0, 0);
}


void lightSpecificLedId(int ledId, int ledStripeId, uint32_t color)
{
  ledStripe[ledStripeId].setPixelColor(ledId, color);
  ledStripe[ledStripeId].show();
}

void lightUp_seirial(int startLed, int endLed, uint32_t color, long duration, int ledStripeID)
{
  ledStripe[ledStripeID].clear(); // be sure that it is off

  int NumLightingLeds = abs(startLed - endLed);
    if (NumLightingLeds == 0) { 
    ledStripe[ledStripeID].setPixelColor(startLed, color); 
    ledStripe[ledStripeID].show();
  } 
  else{
    long ledDelay = duration / NumLightingLeds; // SOS HERE ... DIVIZION WITH ZERO !!

  if (startLed <= endLed)
  {
    for (int i = startLed; i < endLed; i++)
    {
      ledStripe[ledStripeID].setPixelColor(i, color);
      ledStripe[ledStripeID].show();
      delay(ledDelay);
    }
  }
  else
  {
    for (int i = startLed; i > endLed; i--)
    {
      ledStripe[ledStripeID].setPixelColor(i, color);
      ledStripe[ledStripeID].show();
      delay(ledDelay);
    }
  }
  }
}

void switchoff(int ledStripeID)
{
  ledStripe[ledStripeID].clear();
  ledStripe[ledStripeID].show();
}

void lightUpToPoint(int reachLed, boolean dir, uint32_t color, long duration)
{
  long delayLed = 2 * (duration / NUMPIXELS_LED1);

  ledStripe[0].clear(); // be sure that it is off

  ledStripe[0].setPixelColor(reachLed, color);
  ledStripe[0].show();
  delay(DELAYVAL);

  if (dir)
  {
    int currentLedLeft = reachLed + 1;
    int currentLedRight = reachLed - 1;

    while (currentLedLeft <= NUMPIXELS_LED1 || currentLedRight >= 0)
    {
      ledStripe[0].setPixelColor(currentLedRight, color);
      ledStripe[0].setPixelColor(currentLedLeft, color);
      ledStripe[0].show();
      delay(delayLed);
      currentLedLeft++;
      currentLedRight--;
    }
  }

  else
  {
    int currentLedRight = 0;
    int currentLedLeft = NUMPIXELS_LED1 - 1; // caution !

    while (currentLedLeft >= reachLed && currentLedRight <= reachLed)
    {
      ledStripe[0].setPixelColor(currentLedLeft, color);
      ledStripe[0].setPixelColor(currentLedRight, color);
      ledStripe[0].show();
      delay(delayLed);
      currentLedRight++;
      currentLedLeft--;
    }
    if (currentLedLeft < reachLed)
    { 
      while (currentLedRight <= reachLed)
      {
        ledStripe[0].setPixelColor(currentLedRight, color);
        ledStripe[0].show();
        delay(delayLed);
        currentLedRight++;
      }
    }
    else if (currentLedRight > reachLed) 
    {
      while (currentLedLeft >= reachLed)
      {
        ledStripe[0].setPixelColor(currentLedLeft, color);
        ledStripe[0].show();
        delay(delayLed);
        currentLedLeft--;
      }
    }
    else
    {
      // do nothing here
    }
  }
}

void lightLedByLed(int reachLed, uint32_t color, long duration) // duration in msec
{
  // Serial.println("Arduino : I am in lightLedByLed function");// debug
  long delayLed = (duration / reachLed);

  for (int pixelID = 1; pixelID <= reachLed; pixelID++)
  {
    ledStripe[0].setPixelColor(pixelID, color);
    ledStripe[0].show();
    ledStripe[0].clear();
    delay(delayLed);
  }
  ledStripe[0].show(); // push the switch off command
}


String getSubstring(String data, char separator, int index)
{
  int found = 0;
  int strIndex[] = {0, -1};
  int maxIndex = data.length() - 1;

  for (int i = 0; i <= maxIndex && found <= index; i++)
  {
    if (data.charAt(i) == separator || i == maxIndex)
    {
      found++;
      strIndex[0] = strIndex[1] + 1;
      strIndex[1] = (i == maxIndex) ? i + 1 : i;
    }
  }
  return found > index ? data.substring(strIndex[0], strIndex[1]) : "kati";
}




// Vibrator
void vibrateSteady(long VibrationDuration)
{  
  analogWrite(vibrPin, 125); // with 50% power
  delay(VibrationDuration);
  analogWrite(vibrPin, 0); // turn it OFF
  delay(1000);
}

void vibratePeriodically(long periodDuration, long EventDuration)
{
  unsigned long time_start = millis();

  while (millis() < time_start + EventDuration)
  {
    unsigned long time_now = millis();
    while (millis() < time_now + periodDuration)
    {
      analogWrite(vibrPin, 255); // with 100% power
    }
    analogWrite(vibrPin, 0); // turn it OFF
    unsigned long time_delay = millis();
    while (millis() < time_delay + periodDuration)
      ; // do nothing -- just wait
  }
}

void vibrateSpecificNumberOfTimes(int times, long vibrationDuration)
{
  for (int count = 1; count <= times; count++)
  {
    vibrateSteady(vibrationDuration);
  }
}





// Touch sensor
int touchSensorGetStatus()
{
  int touchState ; // 0 or 1
  long capacityData =  cap.filteredData(CAP_SENSOR_ID);

  if (capacityData < TOUCH_THRESHOLD) {
    return touchState = 0 ; // touched
  }
  else {
    return touchState = 1 ; // not touched
  }
}

// Weight
long calcWeight(long y) {
  return round((y - B) / A);
}

int addRemoveItemCheck(){
    int isLoaded ; // 0 or 1 
    long weightResult = calcWeight(hx711.read());
    if (weightResult > WEIGHT_THRESHOLD){
        return isLoaded = 0 ; // there is something on it 
    }
    else{
        return isLoaded = 1 ; // no. there is nothing on it -- empty
    }
}

// Proximity
int proximityCheck() {
  return digitalRead(proximityPin) ;
}


void blinkingLed(int ledId, uint32_t color, long duration, int ledstripeId){
    ledStripe[ledstripeId].setPixelColor(ledId , RGB2Color(0, 0, 0)); // switch it off RGB2Color(0, 0, 0)
    ledStripe[ledstripeId].show();
    delay(duration); //ms
    ledStripe[ledstripeId].setPixelColor(ledId , color);
    ledStripe[ledstripeId].show();
    delay(duration); //ms
    }

void doorLearningInterruption(){ // light up door with red color for 3 seconds 
  lightFrontDoor_Constant(red);
  delay(3000);
  switchoff(0);
  lightUp_seirial(21,currentLed,yellow,0,0);
}

void doorLightSolidLeds(int targetLed){ // for learning
  currentLed = targetLed ; // SOS before calling lightup_seirial !
  lightUp_seirial(21,currentLed,yellow,0,0) ; 
}

void blinkingSomeLeds(int startlLedId, int endLedId, uint32_t color, long TotalEventDuration, long BlinkingDuration, int ledstripeId)
{
    unsigned long startTime = millis();
    unsigned long endTime = startTime ;
    while (endTime - startTime <= TotalEventDuration)
    {
        ledStripe[ledstripeId].clear();
        ledStripe[ledstripeId].show();
        delay(BlinkingDuration); // ms

        lightUp_seirial(startlLedId, endLedId, color, 0, ledstripeId);
        delay(BlinkingDuration); // ms

        endTime = millis();
    }
    ledStripe[ledstripeId].clear(); // be sure that lights are off when function ends
    ledStripe[ledstripeId].show();
}

void setLearning(String status){
   
  if (status == "on"){
    Serial.println("learn T") ; 
    learningOn = true ; 
  }
  else if (status == "off"){
    Serial.println("learn F") ; 
    learningOn = false ;
    ledStripe[0].clear(); // be sure that lights are off when function ends
    ledStripe[0].show();
  }
  else {
    Serial.println("problem"); 
  }
}

// serial print variable type
void types(String a) { Serial.println("it's a String"); }
void types(int a) { Serial.println("it's an int"); }
void types(char *a) { Serial.println("it's a char*"); }
void types(float a) { Serial.println("it's a float"); }
void types(bool a) { Serial.println("it's a bool"); }