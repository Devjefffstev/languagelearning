/*
  Project: Joystick Control with Arduino UNO R4 and LED Matrix
  Description:
    This project uses a joystick connected to the Arduino UNO R4 to control the built-in LED matrix (8x12).
    - The joystick's X and Y axes are read as analog signals (0–1023).
    - Moving the joystick displays compact arrows on the LED matrix:
        * Up    → arrow pointing up
        * Down  → arrow pointing down
        * Left  → arrow pointing left
        * Right → arrow pointing right
        * Center (neutral position) → small dot in the middle
    - The joystick also has a push button. When pressed, all LEDs on the matrix turn ON.
    - The Serial Monitor is used to display joystick values and button state for debugging.

  Hardware:
    - Arduino UNO R4 (Minima or WiFi)
    - Joystick module (X, Y, SW pins)
    - Built-in Arduino LED Matrix (8 rows x 12 columns)
*/

#include <Arduino_LED_Matrix.h>

ArduinoLEDMatrix matrix;

int xPin = A0;        // Joystick X-axis connected to analog pin A0
int yPin = A1;        // Joystick Y-axis connected to analog pin A1
int buttonPin = 2;    // Joystick button (SW) connected to digital pin 2

uint8_t pixels[96];   // 8 rows x 12 columns = 96 LEDs

// Clear the matrix (turn off all LEDs)
void clearMatrix() {
  for (int i = 0; i < 96; i++) pixels[i] = 0;
}

// Turn ON a specific LED at row and column
void setPixel(int row, int col) {
  if (row >= 0 && row < 8 && col >= 0 && col < 12) {
    pixels[row * 12 + col] = 1;
  }
}

// Turn ON all LEDs in the matrix
void setAllPixels() {
  for (int i = 0; i < 96; i++) pixels[i] = 1;
}

// Arrow Up (compact)
void drawArrowUp() {
  // short body
  setPixel(4, 6);
  setPixel(5, 6);
  setPixel(6, 6);
  // small tip
  setPixel(3, 6);
  setPixel(2, 6);
  setPixel(3, 5);
  setPixel(3, 7);
}

// Arrow Down (compact)
void drawArrowDown() {
  // short body
  setPixel(2, 6);
  setPixel(3, 6);
  setPixel(4, 6);
  // small tip
  setPixel(5, 6);
  setPixel(6, 6);
  setPixel(5, 5);
  setPixel(5, 7);
}

// Arrow Left
void drawArrowLeft() {
  for (int c = 3; c < 9; c++) setPixel(4, c);   // body
  setPixel(4, 2); setPixel(4, 1);               // tip
  setPixel(3, 2); setPixel(5, 2);
}

// Arrow Right
void drawArrowRight() {
  for (int c = 3; c < 9; c++) setPixel(4, c);   // body
  setPixel(4, 9); setPixel(4, 10);              // tip
  setPixel(3, 9); setPixel(5, 9);
}

// Center Dot
void drawCenterDot() {
  setPixel(3, 5); setPixel(3, 6);
  setPixel(4, 5); setPixel(4, 6);
}

void setup() {
  matrix.begin();          // initialize LED matrix
  Serial.begin(9600);      // start serial communication
  pinMode(buttonPin, INPUT_PULLUP); // configure joystick button
}

void loop() {
  int xVal = analogRead(xPin);       // read X-axis value
  int yVal = analogRead(yPin);       // read Y-axis value
  int buttonState = digitalRead(buttonPin); // read button state

  clearMatrix(); // reset matrix before drawing

  // Print values to Serial Monitor
  Serial.print("X: "); Serial.print(xVal);
  Serial.print(" | Y: "); Serial.print(yVal);
  Serial.print(" | Button: "); Serial.println(buttonState);

  if (buttonState == LOW) {
    setAllPixels();
    Serial.println("Button pressed → All LEDs ON");
  } else {
    if (yVal > 700) {
      drawArrowDown();
      Serial.println("Joystick Down → Arrow Down");
    } else if (yVal < 300) {
      drawArrowUp();
      Serial.println("Joystick Up → Arrow Up");
    } else if (xVal > 700) {
      drawArrowRight();
      Serial.println("Joystick Right → Arrow Right");
    } else if (xVal < 300) {
      drawArrowLeft();
      Serial.println("Joystick Left → Arrow Left");
    } else if (xVal > 400 && xVal < 600 && yVal > 400 && yVal < 600) {
      drawCenterDot();
      Serial.println("Joystick Center → Dot");
    }
  }

  matrix.loadPixels(pixels, 96); // update matrix with new pixels
  delay(100);                    // small delay for stability
}
