# @Time : 2020/5/3 13:06 
# @Author : jing.liang
# @description :
import requests
import json


def send_single_sms(apikey, code, mobile):
    # 发送单条短信
    url = "https://sms.yunpian.com/v2/sms/single_send.json"
    text = "您的短信验证码是{}。".format(code)

    res = requests.post(url, data={
        "apikey": apikey,
        "mobile": mobile,
        text: text
    })
    res_json = json.loads(res.text)
    return res_json


