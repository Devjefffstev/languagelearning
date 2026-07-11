/*
  Critical Temperature Alarm with DHT11 and Buzzer
  ------------------------------------------------
  Description:
  This Arduino program implements a critical temperature alarm system using a DHT11 sensor
  and an active buzzer.

  - The system continuously reads the ambient temperature from the DHT11 sensor.
  - If the temperature rises above 35 °C, the buzzer is activated to signal a critical condition.
  - The buzzer remains active until the temperature drops below 34 °C, at which point it is turned off.
  - This ON/OFF difference is called hysteresis, and it prevents the buzzer from flickering
    when the temperature is close to the threshold.
  - The program also prints the current temperature readings to the Serial Monitor.
  - If the sensor fails to provide a valid reading, an error message is displayed.
*/

#include <DHT.h>

#define DHTPIN 2       // DATA pin of DHT02
#define DHTTYPE DHT11  // Sensor type
#define BUZZER_PIN 8   // Active buzzer pin

const float THRESHOLD_ON  = 35.0;  // Temperature to activate alarm
const float THRESHOLD_OFF = 34.0;  // Temperature to deactivate alarm

DHT dht(DHTPIN, DHTTYPE);
bool alarmActive = false;

void setup() {
  pinMode(BUZZER_PIN, OUTPUT);
  digitalWrite(BUZZER_PIN, LOW);
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  // Read temperature with NAN handling
  float t = dht.readTemperature(); // °C
  if (isnan(t)) {
    Serial.println("Error reading DHT11");
    delay(1000);
    return;
  }

  Serial.print("Temperature: ");
  Serial.print(t);
  Serial.println(" °C");

  // Hysteresis logic to avoid buzzer flickering near the threshold
  if (!alarmActive && t > THRESHOLD_ON) {
    alarmActive = true;
    digitalWrite(BUZZER_PIN, HIGH); // Turn buzzer ON
  } else if (alarmActive && t < THRESHOLD_OFF) {
    alarmActive = false;
    digitalWrite(BUZZER_PIN, LOW);  // Turn buzzer OFF
  }

  delay(1000); // DHT11 recommends ~1s between readings
}

