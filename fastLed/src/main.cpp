#include <Arduino.h>
#include <FastLED.h>

#define NUM_LEDS 60
#define DATA_PIN 6
CRGB leds[NUM_LEDS];

void setup()
{
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
  FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, NUM_LEDS);
}

void loop()
{
  digitalWrite(LED_BUILTIN, HIGH); // turn the LED on (HIGH is the voltage level)
  Serial.println(millis());
  delay(1000);                    // wait for a second
  digitalWrite(LED_BUILTIN, LOW); // turn the LED off by making the voltage LOW
  Serial.println("LOW");
  delay(1000); // wait for a second
}