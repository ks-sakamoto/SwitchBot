// 設定ファイルからBluetooth UUIDを読み込み
import CONFIG from './config.js';

// Bluetooth接続に必要なグローバル変数
let device; // Bluetoothデバイスのインスタンス
let server; // GATTサーバのインスタンス
let service; // Bluetoothサービス群のインスタンス
let characteristic; // 目的のサービス（データの送受信用）

/**
* ESP32デバイスへのBluetooth接続を確立する
* - デバイスの検出
* - GATTサーバへの接続
* - サービス群と目的のサービスを取得
*/
async function connect() {
    try {
        // Bluetoothデバイスの検出を要求
        device = await navigator.bluetooth.requestDevice({
            filters: [{ service: [CONFIG.SERVICE_UUID] }]
        });
        // GATTサーバに接続
        server = await device.gatt.connect();
        // 指定されたUUIDのサービス群を取得
        service = await server.getPrimaryService(CONFIG.SERVICE_UUID);
        // サービス群から目的のサービスを取得
        characteristic = await service.getCharacteristic(CONFIG.CHARACTERISTIC_UUID);
        // 接続成功を通知
        console.log('Connected to ESP32');
        document.getElementById('connectionStatus').innerText = 'Connected';
    } catch (error) {
        // 接続エラーの処理
        console.error('Failed to connect', error);
        document.getElementById('connectionStatus').innerText = 'Failed to connect';
    }
}

/**
 * サーボモータのスイッチ状態を切り替える
 * - 接続確認
 * - 'toggle'コマンドの送信
 */
async function toggleSwitch() {
    // 目的のサービスが取得出来ていない場合は処理中断
    if (!characteristic) {
        console.error('Not connected to ESP32');
        return;
    }
    try {
        // 'toggle'コマンドをバイナリデータに変換
        const command = new TextEncoder().encode('toggle');
        // デバイスにコマンドを送信
        await characteristic.writeValue(command);
        console.log('Switch toggled');
    } catch (error) {
        console.error('Failed to toggle switch', error);
    }
}

// 接続ボタンのクリックイベントハンドラ
document.getElementById('connectButton').addEventListener('click', async () => {
    await connect();
});

// トグルボタンのクリックイベントハンドラー
document.getElementById('toggleButton').addEventListener('click', async () => {
    // 未接続の場合は再接続を試みる
    if (!device || !device.gatt.connected) {
        await connect();
    }
    // サーボモータスイッチの切り替えを実行
    await toggleSwitch();
});
