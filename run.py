#!/usr/bin/python3
'''
# @Author       : Chr_
# @Date         : 2021-03-29 22:40:39
# @LastEditors  : Chr_
# @LastEditTime : 2021-04-03 00:27:38
# @Description  : 启动文件
'''

import RPi.GPIO as GPIO
from obj import Pi_2FA

KEYS = [5, 6, 13, 19]

pi_2fa = Pi_2FA()


def btn_callback(key):
    if pi_2fa.Ready:
        if key == KEYS[0]:
            pi_2fa.page_down()
        elif key == KEYS[1]:
            pi_2fa.page_up()
        elif key ==KEYS[2]:
            pi_2fa.switch_mode()
        elif key ==KEYS[3]:
            pi_2fa.none_mode()
        else:
            print(key)
            return


GPIO.setmode(GPIO.BCM)
for key in KEYS:
    GPIO.setup(key, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(
        key, GPIO.RISING, callback=btn_callback, bouncetime=200)

if __name__ == '__main__':
    print('start')
    try:
        while True:
            if pi_2fa.Ready:
                pi_2fa.check_time()
            continue
    except KeyboardInterrupt:
        print('end')
    pi_2fa.EPD.Clear(0xff)  
    GPIO.cleanup()