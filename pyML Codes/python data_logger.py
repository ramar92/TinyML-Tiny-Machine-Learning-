import serial
import csv
from datetime import datetime

# Set up the serial connection
arduino_port = "COM7"  # Replace with the correct port for your Arduino
baud_rate = 9600       # Match the baud rate in your Arduino code
output_file = "accelerometer_data.csv"

# Open the serial connection
try:
    ser = serial.Serial(arduino_port, baud_rate, timeout=1)
    print(f"Connected to {arduino_port} at {baud_rate} baud.")
except Exception as e:
    print(f"Error: {e}")
    exit()

# Open the CSV file for writing
with open(output_file, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp", "X", "Y", "Z"])  # Write the CSV header

    try:
        print(f"Logging data to {output_file}. Press Ctrl+C to stop.")
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode("utf-8").strip()
                print(line)  # Print data to console
                if line and "\t" in line:
                    values = line.split('\t')
                    if len(values) == 3:  # Ensure 3 values for X, Y, Z
                        writer.writerow([datetime.now(), values[0], values[1], values[2]])
    except KeyboardInterrupt:
        print("\nData logging stopped.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        ser.close()
        print("Serial connection closed.")
