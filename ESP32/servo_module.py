import time

from machine import PWM, Pin


class Servo:
    def __init__(self, pin) -> None:
        # PWMの設定(周波数50Hz)
        self.servo = PWM(Pin(pin), freq=50)
        # デューティサイクルの範囲を設定
        # 0.5ms（0度） = 2.5% duty
        # 2.4ms（180度） = 12% duty
        self.min_duty = 26  # 0.5ms/20ms * 1024
        self.max_duty = 123  # 2.4ms/20ms * 1024
        self.defalut_duty = 103  # 初期角度duty

        # サーボモータの動作音を止めるため(これによって角度は変わらない)
        time.sleep(1)
        self.servo.duty(0)

    def set_angle(self, duty=120) -> None:
        """
        角度を設定し、サーボモータを動作させる。
        動作後は初期角度に戻す。

        Parameters
        ----------
        angle : fload
            サーボモータを動作させる角度
        duty : int
            サーボモータを動作させるデューティー比（本来はangleにしたい）
        """
        # duty = int(
        #     self.min_duty + (self.max_duty - self.min_duty) * angle / 180
        # )
        time.sleep(2)
        self.servo.duty(duty)

    def set_default_angle(self) -> None:
        """サーボモータを初期角度に戻す"""
        time.sleep(2)
        self.servo.duty(self.defalut_duty)
        time.sleep(1)
        self.servo.duty(0)

    def stop(self) -> None:
        time.sleep(1)
        self.servo.duty(self.defalut_duty)
        time.sleep(2)
        self.servo.deinit()


def main(duty=120):
    # GPIO15番ピンにサーボモータを接続
    servo = Servo(26)

    # サーボモータ始動
    print("start servo")
    servo.set_angle(duty)
    servo.set_default_angle()

    # サーボモータ停止
    servo.stop()
    print("stop servo")


if __name__ == "__main__":
    main()
