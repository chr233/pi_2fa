'''
# @Author       : Chr_
# @Date         : 2021-02-27 00:49:27
# @LastEditors  : Chr_
# @LastEditTime : 2021-04-02 00:37:55
# @Description  : 配置文件
'''

# 每一项的第一个值为令牌名称,显示在右边
# 第二个值为令牌类型,S:STEAM令牌,P:TOTP令牌(谷歌Auth)
# 第三个值为令牌Secret,这个需要手动从令牌客户端提取,为Base64编码格式

secrets = [
    ('abc', 'S', 'MTIzZGFyZHNhYWRmYWQ='),
]

# 要显示天气的城市名称

city = '杭州'