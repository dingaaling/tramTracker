#include <Adafruit_NeoPixel.h>

#define NUMPIXELS 60
#define PIXELSPIN 6

Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUMPIXELS, PIXELSPIN, NEO_GRB + NEO_KHZ800);


unsigned long wipeInterval=20000;  // the time we need to wait (20 seconds per LED, 10 min to complete)
unsigned long theaterInterval=20000;  // the time we need to wait
unsigned long colorWipePreviousMillis=0;
unsigned long theaterChasePreviousMillis=0;

int theaterChaseQ = 0;
uint16_t currentPixel = 0;// what pixel are we operating on

void setup() {
  currentPixel = 0;
  Serial.begin(19200);
  strip.begin(); // This initializes the NeoPixel library.
  strip.show(); // This sends the updated pixel color to the hardware.
      
}

void loop () {

        if (Serial.available() > 0) {
          data = Serial.read();

          if (data == 0){

            if ((unsigned long)(millis() - theaterChasePreviousMillis) >= theaterInterval) {
              theaterChasePreviousMillis = millis();
              theaterChase(strip.Color(255,0,0));
              }

          }

          else if (data > 0){
             wipeInterval=data*1000;
             if ((unsigned long)(millis() - colorWipePreviousMillis) >= wipeInterval) {
                colorWipePreviousMillis = millis();
                colorWipe(strip.Color(255,0,0));
                }


          }

  }

}


// Fill the dots one after the other with a color
void colorWipe(uint32_t c){
  strip.setPixelColor(currentPixel,c);
  strip.setPixelColor(currentPixel+30,c);
  strip.setBrightness(50);
  strip.show();
  currentPixel++;
  if(currentPixel == NUMPIXELS){
    currentPixel = 0;
  }
}

//Theatre-style crawling lights.
void theaterChase(uint32_t c) {
  for (int i=0; i < strip.numPixels(); i=i+2) {
      strip.setPixelColor(i+theaterChaseQ, c);    //turn every other pixel on
    }
    strip.show();
    for (int i=0; i < strip.numPixels(); i=i+2) {
      strip.setPixelColor(i+theaterChaseQ, 0);        //turn every other pixel off
    }
    theaterChaseQ++;
    if(theaterChaseQ >= 2) theaterChaseQ = 0;
}


