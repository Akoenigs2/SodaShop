from machine import Pin, UART
import time

# Configure UART (match Raspberry Pi 4 settings)
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

# LED setup (change pin number if needed)
led = Pin(15, Pin.OUT)  # Use GPIO 15 for the LED

def read_serial_values():
    """Reads and parses serial input from Raspberry Pi, returns a list of five integers."""
    if uart.any():  # Check if data is available
        try:
            data = uart.readline().decode().strip()  # Read and decode data
            values = list(map(int, data.split(',')))  # Convert to integers
            if len(values) == 5 and all(0 <= v <= 100 for v in values):  
                return values
            else:
                print("Invalid data format:", data)  # Debugging
        except Exception as e:
            print("Error reading input:", e)
    return None

while True:
    values = read_serial_values()
    if values:
        print("Received values:", values)  # Debug output
        if values[0] > 50:
            led.value(1)  # Turn LED ON
            print("LED ON (first value > 50)")
        else:
            led.value(0)  # Turn LED OFF
            print("LED OFF (first value ≤ 50)")
    time.sleep(0.1)  # Small delay to avoid excessive polling


'''
from machine import Pin, PWM, UART
import time

# Configure UART to match Raspberry Pi 4 settings (9600 baud)
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

# Define GPIO pins for the relays (adjust as needed)
relay_pins = [2, 3, 4, 5, 6]

# Initialize PWM for relay control
relays = [PWM(Pin(pin)) for pin in relay_pins]

# Set PWM frequency (adjust as necessary for relay response)
for relay in relays:
    relay.freq(1000)  # 1 kHz

def set_relay_pwm(values):
    """Convert percentage values (0-100) to PWM duty cycle (0-65535)"""
    for i in range(5):
        duty = int((values[i] / 100) * 65535)
        relays[i].duty_u16(duty)

def read_serial_values():
    """Reads and parses serial input from Raspberry Pi, returns a list of five integers."""
    if uart.any():  # Check if data is available
        try:
            data = uart.readline().decode().strip()  # Read and decode data
            values = list(map(int, data.split(',')))  # Convert to integers
            if len(values) == 5 and all(0 <= v <= 100 for v in values):  
                return values
            else:
                print("Invalid data format:", data)  # Debugging
        except Exception as e:
            print("Error reading input:", e)
    return None

while True:
    values = read_serial_values()
    if values:
        print("Received values:", values)  # Debug output
        set_relay_pwm(values)
    time.sleep(0.1)  # Small delay to avoid excessive polling
'''