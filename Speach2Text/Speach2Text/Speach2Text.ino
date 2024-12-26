#include <PDM.h>

// Buffer to read audio samples
short sampleBuffer[256];
volatile int samplesRead;

void setup() {
  Serial.begin(9600);
  while (!Serial);

  // Configure PDM microphone
  if (!PDM.begin(1, 16000)) { // Mono channel, 16kHz sample rate
    Serial.println("Failed to initialize PDM!");
    while (1);
  }

  // Set the PDM buffer size
  PDM.setBufferSize(512);

  // Set callback for when audio is available
  PDM.onReceive(onPDMdata);

  Serial.println("PDM Microphone initialized.");
}

void loop() {
  if (samplesRead) {
    // Send the audio data over Serial
    for (int i = 0; i < samplesRead; i++) {
      Serial.println(sampleBuffer[i]);
    }
    samplesRead = 0;
  }
}

// Callback for receiving audio data
void onPDMdata() {
  int bytesAvailable = PDM.available();
  PDM.read(sampleBuffer, bytesAvailable);
  samplesRead = bytesAvailable / 2;
}
