# black_hat_python_tutorial

### Prepare

```shell-session
$ python -m venv ./venv

$ # activate venv
$ souce ./venv/activate.fish
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

### Secure Connection Via SSH With Paramiko

```shell-session
$ pip install paramiko
$ # or
$ pip install -r ./requirements.txt
```
