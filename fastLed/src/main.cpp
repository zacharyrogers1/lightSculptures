#include <Arduino.h>
#include <FastLED.h>
#include <animations.h>

#define NUM_LEDS 400
#define DATA_PIN 10
#define CHIPSET WS2811Controller800Khz
#define BRIGHTNESS 128
#define COLOR_CORRECTION TypicalPixelString

CRGB leds[NUM_LEDS];

uint8_t hue = 0;

void setup()
{
  Serial.begin(9600);
  FastLED.addLeds<CHIPSET, DATA_PIN, RGB>(leds, NUM_LEDS);
  FastLED.setBrightness(BRIGHTNESS);
  FastLED.setCorrection(COLOR_CORRECTION); // After some experimenting TypicalPixelString matches the white color correction best
}



void loop()
{
  rainbow_march(100, 10, leds, 400);
  FastLED.show();
}
