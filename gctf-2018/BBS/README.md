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

so, when you report the post, you can catch it as a POST request which the post parameter contains a path to a `/admin/$id`. 


