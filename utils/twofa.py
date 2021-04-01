'''
# @Author       : Chr_
# @Date         : 2021-03-30 17:04:42
# @LastEditors  : Chr_
# @LastEditTime : 2021-04-01 23:10:19
# @Description  : 令牌生成器
'''

import hmac
import hashlib
from base64 import b64decode,b32decode
from time import time
import struct


def get_time()->int:
    return int(time() / 30)

def get_steam_auth_code(secret: str, time: int) -> str:
    '''
    生成令牌
    '''
    def bytes_to_int(bytes):
        result = 0
        for b in bytes:
            result = result * 256 + int(b)
        return result

    try:
        t = time.to_bytes(8, 'big')
        key = b64decode(secret)
        h = hmac.new(key, t, hashlib.sha1)
        signature = list(h.digest())
        start = signature[19] & 0xf
        fc32 = bytes_to_int(signature[start:start + 4])
        fc32 &= 0x7FFFFFFF
        fullcode = list('23456789BCDFGHJKMNPQRTVWXY')
        chars = []
        for i in range(5):
            chars.append(fullcode[fc32 % 26])
            fc32 //= 26
        code = ''.join(chars)
    except Exception as e:
        print(e)
        code='ERROR'        
    return code

 
def get_totp_auth_code(secret:str,time:int):
    try:
        key = b32decode(secret)
        msg = struct.pack(">Q", time)
        mac = hmac.new(key, msg, hashlib.sha1).digest()
        offset = mac[-1] & 0x0f
        binary = struct.unpack('>L', mac[offset:offset+4])[0] & 0x7fffffff
        code= str(binary)[-6:].zfill(6)
    except Exception as e:
        print(e)
        code = 'ERROR'
    return code