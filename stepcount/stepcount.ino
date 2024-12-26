#include <Arduino_LSM9DS1.h>

// Threshold for step detection
const float stepThreshold = 0.5; // Adjust based on sensitivity
float prevMagnitude = 0;

void setup() {
  Serial.begin(9600);
  while (!Serial);
  Serial.println("Started");

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }

  Serial.print("Accelerometer sample rate = ");
  Serial.print(IMU.accelerationSampleRate());
  Serial.println(" Hz");
  Serial.println("X\tY\tZ\tMagnitude\tStep Count");
}

int stepCount = 0;

void loop() {
  float x, y, z;

  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(x, y, z);

    // Calculate the magnitude of the acceleration vector
    float magnitude = sqrt(x * x + y * y + z * z);

    // Detect step if the magnitude crosses the threshold
    if (magnitude - prevMagnitude > stepThreshold) {
      stepCount++;
    }

    // Save the current magnitude for the next iteration
    prevMagnitude = magnitude;

    // Print acceleration and step count
    Serial.print(x, 2);
    Serial.print("\t");
    Serial.print(y, 2);
    Serial.print("\t");
    Serial.print(z, 2);
    Serial.print("\t");
    Serial.print(magnitude, 2);
    Serial.print("\t");
    Serial.println(stepCount);
  }
  delay(50); // Sampling delay
}
