# CSRF 基础知识学习笔记

* 杜绝CSRF的方案之 SameSite cookies：http://www.mi1k7ea.com/2021/01/16/%E6%9D%9C%E7%BB%9DCSRF%E7%9A%84%E6%96%B9%E6%A1%88%EF%BC%9ASameSite-cookies/

* 使用 Same-Site Cookie 属性防止 CSRF 攻击：https://www.tubring.cn/articles/same-site-cookie-attribute-prevent-cross-site-request-forgery

* [Day24] Same-site cookie，CSRF 的救星？：https://ithelp.ithome.com.tw/articles/10326413

  顺便可以读读前篇文章，十分推荐：[Day23] 跨站請求偽造 CSRF 一點就通：https://ithelp.ithome.com.tw/articles/10325588

* 深入理解 Cookie 的 Same 属性：https://juejin.cn/post/6963632513914765320#heading-6



## [Day20] 重中之重：Same-origin policy 與 site

### [x] Same-origin policy 的作用及原理

同源策略的主要作用是保护Web应用免受跨站脚本（XSS）和跨站请求伪造（CSRF）等攻击。它通过限制不同源的资源之间的访问权限，确保一个源的脚本不能访问或操作另一个源的数据，从而保护用户数据的安全. . . . . .



### Origin 跟 Site 到底是什么？该怎么区分？

Origin 就是：**scheme + port + host**，三者加起来就是 origin，假设有个 URL 是：`https://huli.tw/abc`，各个组成分别如下所示，而所谓的 Same origin 就是两个 URL 的 origin 要一样！

* `schema`：https
* `port`：443（https 的预设 port）
* `host`：huli.tw

接着我们看一下 site，site 的话要看的东西比 origin 少，只看 **scheme + host**！



### 细究 Same origin

