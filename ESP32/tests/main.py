"""
電池駆動の確認をするためのテストスクリプト
- 内臓LEDのLチカ
- サーボモータの起動
- deepsleepの開始
"""

import time

import test_deepsleep
import test_servo
from machine import Pin

if __name__ == "__main__":
    # 内臓LEDピンは2番
    pin = Pin(2, Pin.OUT)

    # Lチカ3回
    for _ in range(3):
        time.sleep(1)
        pin.on()  # LEDオン
        time.sleep(1)
        pin.off()  # LEDオフ

    # サーボモータ起動
    test_servo.main()

    # deepsleep開始
    test_deepsleep.main()
