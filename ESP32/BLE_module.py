import random
import struct
import time

import bluetooth
import config
import deepsleep_module
import servo_module
from machine import Pin
from micropython import const

# BLEイベントの定義
_IRQ_CENTRAL_CONNECT = const(1)  # セントラル機器が接続したときのイベント
_IRQ_CENTRAL_DISCONNECT = const(2)  # セントラル機器が切断したときのイベント
_IRQ_GATTS_WRITE = const(3)  # セントラル機器からデータを受信したときのイベント


# 各種フラグの定義
_FLAG_WRITE_NO_RESPONSE = const(0x0004)  # 応答なし書き込み可能
_FLAG_WRITE = const(0x0008)  # 書き込み可能


# ディスクリプタUUIDの定義
# _USER_DESCRIPTION_UUID = bluetooth.UUID(0x2901)

# サービスUUIDの定義
_SERVICE_UUID = bluetooth.UUID(config.SERVICE_UUID)
# サーボモータ動作用のキャラクタリスティック
_SERVO_CONTROL = (
    bluetooth.UUID(config.SERVO_CHAR_UUID),
    _FLAG_WRITE | _FLAG_WRITE_NO_RESPONSE,
    # ディスクリプタを追加
    # ((_USER_DESCRIPTION_UUID, bytes("Servo Control", "utf-8")),),
)
# Deepsleep用のキャラクタリスティック
_DEEPSLEE_CONTROL = (
    bluetooth.UUID(config.DEEPSLEEP_CHAR_UUID),
    _FLAG_WRITE | _FLAG_WRITE_NO_RESPONSE,
    # ディスクリプタを追加
    # ((_USER_DESCRIPTION_UUID, bytes("Deepsleep Control", "utf-8")),),
)
# Lチカ用のキャラクタリスティック
_LED_CONTROL = (
    bluetooth.UUID(config.LED_CHAR_UUID),
    _FLAG_WRITE | _FLAG_WRITE_NO_RESPONSE,
    # ディスクリプタを追加
    # ((_USER_DESCRIPTION_UUID, bytes("LED Control", "utf-8")),),
)

# GATTサーバに登録するためのサービス
_SERVICE = (
    _SERVICE_UUID,
    (_SERVO_CONTROL, _LED_CONTROL, _DEEPSLEE_CONTROL),
)

# アドバタイジングデータタイプの定義
_ADV_TYPE_FLAGS = const(0x01)  # フラグ
_ADV_TYPE_NAME = const(0x09)  # デバイス名
_ADV_TYPE_UUID16_COMPLETE = const(0x3)  # 16ビットUUID（完全なリスト）
_ADV_TYPE_UUID32_COMPLETE = const(0x5)  # 32ビットUUID（完全なリスト）
_ADV_TYPE_UUID128_COMPLETE = const(0x7)  # 128ビットUUID（完全なリスト）
_ADV_TYPE_UUID16_MORE = const(0x2)  # 16ビットUUID（不完全なリスト）
_ADV_TYPE_UUID32_MORE = const(0x4)  # 32ビットUUID（不完全なリスト）
_ADV_TYPE_UUID128_MORE = const(0x6)  # 128ビットUUID（不完全なリスト）
_ADV_TYPE_APPEARANCE = const(0x19)  # デバイスの外観

# 最大ペイロードサイズ
_ADV_MAX_PYLOAD = const(31)


