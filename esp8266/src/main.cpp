#include <Arduino.h>
#include <FastLED.h>

#define NUM_LEDS 400
#define DATA_PIN 12
#define CHIPSET WS2811Controller800Khz
#define BRIGHTNESS 128
#define COLOR_CORRECTION TypicalPixelString

CRGB leds[NUM_LEDS];
void setup()
{
  Serial.begin(9600);
  FastLED.addLeds<CHIPSET, DATA_PIN, RGB>(leds, NUM_LEDS);
  FastLED.setBrightness(BRIGHTNESS);
  FastLED.setCorrection(COLOR_CORRECTION); // After some experimenting TypicalPixelString matches the white color correction best
}



void loop()
{
  fill_solid(leds, NUM_LEDS, CRGB::Blue);
}