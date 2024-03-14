// DMD display driver, controlled by I2C
// by Oleksander Laskavtsev 

// Uses the Wire library
// Receives data as an I2C/TWI slave device
// Displays data with a specially created font

// Created 22 March 2023

#include <Wire.h> 
#include <SPI.h> //we need some SPI for DMD...
#include <DMD2.h> //including DMD2 library
#include <fonts/LAS14x30.h> //including the FONT

#define ROW 1 // the ROW number from the top 

SPIDMD dmd(5,2); // declaring DMD object (5 accross, 2 down)

void setup() {
  Wire.begin(ROW+7);         // join I2C bus as a slave, with the address defined in ROW 
  Wire.onReceive(receiveData); // registering I2C event
  dmd.setBrightness(32); // setting up default brighness
  dmd.selectFont(LAS14x30); // setting up the font
  dmd.begin(); // srarting Digital Matrix Display
  dmd.scanDisplay(); // scanning the avaliable matrices
}

void loop() {
  //nothing to do here...
}

void receiveData() {
  String rData;
  char toDraw[11];
  while (0 < Wire.available()) { // loop through all but the last
    char c = Wire.read(); // receive byte as a character
    rData += c; // getting data from the main module via I2C bus
  }
  int divIndex = rData.indexOf("~");
  int endIndex = rData.length();
  String brv = rData.substring(0, divIndex); // extracting the brightness value
  String tData = rData.substring(divIndex+1, endIndex); // extracting the text data
  int val = brv.toInt(); // converting brightness into integer
  tData.toCharArray(toDraw, (tData.length()+1)); // converting text data into array of chars
  dmd.clearScreen(); // it's high time to refresh!..
  dmd.setBrightness(val); // setting the reasonable brightness
  dmd.drawString(0, 0, toDraw); // drawing the text data
}
