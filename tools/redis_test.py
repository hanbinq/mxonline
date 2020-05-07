# @Time : 2020/5/4 21:35 
# @Author : jing.liang
# @description :
import redis


r = redis.Redis(host='127.0.0.1', port=6379, db=0, charset="utf8", decode_responses=True)

r.set("mobile1", "123")
r.expire("mobile", 1)
print(r.get("mobile"))

