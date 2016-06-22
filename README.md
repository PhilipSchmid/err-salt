ErrBot plugin for Salt
===

Setup
---
Salt Master must have the salt-api configured and running.
Documentation: http://salt-api.readthedocs.org/en/latest/

Requirements
---
Make sure you have salt-pepper installed or simply use https://hub.docker.com/r/pschmid/docker-errbot-saltslack/.

Installation
---
```
!repos install https://github.com/PhilipSchmid/errbot4salt
```

Configuration
---
```
!plugin config Salt
```
Sample configuration:
```
!plugin config Salt
[  
   {  
      "api_auth":"pam",
      "api_pass":"mypassword",
      "api_url":"https://saltMasterIP:8080",
      "api_user":"myuser",
      "environment":"base",
      "paste_api_url":""
   }
]

```
Debug
---
Test the salt-api reachability with curl (you should get a X-Auth-Token as response):
```
curl -si https://saltMasterIP:8080/login \
        -H "Accept: application/json" \
        -d username='myuser' \
        -d password='mypassword' \
        -d eauth='pam' \
        -k -v
```
To test the salt-pepper connectivity to the salt-api, use the following statement:
```    
err@17782a52fb95:~$ pepper --eauth="pam" --username="myuser" --password="mypassword" -u https://saltMasterIP:8080 --ignore-ssl-errors -H '*' test.ping
{
    "return": [
        {
            "saltmaster01": true
        }
    ]
}
```
If you get something like "Pepper error: Authentication denied". Check your salt-api.conf and master configuration. Examples:
```
myuser@saltmaster01:~$ sudo cat /etc/salt/master.d/salt-api.conf
rest_cherrypy:
  port: 8080
  host: 0.0.0.0
  ssl_crt: /etc/pki/tls/certs/localhost.crt
  ssl_key: /etc/pki/tls/certs/localhost.key
  external_auth:
    pam:
      myuser:
        - .*
```
```
master@saltmaster01:~$ sudo grep -v '^#' /etc/salt/master
..
external_auth:
  pam:
    myuser:
      - test.*
..
```

Usage
---
Simple example usage

```
!salt base * test.ping
!salt base * cmd.run "ps -ef | grep python"
!salt base saltmaster* cmd.run "ip addr"
```
