#include <Arduino.h>
#include <FastLED.h>

#define NUM_LEDS 400
#define DATA_PIN 10
CRGB leds[NUM_LEDS];

uint8_t hue = 0;

void setup()
{
  Serial.begin(9600);
  FastLED.addLeds<WS2811Controller800Khz, DATA_PIN, RGB>(leds, NUM_LEDS);
  FastLED.setBrightness(128);
  FastLED.setCorrection(TypicalPixelString); // After some experimenting TypicalPixelString matches the white color correction best

}

void loop()
{
  fill_solid(leds, NUM_LEDS, CRGB::White);
  FastLED.show();
}