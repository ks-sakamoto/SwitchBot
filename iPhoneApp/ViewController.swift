import UIKit
import CoreBluetooth

class ViewController: UIViewController {

    var centralManager: CBCentralManager!
    var esp32Peripheral: CBPeripheral?

    let serviceUUID = CBUUID(string: "12345678-1234-5678-1234-56789abcdef0")
    let characteristicUUID = CBUUID(string: "87654321-4321-6789-4321-0fedcba98765")

    override func viewDidLoad() {
        super.viewDidLoad()
        centralManager = CBCentralManager(delegate: self, queue: nil)
    }

    @IBAction func toggleSwitch(_ sender: UIButton) {
        if let peripheral = esp32Peripheral {
            let command = "toggle"
            if let data = command.data(using: .utf8) {
                peripheral.writeValue(data, for: characteristicUUID, type: .withResponse)
            }
        }
    }
}

extension ViewController: CBCentralManagerDelegate, CBPeripheralDelegate {

    func centralManagerDidUpdateState(_ central: CBCentralManager) {
        if central.state == .poweredOn {
            centralManager.scanForPeripherals(withServices: [serviceUUID], options: nil)
        } else {
            print("Bluetooth is not available.")
        }
    }

    func centralManager(_ central: CBCentralManager, didDiscover peripheral: CBPeripheral, advertisementData: [String : Any], rssi RSSI: NSNumber) {
        if peripheral.name?.contains("ESP32") == true {
            esp32Peripheral = peripheral
            esp32Peripheral?.delegate = self
            centralManager.stopScan()
            centralManager.connect(esp32Peripheral!, options: nil)
        }
    }

    func centralManager(_ central: CBCentralManager, didConnect peripheral: CBPeripheral) {
        peripheral.discoverServices([serviceUUID])
    }

    func peripheral(_ peripheral: CBPeripheral, didDiscoverServices error: Error?) {
        if let services = peripheral.services {
            for service in services {
                if service.uuid == serviceUUID {
                    peripheral.discoverCharacteristics([characteristicUUID], for: service)
                }
            }
        }
    }

    func peripheral(_ peripheral: CBPeripheral, didDiscoverCharacteristicsFor service: CBService, error: Error?) {
        if let characteristics = service.characteristics {
            for characteristic in characteristics {
                if characteristic.uuid == characteristicUUID {
                    let command = "toggle"
                    if let data = command.data(using: .utf8) {
                        peripheral.writeValue(data, for: characteristic, type: .withResponse)
                    }
                }
            }
        }
    }
}
