/*------------------------------------------------------------------------
  This is an Arduino library for the Adafruit Thermal Printer.
Pick one up at --> https://www.adafruit.com/product/597
These printers use TTL serial to communicate, 2 pins are required.

Full tutorial with wiring diagrams, images, etc. is available at:
https://learn.adafruit.com/mini-thermal-receipt-printer

Before loading the example code, or even opening the Arduino software,
place the Adafruit_Thermal folder in your Arduino library.

////ARDUINO LIBRARY LOCATION////
On your Mac:: In (home directory)/Documents/Arduino/Libraries
On your PC:: My Documents\Arduino\libraries
On your Linux box: (home directory)/sketchbook/libraries

Adafruit invests time and resources providing this open source code.  Please support Adafruit and open-source hardware by purchasing products from Adafruit!

Written by Limor Fried/Ladyada for Adafruit Industries, with contributions from the open source community.  Originally based on Thermal library from bildr.org
MIT license, all text above must be included in any redistribution.
  
  Example sketch for Adafruit Thermal Printer library for Arduino.
  Demonstrates a few text styles & layouts, bitmap printing, etc.

  IMPORTANT: DECLARATIONS DIFFER FROM PRIOR VERSIONS OF THIS LIBRARY.
  This is to support newer & more board types, especially ones that don't
  support SoftwareSerial (e.g. Arduino Due).  You can pass any Stream
  (e.g. Serial1) to the printer constructor.  See notes below.

  You may need to edit the PRINTER_FIRMWARE value in Adafruit_Thermal.h
  to match your printer (hold feed button on powerup for test page).
  ------------------------------------------------------------------------*/

#include "Adafruit_Thermal.h"
#include "imageToSave.h"

// Here's the new syntax when using SoftwareSerial (e.g. Arduino Uno) ----
// If using hardware serial instead, comment out or remove these lines:

#include "SoftwareSerial.h"
#define TX_PIN 6 // Arduino transmit  YELLOW WIRE  labeled RX on printer
#define RX_PIN 5 // Arduino receive   GREEN WIRE   labeled TX on printer

SoftwareSerial mySerial(RX_PIN, TX_PIN); // Declare SoftwareSerial obj first
Adafruit_Thermal printer(&mySerial);     // Pass addr to printer constructor
// Then see setup() function regarding serial & printer begin() calls.

// Here's the syntax for hardware serial (e.g. Arduino Due) --------------
// Un-comment the following line if using hardware serial:

//Adafruit_Thermal printer(&Serial1);      // Or Serial2, Serial3, etc.

// -----------------------------------------------------------------------

void setup() {

  // This line is for compatibility with the Adafruit IotP project pack,
  // which uses pin 7 as a spare grounding point.  You only need this if
  // wired up the same way (w/3-pin header into pins 5/6/7):
  pinMode(7, OUTPUT); digitalWrite(7, LOW);

  // NOTE: SOME PRINTERS NEED 9600 BAUD instead of 19200, check test page.
  mySerial.begin(19200);  // Initialize SoftwareSerial
  //Serial1.begin(19200); // Use this instead if using hardware serial
  printer.begin();        // Init printer (same regardless of serial type)

  // The following calls are in setup(), but don't *need* to be.  Use them
  // anywhere!  They're just here so they run one time and are not printed
  // over and over (which would happen if they were in loop() instead).
  // Some functions will feed a line when called, this is normal.

  
  // Print the haiku in imageToSave.h:
  printer.println(F("     "));
  printer.println(F("     "));
  printer.printBitmap(imageToSave_width, imageToSave_height, imageToSave_data);
  printer.println(F("     "));
  printer.println(F("     "));
  printer.println(F("     "));
  printer.println(F("     "));
  printer.println(F("     "));
  printer.println(F("     "));
  printer.println(F("     "));

  printer.feed(2);

  printer.sleep();      // Tell printer to sleep
  delay(3000L);         // Sleep for 3 seconds
  printer.wake();       // MUST wake() before printing again, even if reset
  printer.setDefault(); // Restore printer to defaults
}

void loop() {
}