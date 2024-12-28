"""
電池駆動の確認をするためのテストスクリプト
- BLE起動
  - test_bluetooth内でLチカとサーボモータのテストを実行可能
- deepsleepの開始
"""

import test_bluetooth

if __name__ == "__main__":
    # BLE起動
    test_bluetooth.main()
