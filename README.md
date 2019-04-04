# black_hat_python_tutorial

### Prepare

```shell-session
$ python -m venv ./venv
```

### netcap

##### terminal 1 as server

```shell-session
$ python bh_netcap.py -l -c -p 9999
```

##### terminal 2 as client

```shell-session
$ python bh_netcap.py -t localhost -p 9999
$ # then: ctrl + D
$ # then: enter commands like `echo "something"`, `pwd`, `echo -ne "GET / HTTP/1.1\r\nHost: www.google.com\r\n\r\n" | python bh_netcat.py -t www.google.com -p 80`
```
