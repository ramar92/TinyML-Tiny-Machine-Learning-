import serial
import numpy as np
from math import sqrt
import time

# Serial port configuration
SERIAL_PORT = 'COM7'  # Replace with your Arduino's COM port
BAUD_RATE = 9600

# Step detection threshold
STEP_THRESHOLD = 0.5
prev_magnitude = 0
step_count = 0

# Function to calculate magnitude of acceleration
def calculate_magnitude(x, y, z):
    return sqrt(x**2 + y**2 + z**2)

# Function to detect steps
def detect_step(magnitude, prev_magnitude, threshold):
    return (magnitude - prev_magnitude) > threshold

try:
    # Initialize the serial connection
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print("Connected to Arduino. Reading data...")

    while True:
        # Read a line of data from the serial port
        line = ser.readline().decode('utf-8').strip()
        if not line:
            continue

        try:
            # Parse accelerometer data (assumes tab-separated X, Y, Z)
            x, y, z = map(float, line.split('\t'))
        except ValueError:
            print(f"Invalid data: {line}")
            continue

        # Calculate magnitude of acceleration
        magnitude = calculate_magnitude(x, y, z)

        # Detect step and update step count
        if detect_step(magnitude, prev_magnitude, STEP_THRESHOLD):
            step_count += 1
            print(f"Step detected! Total Steps: {step_count}")

        # Update the previous magnitude
        prev_magnitude = magnitude

        # Print acceleration and magnitude for debugging
        print(f"X: {x:.2f}, Y: {y:.2f}, Z: {z:.2f}, Magnitude: {magnitude:.2f}")
        time.sleep(0.05)  # Sampling delay

except KeyboardInterrupt:
    print("\nStopped by user.")
finally:
    # Close the serial connection
    ser.close()
    print("Serial connection closed.")
