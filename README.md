# SwitchBot System

This project is a SwitchBot system that allows you to control a physical switch using an iPhone via Bluetooth Low Energy (BLE). The system consists of an ESP32 microcontroller, a servo motor, and an iPhone application.

## Table of Contents

- [Requirements](#requirements)
- [System Overview](#system-overview)
- [ESP32 Setup](#esp32-setup)
- [iPhone Application](#iphone-application)
- [Device Configuration](#device-configuration)

## Requirements

- ESP32 microcontroller
- Servo motor
- Battery box (2x AAA batteries)
- iPhone with BLE support
- MicroPython

## System Overview

The SwitchBot system consists of the following components:

1. **ESP32 Microcontroller**: The main controller that communicates with the iPhone via BLE and controls the servo motor.
2. **Servo Motor**: Used to press the physical switch.
3. **Battery Box**: Provides power to the ESP32 and servo motor.
4. **iPhone Application**: Communicates with the ESP32 via BLE to control the servo motor.

## ESP32 Setup

### Hardware Connections

1. Connect the servo motor to the ESP32:
   - Signal pin to GPIO 15
   - Power pin to 3.3V
   - Ground pin to GND

2. Connect the battery box to the ESP32:
   - Positive terminal to VIN
   - Negative terminal to GND

3. Connect an external button to GPIO 14 for waking up the ESP32 from DeepSleep mode.

### MicroPython Firmware

1. Install MicroPython on the ESP32. Follow the instructions [here](https://docs.micropython.org/en/latest/esp32/tutorial/intro.html) to flash MicroPython firmware on the ESP32.

2. Upload the `main.py` file to the ESP32. The `main.py` file contains the code to handle BLE communication, control the servo motor, and manage DeepSleep mode.

## iPhone Application

### Building the Application

1. Open Xcode and create a new project.
2. Add the `AppDelegate.swift` and `ViewController.swift` files to your project.
3. Ensure that your project has the necessary permissions for using Bluetooth. Add the following keys to your `Info.plist` file:
   - `NSBluetoothAlwaysUsageDescription`
   - `NSBluetoothPeripheralUsageDescription`

### Using the Application

1. Build and run the application on your iPhone.
2. The application will scan for the ESP32 device and connect to it.
3. Use the user interface to send commands to the ESP32 to control the servo motor.

## Device Configuration

### ESP32 Configuration

1. Ensure that the ESP32 is powered by the battery box.
2. Connect the servo motor and external button as described in the hardware connections section.
3. Upload the `main.py` file to the ESP32.

### iPhone Application Configuration

1. Ensure that Bluetooth is enabled on your iPhone.
2. Open the SwitchBot application and connect to the ESP32 device.
3. Use the application to control the servo motor and press the switch.

### Device configuration diagram

Below is the device configuration diagram for the ESP32, servo motor, and power connections:

```
+-------------------+
|      ESP32        |
|                   |
|  GPIO 15 (PWM) <--|--- Signal pin (Servo Motor)
|  3.3V       <--|--- Power pin (Servo Motor)
|  GND        <--|--- Ground pin (Servo Motor)
|                   |
|  VIN        <--|--- Positive terminal (Battery Box)
|  GND        <--|--- Negative terminal (Battery Box)
|                   |
|  GPIO 14 (Wake) <--|--- External button
+-------------------+
```

* **ESP32 Microcontroller**:
  * GPIO 15: Connect to the signal pin of the servo motor.
  * 3.3V: Connect to the power pin of the servo motor.
  * GND: Connect to the ground pin of the servo motor.
  * VIN: Connect to the positive terminal of the battery box.
  * GND: Connect to the negative terminal of the battery box.
  * GPIO 14: Connect to an external button for waking up the ESP32 from DeepSleep mode.

* **Servo Motor**:
  * Signal pin: Connect to GPIO 15 of the ESP32.
  * Power pin: Connect to 3.3V of the ESP32.
  * Ground pin: Connect to GND of the ESP32.

* **Battery Box**:
  * Positive terminal: Connect to VIN of the ESP32.
  * Negative terminal: Connect to GND of the ESP32.

* **External Button**:
  * Connect to GPIO 14 of the ESP32 for waking up from DeepSleep mode.

## Power Management

The ESP32 is configured to use DeepSleep mode to reduce power consumption. The device will wake up from DeepSleep mode when the external button is pressed. After executing the servo motor command, the ESP32 will return to DeepSleep mode after 10 seconds.

## Troubleshooting

- If the ESP32 does not respond to commands from the iPhone, ensure that the BLE connection is established and the device is powered on.
- If the servo motor does not move, check the connections and ensure that the servo motor is receiving power.
- If the ESP32 does not wake up from DeepSleep mode, check the connection of the external button and ensure that it is connected to GPIO 14.
