import serial
import time
import numpy as np

# Initialize serial communication
arduino = serial.Serial(port='COM7', baudrate=9600, timeout=1)  # Update COM port as needed
time.sleep(2)  # Wait for the connection to establish

def calculate_steps(data, threshold=1.2):
    """
    Calculate steps based on acceleration magnitude crossing a threshold.
    """
    steps = 0
    for i in range(1, len(data)):
        if data[i - 1] < threshold <= data[i]:  # Rising edge detection
            steps += 1
    return steps

# Main loop
accel_data = []
try:
    while True:
        if arduino.in_waiting > 0:
            line = arduino.readline().decode('utf-8').strip()
            try:
                accel = float(line)
                accel_data.append(accel)
                if len(accel_data) > 50:  # Keep a rolling window of 50 readings
                    accel_data.pop(0)
                
                steps = calculate_steps(accel_data)
                print(f"Steps: {steps}")
            except ValueError:
                continue
except KeyboardInterrupt:
    print("Exiting...")
    arduino.close()
