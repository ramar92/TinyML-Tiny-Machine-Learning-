#include <Arduino_LSM9DS1.h> // For the IMU sensor

// Thresholds (Adjust as needed)
const float STEP_THRESHOLD = 1.2;     // Acceleration threshold for steps
const float TURN_THRESHOLD = 50.0;   // Angular velocity threshold for turns

// Variables
unsigned long lastStepTime = 0;
const unsigned long stepInterval = 300; // Minimum time between steps (ms)
int stepCount = 0;
String turnDirection = "None";

void setup() {
  Serial.begin(115200); // Serial communication for transmitting data
  while (!Serial);

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }
  Serial.println("IMU initialized successfully.");
}

void loop() {
  float accX, accY, accZ;
  float gyroX, gyroY, gyroZ;

  // Read accelerometer values
  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(accX, accY, accZ);

    // Detect steps
    if (millis() - lastStepTime > stepInterval && accZ > STEP_THRESHOLD) {
      stepCount++;
      lastStepTime = millis();
    }
  }

  // Read gyroscope values
  if (IMU.gyroscopeAvailable()) {
    IMU.readGyroscope(gyroX, gyroY, gyroZ);

    // Detect turns
    if (gyroZ > TURN_THRESHOLD) {
      turnDirection = "Right";
    } else if (gyroZ < -TURN_THRESHOLD) {
      turnDirection = "Left";
    } else {
      turnDirection = "None";
    }
  }

  // Transmit data as JSON
  Serial.print("{\"steps\":");
  Serial.print(stepCount);
  Serial.print(",\"turn\":\"");
  Serial.print(turnDirection);
  Serial.println("\"}");

  delay(100); // Short delay
}
