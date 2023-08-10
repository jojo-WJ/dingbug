import datetime
import requests
import json

# 禅道接口地址
# url = "http://your.zentao.url/api-bug-list"
url = "http://192.168.12.195:82/zentao/api.php/v1"

# 禅道接口参数，按需修改
data = {
    "status": "active",
    "type": "bug",
    "orderBy": "id_desc",
    "limit": 100,
    "offset": 0,
    "recTotal": "yes",
    "assignedTo": "me"
}

loginhost = "http://192.168.12.195:82/zentao/index.php?m=user&f=login"  # 登录url
add_bughost = "http://zen.beta.cn/index.php?m=bug&f=create&productID=10&branch=0&extra=moduleID=0"  # new bug url


# 钉钉机器人webhook地址，按需修改
# dingding_url = "https://oapi.dingtalk.com/robot/send?access_token=your_access_token"
dingding_url = "https://oapi.dingtalk.com/robot/send?access_token=68e55c3021017692953a278bbd65e70b799a37975f80f4b59042e81eb401e9cb"
# 获取当前时间
now = datetime.datetime.now()



# 判断是否为每天下午5点
if now.hour == 9:
    # 发送请求，获取禅道bug列表
    # response = requests.post(url, data=data)

    header = {'Content-Type': "application/x-www-form-urlencoded; charset=utf-8"}  # 设置请求头
    datas = {"account": "admin", "password": "Ssit123456"}  # 定义请求的数据
    s = requests.session()  # 实例化一个session对象
    response = s.post(loginhost, headers=header, data=datas)  # 使用session发起请求


    print(response.content);

    bug_list = json.loads(response.text)["data"]

    # 构造钉钉消息
    message = {
        "msgtype": "text",
        "text": {
            "content": "禅道未处理的bug：\n"
        }
    }
    for bug in bug_list:
        message["text"]["content"] += f"{bug['id']} {bug['title']}\n"

    # 发送钉钉消息
    requests.post(dingding_url, json=message);