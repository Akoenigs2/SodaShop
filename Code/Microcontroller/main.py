# MicroPython conversion of PaulRP2040.ino for RP2040

from machine import Pin, ADC, UART
import time

# Pin definitions
analog_pin = ADC(26)  # Corresponds to A0 on RP2040
relay_pins = {
    'relay1': Pin(2, Pin.OUT),
    'relay2': Pin(3, Pin.OUT),
    'relay3': Pin(4, Pin.OUT)
}

# Button input pins
button_pins = {
    'button1': Pin(10, Pin.IN, Pin.PULL_UP),
    'button2': Pin(11, Pin.IN, Pin.PULL_UP),
    'button3': Pin(12, Pin.IN, Pin.PULL_UP)
}

# Serial communication setup
uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))

# Global variables for received values
value1, value2, value3, value4, value5 = 0, 0, 0, 0, 0

# Debouncer function
def debouncer(pin):
    state1 = pin.value()
    time.sleep(0.01)
    state2 = pin.value()
    return state1 if state1 == state2 else 0

# Relay control function
def relay_control(pin_in_con, reg_out, pin_name):
    if pin_in_con:
        reg_out.on()
    else:
        reg_out.off()
    print(f"{pin_name} set to {'ON' if pin_in_con else 'OFF'}")
    return pin_in_con

# Function to read and parse serial data
def read_serial():
    global value1, value2, value3, value4, value5
    if uart.any():
        data = uart.readline()
        if data:
            try:
                values = list(map(int, data.decode().strip().split(',')))
                if len(values) == 5 and all(0 <= v <= 100 for v in values):
                    value1, value2, value3, value4, value5 = values
                    print(f"Received values: {values}")
            except ValueError:
                print("Invalid serial data received")

# Main loop
while True:
    analog_value = analog_pin.read_u16()
    print(f"Analog Read: {analog_value}")
    
    # Read and parse serial input
    read_serial()
    
    print(f"Value1= {value1}")
    print(f"Value2= {value2}")
    print(f"Value3= {value3}")
    print(f"Value4= {value4}")
    print(f"Value5= {value5}")
    
    # Read button states with debouncing
    button_states = {name: debouncer(pin) for name, pin in button_pins.items()}
    
    # Example relay control logic based on buttons and analog value
    relay_control(button_states['button1'] or analog_value > 30000, relay_pins['relay1'], "Relay 1")
    relay_control(button_states['button2'] or analog_value > 40000, relay_pins['relay2'], "Relay 2")
    relay_control(button_states['button3'] or analog_value > 50000, relay_pins['relay3'], "Relay 3")
    
    time.sleep(0.1)
