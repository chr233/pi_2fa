'''
# @Author       : Chr_
# @Date         : 2021-03-30 17:04:42
# @LastEditors  : Chr_
# @LastEditTime : 2021-04-03 23:01:07
# @Description  : 令牌生成器
'''

import hmac
import hashlib
from base64 import b64decode,b32decode
from time import time
import struct


def get_time()->int:
    return int(time() / 30)

def get_steam_auth_code(secret: str, t: int=None) -> str:
    '''
    生成令牌
    '''
    try:
        if not t:
            t = int(time()/30)
        msg = struct.pack(">Q", t)
        key = b64decode(secret)
        mac = hmac.new(key, msg, hashlib.sha1).digest()
        offset = mac[-1] & 0x0f
        binary = struct.unpack('>L', mac[offset:offset+4])[0] & 0x7fffffff
        codestr = list('23456789BCDFGHJKMNPQRTVWXY')
        chars = []
        for _ in range(5):
            chars.append(codestr[binary % 26])
            binary //= 26
        code = ''.join(chars)
    except Exception as e:
        print(e)
        code='ERROR'        
    return code

 
def get_totp_auth_code(secret:str,t:int=None):
    try:
        if not t:
            t = int(time() / 30)
        key = b32decode(secret)
        msg = struct.pack(">Q", t)
        mac = hmac.new(key, msg, hashlib.sha1).digest()
        offset = mac[-1] & 0x0f
        binary = struct.unpack('>L', mac[offset:offset+4])[0] & 0x7fffffff
        code = str(binary)[-6:].zfill(6)
    except Exception as e:
        print(e)
        code = 'ERROR'
    return code