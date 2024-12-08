# SwitchBot System

This project is a SwitchBot system that allows you to control a physical switch using an iPhone via Bluetooth Low Energy (BLE). The system consists of an ESP32 microcontroller, a servo motor, and a web interface using WebBluetooth.

## Table of Contents

- [Requirements](#requirements)
- [System Overview](#system-overview)
- [ESP32 Setup](#esp32-setup)
- [ESP32 Pinout Reference](#esp32-pinout-reference)
-  [Web Interface](#web-interface)
- [Device Configuration](#device-configuration)

## Requirements

- ESP32 microcontroller
- Servo motor
- Battery box (2x AAA batteries)
- iPhone with Bluefy browser
- MicroPython

## System Overview

The SwitchBot system consists of the following components:

1. **ESP32 Microcontroller**: The main controller that communicates with the iPhone via WebBluetooth and controls the servo motor.
2. **Servo Motor**: Used to press the physical switch.
3. **Battery Box**: Provides power to the ESP32 and servo motor.
4. **Web Interface**: Communicates with the ESP32 via WebBluetooth to control the servo motor.

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

## Web Interface

### Building the Web Interface

1. Create an `index.html` file with a basic HTML structure and a button to toggle the switch.
2. Create a `script.js` file to implement the WebBluetooth logic to connect to the ESP32 and send the toggle command.

### Using the Web Interface

1. Open the Bluefy browser on your iPhone.
2. Navigate to the GitHub Pages URL where the web interface is hosted.
3. Click the "Toggle Switch" button to connect to the ESP32 and control the servo motor.

### Hosting the Web Interface on GitHub Pages

1. Create a new repository on GitHub and add the `index.html` and `script.js` files to the repository.
2. Enable GitHub Pages for the repository by going to the repository settings and selecting the `main` branch as the source for GitHub Pages.
3. The web interface will be available at `https://<username>.github.io/<repository-name>/`.

## Device Configuration

### ESP32 Configuration

1. Ensure that the ESP32 is powered by the battery box.
2. Connect the servo motor and external button as described in the hardware connections section.
3. Upload the `main.py` file to the ESP32.

### Web Interface Configuration

1. Ensure that Bluetooth is enabled on your iPhone.
2. Open the Bluefy browser and navigate to the GitHub Pages URL where the web interface is hosted.
3. Use the web interface to control the servo motor and press the switch.

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

- If the ESP32 does not respond to commands from the web interface, ensure that the WebBluetooth connection is established and the device is powered on.
- If the servo motor does not move, check the connections and ensure that the servo motor is receiving power.
- If the ESP32 does not wake up from DeepSleep mode, check the connection of the external button and ensure that it is connected to GPIO 14.
