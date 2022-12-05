#include <Arduino.h>
#include <FastLED.h>


void rainbow_march(uint8_t thisdelay, uint8_t deltahue, CRGB *leds, int NUM_LEDS)
{ // The fill_rainbow call doesn't support brightness levels.

  uint8_t thishue = millis() * (255 - thisdelay) / 255; // To change the rate, add a beat or something to the result. 'thisdelay' must be a fixed value.

  // thishue = beat8(50);                                       // This uses a FastLED sawtooth generator. Again, the '50' should not change on the fly.
  // thishue = beatsin8(50,0,255);                              // This can change speeds on the fly. You can also add these to each other.

  fill_rainbow(leds, NUM_LEDS, thishue, deltahue); // Use FastLED's fill_rainbow routine.
  // fill_solid()
}