import serial
print(serial.__file__)

try:
    ser = serial.Serial('COM6', 9600)  # Replace 'COM6' with your actual port
    print("Serial connection established!")
    ser.close()
except Exception as e:
    print(f"Error: {e}")