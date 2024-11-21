#include <FastLED.h>

#define NUM_LEDS 14       
#define DATA_PIN 2        
#define BRIGHTNESS 100    
#define DELAY_TIME 10     
#define RAINBOW_STEP 10   
#define COLORWIPE_STEP 5  
#define SPARKLE_PROB 2   
#define MAX_NUM_COLOR 255 
#define BAUDRATE 960
#define READY "Ready"
#define NOT_PROGRES false
#define PROGRES true

CRGB leds[NUM_LEDS];       
char lastCommand = '0';   
bool commandInProgress = false; 
int currentEffect = -1;  

void checkSerialInput();
void handleRGBCommand(String command);
void handleEffectCommand(String command);
void runEffect();
void setColor(int r, int g, int b);
void rainbow();
void pulse();
void colorWipe();
void randomSparkle();
void colorChase();

void setup() 
{
  FastLED.addLeds<WS2812, DATA_PIN, GRB>(leds, NUM_LEDS).setCorrection(TypicalLEDStrip);
  FastLED.setBrightness(BRIGHTNESS);
  Serial.begin(BAUDRATE);
  Serial.println(READY);
}


void loop() 
{
  checkSerialInput(); // Check for commands from Serial input

  if (commandInProgress) 
  {
    runEffect();
  }
}

// Checks for incoming commands via Serial
void checkSerialInput()
 {
  if (Serial.available() > 0) 
  {
    String command = Serial.readStringUntil('\n');

    if (command.startsWith("rgb:")) 
    {
      handleRGBCommand(command);
    } 
    else if (command.length() > 0) 
    {
      handleEffectCommand(command);
    }
  }
}

// Handles RGB color commands
void handleRGBCommand(String command) 
{
  int r = 0;
  int g = 0;
  int b = 0;
  sscanf(command.c_str(), "rgb:%d,%d,%d", &r, &g, &b); // Extract RGB values
  setColor(r, g, b); // Set the LED color
  commandInProgress = false; // Stop the current effect
}

// Handles commands to select an effect
void handleEffectCommand(String command) 
{
  lastCommand = command.charAt(0); // Store the command
  commandInProgress = PROGRES;       // Set the active flag
  currentEffect = lastCommand - '0'; // Convert command to effect ID
}


/* 
Executes the current effect
Time Complexity: O(1)
*/
void runEffect() 
{
  switch (currentEffect)
   {
    case 1: rainbow(); break;
    case 2: pulse(); break;
    case 3: colorWipe(); break;
    case 4: randomSparkle(); break;
    case 5: colorChase(); break;
    default: commandInProgress = NOT_PROGRES; break;
  }
}


/* 
Sets the color of all LEDs
all leds will display same color as degined by the parametrs r (red), g(green),and b (blue)
Time Complexity: O(NUM_LEDS)
*/

void setColor(int r, int g, int b) 
{
  int i = 0;
  for (i = 0; i < NUM_LEDS; i++)
  {
    leds[i] = CRGB(r, g, b);
  }
  FastLED.show(); 
}

/* 
Creates a rainbow effect
Time Complexity: O(NUM_LEDS)
*/
void rainbow()
{
  int i = 0;
  static uint8_t hue = 0;
  for (i = 0; i < NUM_LEDS; i++) 
  {
    leds[i] = CHSV(hue + (i * RAINBOW_STEP), MAX_NUM_COLOR, MAX_NUM_COLOR);
  }
  FastLED.show();
  delay(DELAY_TIME);
  hue++;
}


/* 
Creates a pulsing effect by changing brightness
Time Complexity: O(NUM_LEDS)
*/
void pulse()
 {
  static int brightness = 0;
  static bool increasing = true;
  int i = 0;
  for (i = 0; i < NUM_LEDS; i++)
   {
    leds[i] = CRGB(brightness, 0, 0); // Red with current brightness
  }
  FastLED.show();

  if (increasing) 
  {
    brightness++;
    if (brightness == MAX_NUM_COLOR) increasing = false;
  } 
  else
  {
    brightness--;
    if (brightness == 0) increasing = true;
  }
  delay(DELAY_TIME);
}

/*
 Creates a wiping effect by cycling through colors
Time Complexity: O(NUM_LEDS)
 */
void colorWipe()
 {
  static int colorIndex = 0;
  int i = 0;
  for (i = 0; i < NUM_LEDS; i++)
  {
    leds[i] = CHSV(colorIndex, MAX_NUM_COLOR, MAX_NUM_COLOR);
  }
  FastLED.show();

  colorIndex += COLORWIPE_STEP;
  if (colorIndex >= MAX_NUM_COLOR) colorIndex = 0;
  delay(DELAY_TIME);
}


/* 
Creates a random sparkle effect
// Time Complexity: O(NUM_LEDS)
*/
void randomSparkle()
{
  int i = 0;
  for (i = 0; i < NUM_LEDS; i++) 
  {
    if (random(100) < SPARKLE_PROB) 
    {
       // Probability check
      leds[i] = CRGB(MAX_NUM_COLOR, MAX_NUM_COLOR, MAX_NUM_COLOR); // White color
    } 
    else
    {
      leds[i] = CRGB(0, 0, 0); // Turn off LED
    }
  }
  FastLED.show();
  delay(DELAY_TIME);
}

/* 
Creates a chasing light effect
Time Complexity: O(NUM_LEDS)
*/
void colorChase() 
{
  static int position = 0;
  int i = 0;
  for (i = 0; i < NUM_LEDS; i++) 
  {
    leds[i] = (i == position) ? CRGB(MAX_NUM_COLOR, 0, 0) : CRGB(0, 0, 0);
  }
  FastLED.show();

  position++;
  if (position >= NUM_LEDS) position = 0;
  delay(DELAY_TIME);
}
