#include <Arduino.h>
#include <FastLED.h>

#define NUM_LEDS 400
#define DATA_PIN 10
CRGB leds[NUM_LEDS];

void setup()
{
  Serial.begin(9600);
  FastLED.addLeds<WS2811, DATA_PIN, RGB>(leds, NUM_LEDS);
  FastLED.setBrightness(50);
}

void loop()
{
  // leds[0] = CRGB::Red;
  leds[1] = CRGB::Green;
  // leds[2] = CRGB::Blue;
  FastLED.show();
}