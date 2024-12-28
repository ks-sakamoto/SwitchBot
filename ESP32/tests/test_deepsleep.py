"""
DeepSleepへの移行とDeepSleepからの復帰をテスト
"""

import machine
from machine import Pin

import esp32


class DeepSleep:
    def __init__(self, pin) -> None:
        # ウェイクアップピンの設定
        self.wake_pin = Pin(pin, mode=Pin.IN, pull=Pin.PULL_UP)
        # ウェイクアップ要因の設定
        esp32.wake_on_ext0(pin=self.wake_pin, level=esp32.WAKEUP_ALL_LOW)

    def start_deepsleep(self, time_ms) -> None:
        """DeepSleepモードの開始"""
        print("Going to deep sleep...")
        machine.deepsleep(time_ms)


def main() -> None:
    sleep_controller = DeepSleep(27)

    # DeepSleepモードを開始
    sleep_controller.start_deepsleep(10000)


if __name__ == "__main__":
    main()
