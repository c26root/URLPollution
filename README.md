# UrlPollution

>对URL进行Payload污染 然后发送请求进行FUZZ测试 通过 dnslog ceye.io 等DNS请求记录平台辅助测试

* 命令执行
* 命令注入
* 模板注入

```
all_qs=True 一次污染所有url
append=True 追加payload
```

```
payloads = ['phpinfo();', 'echo 1;']
qs = 'a=1&b=2'
p = Pollution(payloads)
print p.payload_generator(qs)
```

```
['a=1phpinfo%28%29%3B&b=2', 'a=1&b=2phpinfo%28%29%3B', 'a=1echo+1%3B&b=2', 'a=1&b=2echo+1%3B']
```
