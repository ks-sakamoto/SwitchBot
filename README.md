# SwitchBot System

This project is a SwitchBot system that allows you to control a physical switch using an iPhone via Bluetooth Low Energy (BLE). The system consists of an ESP32 microcontroller, a servo motor, and a BLE communication using nRF Connect or LightBlue.

## Table of Contents

- [Requirements](#requirements)
- [System Overview](#system-overview)
- [ESP32 Setup](#esp32-setup)
- [ESP32 Pinout Reference](#esp32-pinout-reference)
- [BLE Communication](#ble-communication)
- [Device Configuration](#device-configuration)

## Requirements

- ESP32 microcontroller
- Servo motor
- 9V battery
- 3-terminal regulator
- iPhone with nRF Connect or LightBlue app
- MicroPython

## System Overview

The SwitchBot system consists of the following components:

1. **ESP32 Microcontroller**: The main controller that communicates with the iPhone via BLE and controls the servo motor.
2. **Servo Motor**: Used to press the physical switch.
3. **Battery Box**: Provides power to the ESP32 and servo motor.
4. **BLE Communication**: Communicates with the ESP32 via BLE to control the servo motor.

## ESP32 Setup

### Hardware Connections

1. Connect the servo motor to the ESP32:
   - Signal pin to GPIO 15
   - Power pin to 3.3V
   - Ground pin to GND

2. Connect the 9V battery to the 3-terminal regulator:
   - Positive terminal of the 9V battery to the input pin of the 3-terminal regulator
   - Ground terminal of the 9V battery to the ground pin of the 3-terminal regulator

3. Connect the output of the 3-terminal regulator to the ESP32:
   - Output pin of the 3-terminal regulator to VIN
   - Ground pin of the 3-terminal regulator to GND

4. Connect an external button to GPIO 14 for waking up the ESP32 from DeepSleep mode.

### MicroPython Firmware

1. Install MicroPython on the ESP32. Follow the instructions [here](https://docs.micropython.org/en/latest/esp32/tutorial/intro.html) to flash MicroPython firmware on the ESP32.

2. Upload the `main.py` file to the ESP32. The `main.py` file contains the code to handle BLE communication, control the servo motor, and manage DeepSleep mode.

### USB Driver Installation

If your computer does not recognize the ESP32 when connected via USB, you may need to install the USB driver. Follow the instructions provided in the link below to install the USB driver for ESP32:

[Install ESP32 USB Drivers (CP210x) on Windows](https://randomnerdtutorials.com/install-esp32-esp8266-usb-drivers-cp210x-windows/)

### Transferring MicroPython Scripts to ESP32

To transfer MicroPython scripts to the ESP32, you can use the `ampy` tool. Follow the steps below to install `ampy` and transfer the `main.py` file to the ESP32.

#### Installing `ampy`

1. Install `ampy` using `pip`:
   ```
   pip install adafruit-ampy
   ```

#### Transferring `main.py` to ESP32

1. Connect the ESP32 to your computer via USB.
2. Use the following command to transfer the `main.py` file to the ESP32:
   ```
   ampy --port /dev/ttyUSB0 put main.py
   ```
   Replace `/dev/ttyUSB0` with the appropriate serial port for your system.

## ESP32 Pinout Reference

For a complete guide to the ESP32 pinout, refer to this [link](https://ciksiti.com/ja/chapters/13091-esp32-pinout-reference--a-complete-guide).

## BLE Communication

### Using nRF Connect or LightBlue

1. Download and install the nRF Connect or LightBlue app on your iPhone.
2. Open the app and scan for BLE devices.
3. Connect to the ESP32 device.
4. Use the app to send commands to the ESP32 to control the servo motor.

## Device Configuration

### ESP32 Configuration

1. Ensure that the ESP32 is powered by the 9V battery and 3-terminal regulator.
2. Connect the servo motor and external button as described in the hardware connections section.
3. Upload the `main.py` file to the ESP32.

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
|  VIN        <--|--- Output pin (3-terminal regulator)
|  GND        <--|--- Ground pin (3-terminal regulator)
|                   |
|  GPIO 14 (Wake) <--|--- External button
+-------------------+
       |
       |
       v
+-------------------+
| 3-terminal regulator |
|                   |
|  Input pin  <--|--- Positive terminal (9V battery)
|  Ground pin <--|--- Ground terminal (9V battery)
+-------------------+
```

* **ESP32 Microcontroller**:
  * GPIO 15: Connect to the signal pin of the servo motor.
  * 3.3V: Connect to the power pin of the servo motor.
  * GND: Connect to the ground pin of the servo motor.
  * VIN: Connect to the output pin of the 3-terminal regulator.
  * GND: Connect to the ground pin of the 3-terminal regulator.
  * GPIO 14: Connect to an external button for waking up the ESP32 from DeepSleep mode.

* **Servo Motor**:
  * Signal pin: Connect to GPIO 15 of the ESP32.
  * Power pin: Connect to 3.3V of the ESP32.
  * Ground pin: Connect to GND of the ESP32.

* **3-terminal regulator**:
  * Input pin: Connect to the positive terminal of the 9V battery.
  * Ground pin: Connect to the ground terminal of the 9V battery.
  * Output pin: Connect to VIN of the ESP32.
  * Ground pin: Connect to GND of the ESP32.

* **9V Battery**:
  * Positive terminal: Connect to the input pin of the 3-terminal regulator.
  * Ground terminal: Connect to the ground pin of the 3-terminal regulator.

* **External Button**:
  * Connect to GPIO 14 of the ESP32 for waking up from DeepSleep mode.

## Power Management

The ESP32 is configured to use DeepSleep mode to reduce power consumption. The device will wake up from DeepSleep mode when the external button is pressed. After executing the servo motor command, the ESP32 will return to DeepSleep mode after 10 seconds.

## Troubleshooting

- If the ESP32 does not respond to commands from the BLE app, ensure that the BLE connection is established and the device is powered on.
- If the servo motor does not move, check the connections and ensure that the servo motor is receiving power.
- If the ESP32 does not wake up from DeepSleep mode, check the connection of the external button and ensure that it is connected to GPIO 14.
