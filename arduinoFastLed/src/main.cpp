#include <Arduino.h>
#include <FastLED.h>
#include "animations.h"
#include "matrixLights.h"

#define NUM_LEDS 400
#define DATA_PIN 10
#define CHIPSET WS2811Controller800Khz
#define BRIGHTNESS 128
#define COLOR_CORRECTION TypicalPixelString

CRGB leds[NUM_LEDS];
MatrixLights myLights = MatrixLights(20, 20, leds);

void setup()
{
  Serial.begin(9600);
  FastLED.addLeds<CHIPSET, DATA_PIN, RGB>(leds, NUM_LEDS);
  FastLED.setBrightness(BRIGHTNESS);
  FastLED.setCorrection(COLOR_CORRECTION); // After some experimenting TypicalPixelString matches the white color correction best

}



void loop()
{
  myLights.setColor(CRGB::Blue);
  myLights.setColor(CRGB::Red);
}
