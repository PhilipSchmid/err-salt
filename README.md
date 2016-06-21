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
!repos install https://github.com/PhilipSchmid/err-salt
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
      "api_url":"saltMasterIP:8080",
      "api_user":"myuser",
      "environment":"base",
      "paste_api_url":""
   }
]

```

Usage
---
Simple example usage

```
!salt * test.ping
!salt app* cmd.run "ps -ef  | grep python"
```
