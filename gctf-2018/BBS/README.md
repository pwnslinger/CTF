# BBS

## Description

During the last Google CTF we have encountered a bunch of client-side web challegens which the highest point one was BBS. Actually I was not fortunate to take time to play during the game but after that I found sometime to work on especially on this challenge. after entering the challenge page, you'll notice that it's similar to an issue tracker portal which you can report messages and stuff to admin and he/she will click on that. On main page you can register a new account and login to your portal. there're some capabilities like updating your profile photo, and writing stuff and report. 

## Vulnerability

After logging in, on the main page, specify title and content of post and then send it. Under `assets/app.js` there's a report functionality which sends out the post to admin. 

```javascript
function report(id) {
    $.post('/report', {
            'post': '/admin/' + id
                
            }).then(() => alert('Reported!'));

}
```

so, when you report the post, you can catch it as a POST request which the post parameter contains a path to a `/admin/$id`. by visiting that url we can see there's a message for admin at `/post` which sends another ajax request to the following address, including a page title says `Under Construction!`. 

```javascript
function load_post() {
    var q = qs.parse(location.search, {ignoreQueryPrefix: true});
        var url = q.p;

        $.ajax(url).then((text) => {
                $('#post').html(atob(text));
                    
                });

}
``` 

`load_post` will parses the query string and passes the `$_GET['p']` parameter directly to ajax()!. One example of URL is as the following: 
`https://bbs.web.ctfcompetition.com/post?p=/ajax/post/2147483647` 

when we go to that link, we see the content in base64 format and it contains `Private content!`. But there's a functionality in app.js at `linkify()` which inserts an iframe element on the `mouseover` event that fetches the content of post id in decoded format on the page. 

if we send a simple payload like `<img src=x onerror=alert(1);>`, base64 decoded one contains html_encoded tags but the one prints out on the page after quoting and linkify is the escaped one! 


