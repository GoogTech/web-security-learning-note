import html

def html_encode(input_str):
    # 使用 html.escape 进行基础转义, 详情见源码
    encoded_str = html.escape(input_str, quote=False)
    
    # 手动替换特定字符
    encoded_str = encoded_str.replace(" ", "&#32;")   # 空格
    encoded_str = encoded_str.replace("|", "&#124;") # 管道符
    encoded_str = encoded_str.replace("'", "&#39;")  # 单引号
    encoded_str = encoded_str.replace("~", "&#126;") # 波浪号
    return encoded_str

raw_string = "1 UNION SELECT concat(username,' : ',password) FROM users"
print(f"The encoded str: {html_encode(raw_string)}")