class BLEPeripheral:
    """
    copilotに後で考えてもらう
    """

    def __init__(self, ble, name="esp32"):
        """
        Parameters
        ----------
        ble : BLE object
            BLEオブジェクト
        name : str, optional
            デバイス名, by default "esp32"
        """

        self._ble = ble
        self._ble.active(True)  # BLEを有効化
        self._ble.irq(self._irq)  # イベントハンドラを設定
        # GATTサーバにサービスを登録
        ((self._handle_servo, self._handle_deepsleep, self._handle_led),) = (
            self._ble.gatts_register_services((_SERVICE,))
        )
        self._connections = set()  # 接続中のデバイスを管理
        # アドバタイジングペイロードを準備
        self._payload = self._advertising_payload(
            name=name, services=[_SERVICE_UUID]
        )
        self._advertise()  # アドバタイジング開始

        # LED用のピンを初期化
        self._led = Pin(2, Pin.OUT)
        # LED制御用のフラグ
        self._led_active = False
        # LEDの点滅回数を管理
        self._blink_count = 0
        self._MAX_BLINKS = 3

    def _irq(self, event, data):
        """
        IRQハンドラ（BLEのイベントハンドラ）

        Parameters
        ----------
        event :
            ESP32で自動生成する
        data :
            ペリフェラルからの受信データが渡される
        """

        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, _, _ = data
            print("New connection", conn_handle)
            self._connections.add(conn_handle)

        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _ = data
            print("Disconnected", conn_handle)
            self._connections.remove(conn_handle)
            self._advertise()  # 再度アドバタイジングを開始

        elif event == _IRQ_GATTS_WRITE:
            # データ受信時の処理
            # conn_handle: 接続しているデバイスの識別子
            # value_handle: 書き込まれたキャラクタリスティックのハンドル
            conn_handle, value_handle = data

            # # 書き込まれたデータを読み取る
            # value = self._ble.gatts_read(value_handle)

            # 受信データがSERVOキャラクタリスティックの場合
            if value_handle == self._handle_servo:
                # servo.main()を呼び出す
                print("Start servo")
                servo_module.main()

            # 受信データがDeepsleepキャラクタリスティックの場合
            elif value_handle == self._handle_deepsleep:
                # deepsleepを実行
                print("Start deepsleep")
                deepsleep_module.main()

            # 受信データがLEDキャラクタリスティックの場合
            elif value_handle == self._handle_led:
                # Lチカを実行
                print("Start LED")
                self._led_active = True
                self._blink_count = 0

    def process(self):
        """
        メインループで実行する処理
        """

        if self._led_active and self._blink_count < self._MAX_BLINKS:
            self._led.on()
            time.sleep_ms(500)
            self._led.off()
            time.sleep_ms(500)
            self._blink_count += 1
            if self._blink_count >= self._MAX_BLINKS:
                self._led_active = False
                print("LED blinking completed")

    def _advertise(self, interval_us=500000):
        """
        アドバタイジングの開始

        Parameters
        ----------
        interval_us : int, optional
            インターバル時間（マイクロ秒）, by default 500000
        """

        print("Start advertising...")
        self._ble.gap_advertise(interval_us, adv_data=self._payload)

    def _advertising_payload(
        self,
        limited_disc=False,
        br_edr=False,
        name=None,
        services=None,
        appearance=0,
    ):
        """
        アドバタイジングペイロードを生成する関数

        Parameters
        ----------
        limited_disc : bool, optional
            限定的なディスカバリーモード, by default False
        br_edr : bool, optional
            BR/EDR対応フラグ, by default False
        name : string, optional
            デバイス名, by default None
        services : list or taple, optional
            提供するサービスのUUIDリスト, by default None
        appearance : int, optional
            デバイスの外観コード, by default 0
        """

        payload = bytearray()

        def _append(adv_type, value):
            # ペイロードにデータを追加する内部関数
            nonlocal payload
            payload += struct.pack("BB", len(value) + 1, adv_type) + value

        # フラグの設定
        _append(
            _ADV_TYPE_FLAGS,
            struct.pack(
                "B",
                (0x01 if limited_disc else 0x02) + (0x18 if br_edr else 0x04),
            ),
        )

        # デバイス名の設定
        if name:
            _append(_ADV_TYPE_NAME, name.encode())

        # サービスUUIDの設定
        if services:
            for uuid in services:
                b = bytes(uuid)
                if len(b) == 2:
                    _append(_ADV_TYPE_UUID16_COMPLETE, b)
                elif len(b) == 4:
                    _append(_ADV_TYPE_UUID32_COMPLETE, b)
                elif len(b) == 16:
                    _append(_ADV_TYPE_UUID128_COMPLETE, b)

        # デバイスの外観の設定
        if appearance:
            _append(_ADV_TYPE_APPEARANCE, struct.pack("<h", appearance))

        if len(payload) > _ADV_MAX_PYLOAD:
            raise ValueError(
                f"advertising payload too large\r\npayload: {payload}\r\nlength: {len(payload)}"
            )

        return payload


def main():
    ble = bluetooth.BLE()
    device_name = "esp32"

    # GAP名を設定
    ble.config(gap_name=device_name)

    p = BLEPeripheral(ble=ble, name=device_name)

    while True:
        # メインループでLED制御を実行
        p.process()
        time.sleep_ms(100)  # 適度な間隔でループを回し、CPU負荷を軽減


if __name__ == "__main__":
    main()
