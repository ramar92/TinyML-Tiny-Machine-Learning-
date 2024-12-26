#include <Arduino_LSM9DS1.h> // For the IMU sensor

// Thresholds (Adjust as needed based on testing)
const float STEP_THRESHOLD = 1.2;     // Acceleration threshold for steps
const float TURN_THRESHOLD = 50.0;   // Angular velocity threshold for turns

// Variables
unsigned long lastStepTime = 0;
const unsigned long stepInterval = 300; // Minimum time between steps (ms)
int stepCount = 0;
String turnDirection = "None";

void setup() {
  Serial.begin(115200);
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
      Serial.print("Step Count: ");
      Serial.println(stepCount);
      Serial.println("No Moment!!");
    }
  }

  // Read gyroscope values
  if (IMU.gyroscopeAvailable()) {
    IMU.readGyroscope(gyroX, gyroY, gyroZ);

    // Detect turns
    if (gyroZ > TURN_THRESHOLD) {
      turnDirection = "Right Turn";
    } else if (gyroZ < -TURN_THRESHOLD) {
      turnDirection = "Left Turn";
    } else {
    
      turnDirection = "None";
    }

    if (turnDirection != "None") {
      Serial.print("Detected: ");
      Serial.println(turnDirection);
    }
  }

  delay(10); // Short delay for sensor sampling
}
