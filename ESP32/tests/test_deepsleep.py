"""
DeepSleepへの移行とDeepSleepからの復帰をテスト
"""

import time

import machine
from machine import Pin

import esp32


class DeepSleep:
    def __init__(self, pin) -> None:
        # ウェイクアップピンの設定
        self.wake_pin = Pin(pin, mode=Pin.IN, pull=Pin.PULL_UP)
        # ウェイクアップ要因の設定
        esp32.wake_on_ext0(pin=self.wake_pin, level=esp32.WAKEUP_ALL_LOW)

        # 以下は、稼働中のボタンによる割込み処理のため不要
        # 今回はDeepSleepからのウェイクアップにボタンを使用する
        # self.wake_pin.irq(
        #     trigger=Pin.IRQ_FALLING, handler=lambda pin: machine.deepsleep()
        # )

    def start_deepsleep(self) -> None:
        """DeepSleepモードの開始"""
        print("Going to deep sleep...")
        machine.deepsleep()

    # ウェイクアップ後はリブートされるためウェイクアップ要因を取得する意味はない
    # def get_wake_reason(self) -> None:
    #     """ウェイクアップの要因を取得"""
    #     return machine.reset_cause()


def main() -> None:
    sleep_controller = DeepSleep(4)

    # # リセット要因を確認
    # wake_reason = sleep_controller.get_wake_reason()

    # if wake_reason == machine.PIN_WAKE:
    #     print("Wake up from deep sleep!")
    #     print(f"Wake up reason: {wake_reason}")
    #     # ウェイクアップ後の処理
    #     print("Working for 10 seconds...")
    #     time.sleep(10)  # 10秒待機
    # else:
    #     print("First time boot")

    # DeepSleepモードを開始
    sleep_controller.start_deepsleep(10000)


if __name__ == "__main__":
    main()
