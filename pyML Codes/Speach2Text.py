import serial
import numpy as np
import wave
import os
import speech_recognition as sr

# Configure the serial port
SERIAL_PORT = 'COM7'  # Replace with your Arduino's COM port
BAUD_RATE = 9600

# File to save audio data
OUTPUT_FILE = 'audio.wav'

# Initialize serial connection
ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
print("Connected to Arduino. Reading data...")

# Read audio data from the serial port
def read_audio_from_serial():
    audio_data = []
    while True:
        try:
            line = ser.readline().decode('utf-8').strip()
            if line.isdigit() or (line.startswith('-') and line[1:].isdigit()):
                audio_data.append(int(line))
        except KeyboardInterrupt:
            print("Stopping data collection.")
            break
    return np.array(audio_data, dtype=np.int16)

# Save audio data as WAV file
def save_to_wav(audio_data, filename, sample_rate=16000):
    with wave.open(filename, 'w') as wf:
        wf.setnchannels(1)  # Mono
        wf.setsampwidth(2)  # 16-bit audio
        wf.setframerate(sample_rate)
        wf.writeframes(audio_data.tobytes())

# Perform speech-to-text
def perform_speech_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        print("Transcribing audio...")
        text = recognizer.recognize_google(audio)
        print("Transcription: ", text)
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print(f"Error with speech recognition service: {e}")

# Main logic
audio_data = read_audio_from_serial()
print("Data received. Saving to WAV file...")
save_to_wav(audio_data, OUTPUT_FILE)

if os.path.exists(OUTPUT_FILE):
    print("Saved audio. Performing speech-to-text...")
    perform_speech_to_text(OUTPUT_FILE)
