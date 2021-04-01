'''
# @Author       : Chr_
# @Date         : 2021-04-01 11:49:31
# @LastEditors  : Chr_
# @LastEditTime : 2021-04-02 01:03:52
# @Description  : 启动入口
'''

from typing import  List, Tuple

from datetime import datetime

from waveshare_epd import epd2in7
from utils.img import generate_2fa_img
from utils.twofa import get_time, get_steam_auth_code, get_totp_auth_code
from utils.sysinfo import get_sys_info
from utils.weather import get_weather_report

from config import secrets, city


class Pi_2FA(object):
    count_2fa: int = 1
    curr_page: int = 0
    page_count: int = 0
    time_2fa: int = 0
    secrets: List[Tuple[str, str]] = secrets
    weather: List[str] = []

    Ready: bool = True
    Mode: int = 1
    Show: bool = False
    Minute: int = 0
    Day: int = 0

    EPD: epd2in7.EPD

    def __init__(self) -> None:
        self.EPD = epd2in7.EPD()
        self.EPD.init()

        self.page_count = len(self.secrets) // 6 + 1
        self.curr_page = 1

    def page_up(self):
        self.Show=True
        self.count_2fa =3
        self.Minute = -1
        if self.curr_page >= self.page_count:
            self.curr_page = 1
        else:
            self.curr_page += 1

    def page_down(self):
        self.Show=True
        self.count_2fa =3
        self.Minute = -1
        if self.curr_page <= 1:
            self.curr_page = self.page_count
        else:
            self.curr_page -= 1

    def switch_mode(self):
        if self.Mode >= 3 or self.Mode <= 0:
            self.Mode = 1
        else:
            self.Mode += 1
        self.Minute = -1

    def none_mode(self):
        self.Show = not self.Show
        if self.Show:
            self.count_2fa = 3
            self.Minute = -1
            

    def update_screen(self):
        self.Ready = False
        self.time_2fa = get_time()
        start = (self.curr_page-1)*6
        secs = self.secrets[start:start+6]
        twofas = []
        if self.Show:
            for name, type, secret in secs:
                if type == 'S':
                    code = get_steam_auth_code(secret, self.time_2fa)
                elif type == 'T':
                    code = get_totp_auth_code(secret, self.time_2fa)
                else:
                    code = 'FAIL!'
                twofas.append((name, code))

        if self.Mode == 1:
            tips = get_sys_info()
        elif self.Mode == 2:
            tips = self.weather
        elif self.Mode == 3:
            tips = ['blog.chrxw.com', 'By Chr_', 'Ver 0.0.2']
            
        img = generate_2fa_img(
            twofas, (self.curr_page, self.page_count), self.Show, tips)
        self.EPD.display(img)
        self.Ready = True

    def check_time(self):
        now = datetime.now()
        day = now.day
        minute = now.minute

        update = False

        if day != self.Day:
            self.weather = get_weather_report(city=city)
            self.Day = day

        if minute != self.Minute:
            self.Minute = minute
            update=True

        if self.Show:
            t = get_time()
            if t != self.time_2fa:
                update = True
                self.count_2fa -= 1
                self.time_2fa = t
                if self.count_2fa <= 0:
                    self.Show = False

        if update:
            self.update_screen()