在 HTML 规范中的 [7.5 Origin](https://html.spec.whatwg.org/multipage/origin.html#origin) 章节里面可以看到完整的定义，先来看一下规范里面对 origin 的说明：

```
Origins are the fundamental currency of the web's security model. Two actors in the web platform that share an origin are assumed to trust each other and to have the same authority. Actors with differing origins are considered potentially hostile versus each other, and are isolated from each other to varying degrees.
```

这里写的很清楚：如果两个网站有着相同的 origin，就意味着这两个网站彼此信任，但如果是不同的 origin，就会被隔离开来而且受限制！

接着规范里把 origin 分成两种，一种是 `An opaque origin`，另一种是 `A tuple origin`.



### 细究 Same site

site 的定义也在同一份 spec 里面：

```
A site is an opaque origin or a scheme-and-host.
```

所以说 site 可以是 `opaque origin`，或者是 `scheme-and-host`

在 spec 中可以发现除了 same site 以外，还有另一个名词叫做 `schemelessly same site`，这两个的差别也很明显，`same site`会看 `scheme`，而 `schemelessly same site` 不看 `scheme`.

判断是否为 same site 的步骤：

1. 有 same site 跟 schemelessly same site，较常用的是前者
2. 要比较两个 host 是否为 same site 时，要看 registrable domain
3. 要决定 registrable domain 是什么，要看 public suffix list
4. 两个 host 尽管看起来隶属于同个 parent domain，但因为有 public suffix 的存在，不一定是 same site
5. same site 不看 port，所以 `https://blog.huli.tw:8888` 跟 `http://huli.tw` 是 same site



### Same origin 与 Same site

1. same origin 看 port，same site 不看
2. same origin 看 host，same site 看 registrable domain

示例如下所示：

| A                           | B                           | same origin | same site | 说明                            |
| --------------------------- | --------------------------- | ----------- | --------- | ------------------------------- |
| http://huli.tw:8080         | http://huli.tw              | X           | O         | same site 不看 port             |
| https://blog.huli.tw        | https://huli.tw             | X           | O         | registrable domain 相同         |
| https://alice.github.io     | https://github.io           | X           | X         | github.io 在 public suffix 里面 |
| https://a.alice.github.io   | https://b.alice.github.io   | X           | O         | registrable domain 相同         |
| https://bob.github.io/page1 | https://bob.github.io/about | O           | O         | 不管 path                       |



## [Day21] 跨來源資源共用 CORS 基本介紹

* https://ithelp.ithome.com.tw/articles/10323953

在将同源政策 `same-origin policy` 时，有提到浏览器基本上会阻止一个网站读取另一个不同来源的网站的资料，**可是在开发时，前端跟后端可能不是在同一个 origin，或许一个在 `huli.tw`，另一个在 `api.huli.tw`，那这样前端该怎么读到后端的资料呢？**

答：利用 CORS（Cross-Origin Resource Sharing），其是一种可以跨来源交换网站资料的机制，**这个机制在开发中很常用到**，而对黑客而言，如果 CORS 机制设定错误的话，就变成了一个网站漏洞！



### 为什么不能跨来源呼叫 API？

答：为了安全性！在浏览器上，如果想要拿一个网站的完整内容（可以完整读取），基本上就只能透过 `XMLHttpRequest` 或是 `fetch`，若是这些跨来源的 AJAX 没有限制的话，就可以透过使用者的浏览器，拿到任意网站的内容，包含了各种可能有敏感资讯的网站！



### 跨来源 AJAX 是怎么被挡掉的？

假设 `POST https://lidemy.com/deletePost?id=13` 会删除 id 为 13 的文章（后端没有做任何权限检查），网站前后端的网域不同，而且后端并没有加上 CORS 的 header，即没有配置 CORS，因此用 AJAX 发送该 POST 请求时，会受到**同源政策**的限制！

而实际发送请求后，果然 console 中出现错误信息：

```
request has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource
```

由报错信息可得，浏览器说 `'Access-Control-Allow-Origin' header` 不存在，这表示浏览器已经帮你把 request 发出去，而且拿到 response 了，然后发现其中没有  `'Access-Control-Allow-Origin' header`，所以说**浏览器挡住的不是 request，而是 response！！！**

所以说尽管发送上述 POST 请求后 console 中提示出错，**但是文章有被成功删掉**，只是拿不到 reponse 而已！！！



### 该如何设置 CORS？

设置的方式很简单，既然浏览器为了安全的目的在做保护，只要跟浏览器说：我允许 xxx 存取这个请求的 response 就行啦，示例如下：

```
Access-Control-Allow-Origin: *
```

这个 response header 代表允许任何 origin 读取这个 response，如果想要限制单一来源的话，示例如下：

```
Access-Control-Allow-Origin: https://blog.huli.tw
```

那如果想要多个怎么办？实际上HTTP响应头不允许一个字段有多个值，如果需要支持多个origin，服务器应该动态检查`Origin`请求头，并返回正确的单个`Access-Control-Allow-Origin`值，示例如下：

```python
# Flask 示例
from flask import Flask, request, make_response

app = Flask(__name__)

@app.route('/my-resource')
def my_resource():
    origin = request.headers.get('Origin')
    if origin in ['http://allowed-origin1.com', 'http://allowed-origin2.com']:
        response = make_response('...')
        response.headers['Access-Control-Allow-Origin'] = origin
        return response
    else:
        # 处理不允许的origin
        return 'Not allowed', 403
```

这样，服务器可以根据请求的`Origin`动态设置`Access-Control-Allow-Origin`头，只允许特定的 origin 访问资源。



## [Day23] 跨站請求偽造 CSRF 一點就通

### CSRF 攻击原理

CSRF 攻击的主要目的是：在其它网站底下对目标网站发送请求，让目标网站误以为这个请求是使用者自己发出的，但其实不是！、

要达成这件事的前提是跟**浏览器的机制**有关，**即你只要发送 request 给某个网站，浏览器就会其关联的 cookie 一起带上去**，如果使用者是登入状态，那这个 request 就理所当然包含了他的身份信息，即 Session ID，故这 request 看起来就像是使用者本人发出的！

从 A 网站对 B 网站发 request，会带上 B 的 Cookie，从 C 网站对 B 网站发 request，也会带上 B 的 cookie，这就是 CSRF 之所以可以成立的关键！



### 由 GET 改成 POST 依旧不安全

请求方式由 GET 改成 POST 依旧不安全，一样会有 CSRF 问题，示例如下：写一个看不见的 `iframe`，让 form submit 之后的结果出现在 iframe 里面，而且这个form 还可以自动 submit，即受害者访问链接后立刻中招！

```html
<iframe style="display:none" name="csrf-frame"></iframe>
<form method='POST' action='https://small-min.blog.com/delete' target="csrf-frame" id="csrf-form">
    <input type='hidden' name='id' value='3'>
    <input type='submit' value='submit'>
</form>
<script>document.getElementById("csrf-form").submit()</script>
```



### JSON 请求依旧不安全

以 HTML 的 form 来说，`enctype` 只支援如下三种：

1. `application/x-www-form-urlencoded`（默认，大多数情况下会被使用）
2. `multipart/form-data`（多用于文件上传）
3. `text/plain`

如果服务器想要解析 JSON 数据的话，通常 `content type` 都应该是 `application/json`，所以说服务器拿到数据后会先检查 `content type`，其值如果不是 `application/json`，则认为这不是一个合法的 request，拒之！但是但是但是，如果服务器不检查 `content type`，只检查获取到的数据是否为 JSON 格式，那么就有可能遭受 CSRF 攻击，因为 JSON 格式可由 form 表单拟造出来，示例如下：

```html
<!-- method="post"：表示表单数据将以纯文本的形式编码，即不会进行URL编码 -->
<form action="https://small-min.blog.com/delete" method="post" enctype="text/plain">
    <!-- {"id":3, "ignore_me":"=test"} -->
    <input name='{"id":3, "ignore_me":"' value='test"}' type='hidden'>
    <input type="submit" value="delete!"/>
</form>
```



### 服务器端常见防御手段

#### 检查 Referer 或 Origin header

检查 Request 的 header 中的 `referer` 的值，其代表这个 request 是从那个地方过来的，故可通过检查该值是否为合法的 origin，来判断是否拒绝该 request，但是要注意三点：

1. 有些请求下不会带 referer 或是 origin

2. 有些使用者可能会关闭 referer 功能

3. 判断 referer 的值是否为合法的 origin 的代码必须保证没有 Bug，示例如下：

   ```js
   <!-- 如果攻击者的网址是：small-min.blog.com.attack.com，即可绕过检查 -->
   const referer = request.headers.referer;
   if (referer.indexOf('small-min.blog.com') > -1) {
     // pass
   }
   ```



#### 图像或短信验证码

emmm懂得都懂，尽管这是一个很完善的解决方案，但是会影响到使用者的体验！怎么说呢，总要有人作出妥协吧...



#### CSRF  Token

例如在 form 标签里加上一个隐藏的标签，用于存储 token 值，便于在发送请求时携带 token，这里的 token 是由服务器随机产生，每次一表单等敏感操作都应该产生一个新的 token，并将其返回给发送请求者及存储到服务器端，示例如下：

```html
<form action="https://small-min.blog.com/delete" method="POST">
    <input type="hidden" name="id" value="3"/>
    <input type="hidden" name="csrf_token" value="fj1iro2jro12ijoi1"/>
    <input type="submit" value="刪除文章"/>
</form>
```

客户端提交表单后，服务器端会比对表单中的 `csrf_token` 与自己的 session 里面存的是否一样，是的话则证明这是由自己网站发出的 reqeust，但是但是但是！这依旧不安全！因为**如果站点存在 XSS 漏洞，则黑客可先通过 XSS 漏洞来获取 token**，然后再将 token 写入上述 CSRF Payload 中，进而构成一个完整的 CSRF Payload！



#### [x] Double Submit Cookie

......

#### [x] 純前端的 Double Submit Cookie

......



#### 前后端分离开发

前端与后端完全切开，前端只是一个静态网站，后端则只提供 API，而且前后端的网域通常也会分开，例如前端在 `https://huli.tw`，后端在 `htts://api.huli.tw`，在这种架构下， 比起传统的 `cookie-based` 的身份验证，有更多网站会选择使用 JWT 搭配 HTTP header，把验证身份的 token 存在存在浏览器的 localStorage 里面，向后端发送 request 时放在 `Authorization` header 中，示例如下：

```
GET /me HTTP/1.1
Host: api.huli.tw
Authorization: Bearer {JWT_TOKEN}
```

但是但是但是，其也是不安全的！例如 cookie 可用 `httpOnly` 属性让浏览器读取不到，让攻击者没办法直接偷走 token，**但是 `localStorage` 并没有类似的机制，一旦被 XSS 攻击，攻击者就可以轻松把 token 拿走！**

知识扩展：

```
您提到的 httpOnly 属性确实是一个重要的安全措施，主要用于防止跨站脚本攻击（XSS）中的 cookie 窃取。当一个 cookie 被设置 为httpOnly，它就不能被 JavaScript 脚本访问，这意味着即使一个恶意脚本能够在一个页面上运行（例如，通过 XSS 漏洞），它也无法读取或修改设置了 httpOnly 标志的 cookie。

这样做的好处是显著降低了攻击者通过 JavaScript 脚本直接从浏览器中窃取 cookie 的风险。然而，httpOnly并不能防止所有类型的攻击，例如它不保护 cookie 免受中间人攻击（MITM）或会话固定攻击。为了进一步增强安全性，通常还会结合使用 Secure 属性，这样 cookie 只通过 HTTPS 连接传输，从而防止在非加密连接上被截获。

总之，httpOnly 和 Secure 属性是现代 Web 开发中保护会话安全的重要手段，可以显著增强 cookie 的安全性，但应该与其他安全措施一起使用，以提供全面的防护。
```



#### 自定义 header

当我们在讲 CSRF 攻击的时候，拿来使用的示例是表单跟图片，而这些送出请求的方式不能带上 HTTP header，因此前端在打 API 的时候，可以带上一个 `X-Version: web` 之类的 header 字段，如此一来后端就可以根据接收到的 header 中有没有这个字段，来判断这个请求是不是合法的！

但是黑客可利用 `fetch` 直接发送一个包含此字段的跨站请求，示例如下：

```js
fetch(target, {
  method: 'POST',
  headers: {
    'X-Version': 'web'
  }
})
```

但是但是但是！**带有自定义 header 的请求是非简单请求，因此需要通过 `preflight request` 的检查，才会真正发送出去**，所以，如果你服务器端的 CORS 实现是没有问题的，那这个防御也是没有问题的，反之若有问题，则没办法防御 CSRF 攻击了！

##### CORS 的作用及基本原理

CORS 的作用：CORS（Cross-Origin Resource Sharing，跨源资源共享）是一种机制，它允许 Web 应用从不同的域访问资源。**在浏览器中，由于同源策略（Same-Origin Policy）的存在，一个`域`的网页不能请求另一个`域`的资源，除非服务器通过 CORS 明确地允许**。CORS 提供了一种安全的方式来绕过同源策略，使跨域请求成为可能，注：在 web 应用中，**源通常指协议、域名和端口的组合，如 http://example.com:80**

CORS 的基本原理：**当一个浏览器请求跨域资源时，它会自动发送一个预检请求（preflight request），这是一个 OPTIONS 方法的 HTTP 请求，用来询问服务器是否允许来自特定源的跨域请求。**服务器如果允许，会通过 HTTP 响应头中的 `Access-Control-Allow-Origin` 来指示哪些源是被允许的，还可以通过其他响应头来控制哪些 HTTP 方法、请求头字段是允许的。



#### 简洁总结

总的来说，如果不用 cookie 做身份验证，虽然可以解决 CSRF 的问题，但是却让 XSS 能够偷到 token，增加了 XSS 能够影响的范围，而加上 custom header 虽然看起来可以防御 CSRF，但如果 CORS 设置有问题，那这个防御方式也就失效了！

因此，加上 CSRF token 是比较好而且最普遍的方式，当然你也可以把上面提到的防御手段混在一起使用！



## [Day24] Same-site cookie，CSRF 的救星？

### 初探 same-site cooke

### Same-site cookie 的历史

### GET 类型的 CSRF

### Same-site cookie 的隐藏规则

### 防止 CSRF，真的只要 same-site cookie 就够了吗？

### 简洁总结



## 区分 Same-origin policy、CORS、Same-site cookie

### Same-origin policy

### CORS

### Same-site cookie



2025 / 01 / 17 / 18:23