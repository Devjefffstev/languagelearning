/*
  Project: Joystick Control with Arduino R4 and LED Matrix
  Description:
    This project uses a joystick connected to the Arduino R4 to control an LED matrix.
    - The joystick's X and Y axes are read as analog signals (0–1023).
    - Moving the joystick lights up rows or columns on the LED matrix:
        * Up → top row
        * Down → bottom row
        * Left → first column
        * Right → last column
        * Center → middle LED
    - The joystick also has a push button. When pressed, all LEDs on the matrix turn ON.
    - Serial Monitor is used to display the joystick values and button state for debugging.
  Hardware:
    - Arduino R4
    - Joystick module (X, Y, SW pins)
    - Arduino LED Matrix
*/


#include <Arduino_LED_Matrix.h>

ArduinoLEDMatrix matrix;

int xPin = A0;        // Joystick X-axis connected to analog pin A0
int yPin = A1;        // Joystick Y-axis connected to analog pin A1
int buttonPin = 2;    // Joystick button (SW) connected to digital pin 2

uint8_t pixels[96];   // 8 rows x 12 columns = 96 LEDs

// Clear the matrix (turn off all LEDs)
void clearMatrix() {
  for (int i = 0; i < 96; i++) {
    pixels[i] = 0;
  }
}

// Turn ON a specific LED at row and column
void setPixel(int row, int col) {
  if (row >= 0 && row < 8 && col >= 0 && col < 12) {
    pixels[row * 12 + col] = 1;
  }
}

// Turn ON all LEDs in the matrix
void setAllPixels() {
  for (int i = 0; i < 96; i++) {
    pixels[i] = 1;
  }
}

void setup() {
  matrix.begin();
  Serial.begin(9600);              // Initialize Serial Monitor
  pinMode(buttonPin, INPUT_PULLUP); // Configure joystick button with internal pull-up
}

void loop() {
  int xVal = analogRead(xPin);       // Read X-axis value
  int yVal = analogRead(yPin);       // Read Y-axis value
  int buttonState = digitalRead(buttonPin); // Read button state

  // Print values to Serial Monitor
  Serial.print("X: ");
  Serial.print(xVal);
  Serial.print(" | Y: ");
  Serial.print(yVal);
  Serial.print(" | Button: ");
  Serial.println(buttonState);

  clearMatrix();

  // If button is pressed → turn ON all LEDs
  if (buttonState == LOW) {
    setAllPixels();
  } else {
    // Up → top row
    if (yVal > 700) {
      for (int c = 0; c < 12; c++) {
        setPixel(0, c);
      }
    }
    // Down → bottom row
    else if (yVal < 300) {
      for (int c = 0; c < 12; c++) {
        setPixel(7, c);
      }
    }
    // Right → last column
    if (xVal > 700) {
      for (int r = 0; r < 8; r++) {
        setPixel(r, 11);
      }
    }
    // Left → first column
    else if (xVal < 300) {
      for (int r = 0; r < 8; r++) {
        setPixel(r, 0);
      }
    }
    // Center → middle LED (row 3, col 6 approx.)
    else if (xVal > 400 && xVal < 600 && yVal > 400 && yVal < 600) {
      setPixel(3, 6);
    }
  }

  // Display on the LED matrix
  matrix.loadPixels(pixels, 96);

  delay(100);
}



