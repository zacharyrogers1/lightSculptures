#include <Arduino.h>
#include <FastLED.h>

class MatrixLights
{
public:
  uint8_t width;
  uint8_t height;
  struct CRGB *leds;
  MatrixLights(uint8_t width, uint8_t height, struct CRGB *leds);
  ~MatrixLights();

  void setColor(CRGB::HTMLColorCode color);
};

MatrixLights::MatrixLights(uint8_t width, uint8_t height, struct CRGB *leds)
{
  this->height = height;
  this->width = width;
  this->leds = leds;
}

MatrixLights::~MatrixLights()
{
}

void MatrixLights::setColor(CRGB::HTMLColorCode color) {
  fill_solid(this->leds, this->width*this->height, color);
  FastLED.show();
}