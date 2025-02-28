import serial
import parms

def send_values():
    try:
        ser = serial.Serial(parms.port, parms.baudrate, timeout=1)
        data = f"{parms.currentDrink.flavor1Perc},{parms.currentDrink.flavor2Perc},{parms.currentDrink.flavor3Perc}, {parms.currentDrink.flavor4Perc},{parms.currentDrink.carbPerc}\n"
        ser.write(data.encode())  # Send as bytes
        ser.close()
    except Exception as e:
        print(f"Error: {e}")
