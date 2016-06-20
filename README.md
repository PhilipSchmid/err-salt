Err plugin for Salt
===

Setup
---
Salt Master must have the salt-api configured and running.
Documentation: http://salt-api.readthedocs.org/en/latest/

Requirements
---
You must install salt-pepper where errbot can load it before activating the Salt plugin.
```
pip install salt-pepper
```

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

Usage
---
Simple example usage

```
!salt * test.ping
!salt app* cmd.run "ps -ef  | grep python"
```
