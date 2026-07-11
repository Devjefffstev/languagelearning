/*
  Project: ESP32 LED Blink Example
  Description:
    This program demonstrates how to control a digital output pin on the ESP32.
    - Configures GPIO4 as an output pin.
    - Turns the LED on for 1 second, then off for 1 second.
    - Repeats the cycle indefinitely, creating a blinking effect.

  Hardware:
    - ESP32 development board
    - LED connected to GPIO4 (with a suitable resistor)

  Purpose:
    Serves as a basic test to verify that the ESP32 can drive digital outputs
    and is often used as a "Hello World" example in microcontroller programming.
*/
// Version updated: Dec 29, 2025



void setup() {
  pinMode(4, OUTPUT); // declare GPIO4 pin as output
}

void loop() {
  digitalWrite(4, HIGH); // turn LED on
  delay(1000);           // wait 1 second
  digitalWrite(4, LOW);  // turn LED off
  delay(1000);           // wait 1 second
}
