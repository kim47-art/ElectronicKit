#!/usr/bin/env python
#encoding: utf8

import pigpio, sys   # ライブラリのインポート

gpio_PWM = 4    # 確認したい GPIO pin 番号
freq = (int)(sys.argv[1])   # コマンドライン引数で与えられた PWM 周波数

pi = pigpio.pi()   # GPIOにアクセスするためのインスタンスを作成
pi.set_mode(gpio_PWM,pigpio.OUTPUT)   # GPIO pin を出力設定
pi.set_PWM_frequency(gpio_PWM,freq)   # PWM 周波数の設定

print(pi.get_PWM_frequency(gpio_PWM))   # 実際に設定された PWM 周波数の読み込みと表示
pi.stop()   # pigpio リソースの開放