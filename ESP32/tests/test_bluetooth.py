# Claudeで作成、要修正

import struct

import bluetooth
import test_servo
from bluetooth import BLE

# BLEオブジェクトの初期化
ble = BLE()
ble.active(True)


# サービスとキャラクタリスティックのUUID定義
SERVICE_UUID = bluetooth.UUID("12345678-1234-5678-1234-56789abcdef0")
CHAR_UUID = bluetooth.UUID("87654321-4321-6789-4321-0fedcba98765")


# GATTサーバの実装クラス
class BLEServoControl:
    def __init__(self):
        # 内部変数の初期化
        self._handle = None
        self._ble = ble

        # アドバタイズの設定
        self._ble.config(gap_name="Servo Control")
        self._connections = set()

        # GATTサーバのコールバック登録
        self._ble.irq(self._irq)

        # サービスの作成
        self._service = bluetooth.Service(SERVICE_UUID)
        self._char = bluetooth.Characteristic(
            CHAR_UUID,
            bluetooth.FLAG_WRITE
            | bluetooth.FLAG_NOTIFY,  # 書き込みと通知を有効化
        )
        self._service.addCharacteristic(self._char)

        # BLEスタックにサービスを登録
        self._ble.gatts_register_services([self._service])

        # アドバタイジング開始
        self._advertise()

    def _irq(self, event, data):
        # BLEイベントの処理
        if event == bluetooth.IRQ_CENTRAL_CONNECT:
            # セントラルデバイスが接続した時の処理
            conn_handle, addr_type, addr = data
            self._connections.add(conn_handle)
            print("Disconnected from central device")

        elif event == bluetooth.IRQ_CENTRAL_DISCONNECT:
            # セントラルデバイスが切断した時の処理
            conn_handle, addr_type, addr = data
            if conn_handle in self._connections:
                self._connections.remove(conn_handle)
            print("Disconnected from central device")
            # 切断後、再度アドバタイジングを開始
            self._advertise()

        elif event == bluetooth.IRQ_GATTS_WRITE:
            # キャラクタリスティックに書き込みがあった時の処理
            conn_handle, value_handle = data
            # 書き込まれた値を取得
            value = self._ble.gatts_read(value_handle)
            # 値が存在する場合、test_servo.main()を呼び出し
            if value == b"toggle":
                print("Received toggle command")
                test_servo.main()

    def _advertise(self, interval_us=500000):
        # アドバタイジングの開始
        self._ble.gap_advertise(
            interval_us, adv_data=self._advertising_payload()
        )

    def _advertising_payload(self):
        # アドバタイジングペイロードの生成
        payload = bytearray()

        # デバイス名の追加
        device_name = "Servo Control"
        payload += (
            struct.pack("BB", len(device_name) + 1, 0x09)
            + device_name.encode()
        )

        # サービスUUIDの追加
        payload += struct.pack(
            "BB", 17, 0x07
        )  # 長さ、タイプ（完全な128ビットサービスUUID）
        payload += SERVICE_UUID.pack()

        return payload


# メインの実行部分
def main():
    ble_servo = BLEServoControl()

    # メインループ
    while True:
        pass  # イベントはIRQハンドラで処理されます


if __name__ == "__main__":
    main()
