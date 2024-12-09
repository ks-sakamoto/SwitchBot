import time

import bluetooth
import config
import machine
from machine import PWM, Pin, Timer

# Initialize the servo motor
servo = PWM(Pin(15), freq=50)


# Function to set the servo angle
def set_servo_angle(angle):
    duty = int((angle / 180) * 1023)
    servo.duty(duty)


# BLE setup
ble = bluetooth.BLE()
ble.active(True)


# Function to handle BLE events
def ble_irq(event, data):
    if event == 1:  # Central connected
        print("Central connected")
    elif event == 2:  # Central disconnected
        print("Central disconnected")
    elif event == 3:  # Write request
        print("Write request")
        set_servo_angle(90)  # Press the switch
        time.sleep(1)
        set_servo_angle(0)  # Release the switch
        time.sleep(10)
        machine.deepsleep()


# Register the BLE event handler
ble.irq(ble_irq)

# Create a BLE service
service_uuid = bluetooth.UUID(config.SERVICE_UUID)
service = (service_uuid, ())

# Add the service to the BLE stack
ble.gatts_register_services((service,))

# DeepSleep setup
wake_pin = Pin(14, mode=Pin.IN, pull=Pin.PULL_UP)
wake_pin.irq(trigger=Pin.IRQ_FALLING, handler=lambda pin: machine.deepsleep())

# Main loop
while True:
    machine.deepsleep()
