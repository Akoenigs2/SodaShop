from machine import Pin
import time

# Define the LED pin (change 15 to your actual GPIO pin)
led = Pin(15, Pin.OUT)

while True:
    led.toggle()  # Toggle LED state
    time.sleep(0.5)  # Wait for 500ms

