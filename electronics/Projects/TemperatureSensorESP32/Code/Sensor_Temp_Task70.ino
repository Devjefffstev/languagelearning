/*
  Project: ESP32 Temperature Monitoring with DHT11 and LED Indicator
  Author: David
  Date: December 29, 2025
  Version: 1.0

  Description:
    This program reads temperature data from a DHT11 sensor connected to GPIO19
    and prints the values to the serial monitor at 115200 baud.
    - If the temperature exceeds 30°C, the LED connected to GPIO17 is turned on.
    - Otherwise, the LED remains off.
    - Additionally, the LED blinks every 2 seconds to demonstrate digital output control.

  Hardware:
    - ESP32 development board
    - DHT11 temperature sensor (data pin → GPIO19)
    - LED + 220Ω resistor connected to GPIO17

  Purpose:
    This project demonstrates how to integrate a temperature sensor with the ESP32
    and control an LED based on sensor readings. It serves as a simple IoT example
    for environmental monitoring and actuator control.
*/


#include <DHT.h>

#define DHTPIN 19       // Data pin of the DHT11 connected to GPIO19
#define DHTTYPE DHT11   // Sensor type
#define LEDPIN 17       // LED pin connected to GPIO17

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);     // Initialize serial communication
  dht.begin();              // Initialize the DHT11 sensor
  pinMode(LEDPIN, OUTPUT);  // Set LED pin as output
}

void loop() {
  float temp = dht.readTemperature();  // Read temperature in °C

  if (isnan(temp)) {
    Serial.println("Failed to read from DHT sensor");
  }

  Serial.print("Temperature: ");
  Serial.print(temp);
  Serial.println(" °C");

  if (temp > 30.0) {
    digitalWrite(LEDPIN, HIGH);  // Turn LED on if temperature > 30°C
  } else {
    digitalWrite(LEDPIN, LOW);   // Turn LED off otherwise
  }

  // Blink LED every 2 seconds (independent of temperature condition)
  digitalWrite(LEDPIN, HIGH);  
  delay(2000);                  
  digitalWrite(LEDPIN, LOW);   
  delay(2000);                  
}
