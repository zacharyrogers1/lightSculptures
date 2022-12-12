#include <Arduino.h>
#include <FastLED.h>

#define NUM_LEDS 400
#define DATA_PIN 27
#define CHIPSET WS2811Controller800Khz
#define BRIGHTNESS 128
#define COLOR_CORRECTION TypicalPixelString
#define ONBOARD_LED 2

CRGB leds[NUM_LEDS];

void setup()
{
  pinMode(ONBOARD_LED, OUTPUT);
  pinMode(DATA_PIN, OUTPUT);
  Serial.begin(115200);
  FastLED.addLeds<CHIPSET, DATA_PIN, RGB>(leds, NUM_LEDS);
  FastLED.setBrightness(BRIGHTNESS);
  FastLED.setCorrection(COLOR_CORRECTION); // After some experimenting TypicalPixelString matches the white color correction best
}

void loop()
{
  fill_solid(leds, NUM_LEDS, CRGB::Blue);
  digitalWrite(ONBOARD_LED, HIGH);
  FastLED.show();
  delay(1000);
  fill_solid(leds, NUM_LEDS, CRGB::Red);
  digitalWrite(ONBOARD_LED, LOW);
  FastLED.show();
  delay(1000);
}

