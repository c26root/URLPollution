# UrlPollution

> 对URL或者参数进行Payload污染 然后发送请求进行FUZZ测试 通过 dnslog ceye.io 等DNS请求记录平台辅助测试

### 用途
* 命令执行
* 命令注入
* 模板注入


```
payloads = ['phpinfo();', 'echo 1;']
url = 'http://baidu.com/?a=1&b=2'
p = Pollution(payloads)
print p.payload_generator(url)

['http://baidu.com/?a=1phpinfo%28%29%3B&b=2', 'http://baidu.com/?a=1&b=2phpinfo%28%29%3B', 'http://baidu.com/?a=1echo+1%3B&b=2', 'http://baidu.com/?a=1&b=2echo+1%3B']
```


### 参数说明
```
payload_generator(self, query, all_qs=False, append=True)

all_qs=True 一次污染所有url
append=True 追加payload


payloads = ['phpinfo();', 'echo 1;']
qs = 'a=1&b=2'
p = Pollution(payloads)
print p.payload_generator(qs, all_qs=True)

['a=1phpinfo%28%29%3B&b=2phpinfo%28%29%3B', 'a=1echo+1%3B&b=2echo+1%3B']


payloads = ['phpinfo();', 'echo 1;']
qs = 'a=1&b=2'
p = Pollution(payloads)
print p.payload_generator(qs, all_qs=True, append=False)

['a=phpinfo%28%29%3B&b=phpinfo%28%29%3B', 'a=echo+1%3B&b=echo+1%3B']

```
