'''
# @Author       : Chr_
# @Date         : 2021-04-01 23:39:46
# @LastEditors  : Chr_
# @LastEditTime : 2021-04-01 23:57:56
# @Description  : 
'''

import psutil
from typing import List

def get_sys_info()->List[str]:
    
    def graph_process(percent: int, length: int = 5):
        '''生成进度条，percent为进度[0-100]，length为长度'''
        percent_count = int(length*percent/100)
        return(f'{str(percent).rjust(4)}% {"#"*percent_count}{"_"*(length-percent_count)}')
    
    cpu_percent = psutil.cpu_percent()
    cpu_core = psutil.cpu_count(logical=False)
    cpu_load = [ round(x/cpu_core,1) for x in psutil.getloadavg()]
    

    mem = psutil.virtual_memory()
    mem_percent = mem.percent
    
    msg= [
        f'CPU {graph_process(cpu_percent)}',
        f'MEM {graph_process(mem_percent)}',
        f'LOD {cpu_load[0]} {cpu_load[1]} {cpu_load[2]}',
    ]
    return msg