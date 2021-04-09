'''
# @Author       : Chr_
# @Date         : 2021-03-30 17:04:24
# @LastEditors  : Chr_
# @LastEditTime : 2021-04-09 19:56:43
# @Description  : 图片生成器
'''

import time
from os import path
from typing import List, Tuple
from PIL import Image, ImageDraw, ImageFont

SCREEN_W = 264
SCREEN_H = 176

CODE_W = 115
CODE_H = 27

ICON_W = 20
ICON_H = 44

CLOCK_W = SCREEN_W-ICON_W - CODE_W
CLOCK_H = SCREEN_H

FONT_CODE = ImageFont.truetype(path.join('font', 'Courier Prime Code.ttf'), 25)
FONT_TAG = ImageFont.truetype(path.join('font', 'CascadiaMono.ttf'), 12)

FONT_PAGE = ImageFont.truetype(
    path.join('font', 'sarasa-fixed-sc-regular.ttf'), 15)


FONT_ICO = ImageFont.truetype(
    path.join('font', 'sarasa-fixed-sc-regular.ttf'), 22)


FONT_CLOCK = ImageFont.truetype(path.join('font', 'hartland.ttf'), 50)
FONT_DATE = ImageFont.truetype(path.join('font', 'hartland.ttf'), 23)
FONT_APM = ImageFont.truetype(path.join('font', 'sarasa-fixed-sc-regular.ttf'), 13)
FONT_TIPS = ImageFont.truetype(
    path.join('font', 'sarasa-fixed-sc-regular.ttf'), 13)


def generate_2fa_img(data: List[Tuple[str, str]], page: Tuple[int, int] = (1, 1), active: bool = True, tips: List[str] = None) -> Image:

    def draw_icon() -> Image:
        '''绘制图标'''
        img = Image.new('L', (ICON_W, SCREEN_H), 0xff)
        w, h = FONT_ICO.getsize('▲')
        draw = ImageDraw.Draw(img)

        ICO_TXT = ['▲', '▼', '●', '■'] if active else ['△', '▽', '○', '□']

        for i in range(4):
            x, y = (ICON_W-w)/2+1, i*44+(44-h)/2
            draw.text((x, y), ICO_TXT[i], font=FONT_ICO, fill=0x00)

        return img

    def draw_auth() -> Image:
        '''绘制令牌'''

        def draw_auth_single(name: str, code: str) -> Image:
            '''绘制单个令牌'''
            # 计算尺寸
            w1, h1 = FONT_CODE.getsize(code)
            w2, h2 = FONT_TAG.getsize(name[:3])
            W2, H2 = CODE_H, 18
            W1, H1 = CODE_W-H2, CODE_H

            # 画令牌
            im_code = Image.new('L', (CODE_W, CODE_H), 0xff)
            draw_code = ImageDraw.Draw(im_code)
            draw_code.text(((W1-w1)/2, (H1-h1)/2),
                           code, font=FONT_CODE, fill=0x00)
            # 画名称
            im_name = Image.new('L', (W2, H2), 0xff)
            draw_name = ImageDraw.Draw(im_name)
            draw_name.text(((W2-w2)/2, (H2-h2)/2-2),
                           name[:3], font=FONT_TAG, fill=0x00)
            draw_name.line(((0, 0), (W2, 0)), fill=0x00, width=1)
            im_name = im_name.rotate(angle=90, expand=True)
            im_code.paste(im_name, (W1, 0))
            draw_code.rectangle((0, 0, CODE_W-1, CODE_H), outline=0)
            return im_code

        def draw_page_info() -> Image:
            '''绘制页码'''
            PAGE_H = SCREEN_H-6*CODE_H+2
            im_page = Image.new('L', (CODE_W, PAGE_H), 0xff)
            draw = ImageDraw.Draw(im_page)
            draw.rectangle((0, 0, CODE_W-1, PAGE_H), outline=0)

            curr, total = page
            curr -= 1
            if total < 1:
                total = 1
            if curr > total:
                curr = 0
            pages = ['-'] * total
            
            if active:
                pages[curr] = '≡'
            else:
                pages[curr] = '≡'
                
            page_str = ' '.join(pages)
            wp, hp = FONT_PAGE.getsize(page_str)

            draw.text(((CODE_W-wp)/2, (PAGE_H-hp)/2-2),
                      page_str, font=FONT_PAGE, fill=0x00)
            return im_page

        img = Image.new('L', (CODE_W, SCREEN_H), 0xff)

        y = -1
        for name, code in data[:6]:
            img_code = draw_auth_single(name, code)
            img.paste(img_code, (0, y))
            y += img_code.height

        img_page = draw_page_info()
        img.paste(img_page, (0, y))

        return img

    def draw_clock() -> Image:
        '''绘制时钟'''
        img = Image.new('L', (CLOCK_W, CLOCK_H), 0xff)
        draw = ImageDraw.Draw(img)

        t=time.localtime()
        time_str = time.strftime("%I:%M", t)
        date_str = time.strftime("%Y-%m-%d", t)
        is_am = time.strftime("%p",t)=='AM'
        apm_str ='上午'if is_am  else '下午'

        # 画时钟
        wc, hc = FONT_CLOCK.getsize(time_str)
        wd, hd = FONT_DATE.getsize(date_str)
        wp, hp = FONT_APM.getsize(apm_str)
        
        draw.text(((CLOCK_W-wc)/2+3, 15), time_str, font=FONT_CLOCK, fill=0x00)
        draw.text(((CLOCK_W-wd)/2+3, 70), date_str, font=FONT_DATE, fill=0x00)

        # 画上下午
        if is_am:
            x=(CLOCK_W-wd)/2+1
        else:
            x=(CLOCK_W-wd)/2+wd-wp-1
        draw.text((x, 8), apm_str, font=FONT_APM, fill=0x00)

        # 画提示
        for i, tip in enumerate(tips, 0):
            wt, ht = FONT_TIPS.getsize(tip)
            draw.text(((CLOCK_W-wt)/2, 110+(ht+5)*i),
                      tip, font=FONT_TIPS, fill=0x00)

        return img

    if not active:
        data = [('---', '-----')] * 6

    if len(data) < 6:
        data += [('---', '-----')] * 6

    if not tips:
        tips = ['By Chr_', 'Ver 0.01', 'chrxw.com']

    full_img = Image.new('L', (SCREEN_W, SCREEN_H), 0xff)

    img_auth = draw_auth()
    full_img.paste(img_auth, (ICON_W, 0))

    img_icon = draw_icon()
    full_img.paste(img_icon, (0, 0))

    img_clock = draw_clock()
    full_img.paste(img_clock, (ICON_W+CODE_W, 0))

    # with open('o.png', 'wb') as f:
    #     full_img.save(f, 'png')

    return full_img
