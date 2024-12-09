import CONFIG from './config.js';

let device;
let server;
let service;
let characteristic;

async function connect() {
    try {
        device = await navigator.bluetooth.requestDevice({
            filters: [{ service: [CONFIG.SERVICE_UUID] }]
        });
        server = await device.gatt.connect();
        service = await server.getPrimaryService(CONFIG.SERVICE_UUID);
        characteristic = await service.getCharacteristic(CONFIG.CHARACTERISTIC_UUID);
        console.log('Connected to ESP32');
        document.getElementById('connectionStatus').innerText = 'Connected';
    } catch (error) {
        console.error('Failed to connect', error);
        document.getElementById('connectionStatus').innerText = 'Failed to connect';
    }
}

async function toggleSwitch() {
    if (!characteristic) {
        console.error('Not connected to ESP32');
        return;
    }
    try {
        const command = new TextEncoder().encode('toggle');
        await characteristic.writeValue(command);
        console.log('Switch toggled');
    } catch (error) {
        console.error('Failed to toggle switch', error);
    }
}

document.getElementById('connectButton').addEventListener('click', async () => {
    await connect();
});

document.getElementById('toggleButton').addEventListener('click', async () => {
    if (!device || !device.gatt.connected) {
        await connect();
    }
    await toggleSwitch();
});
