import datetime
import requests
import json

api_url = "http://192.168.12.195:82/zentao/api.php/v1"
api_access_key = "efb16b298924b2492bcc1e6b73cd69f6"

# + 'bug'
# headers = {'Content-Type': 'application/json', 'Auth-Token': api_access_key}
body = {"account": "admin", "password": "Ssit123456"}

url = api_url + "/tokens"
# 发送GET请求
response = requests.post(url, json=body)
token = (response.json())['token']
header = {"Token": token}
body1 = {"limit": 2000}
print("token::" + token)

# 获取Bug列表数据
bug_list_url = api_url + "/products/2/bugs"
# bug_list = response.json()['data']

# 发送GET请求
response = requests.get(bug_list_url, headers=header, params=body1)

bug_list = json.loads(response.text)["bugs"]

# 获取当前时间
now = datetime.datetime.now()

# 构造钉钉消息
message = {
    "msgtype": "text",
    "text": {
        "content": f"{now} 禅道未处理的bug：\n"
    }
}

# bug_list_active = bug_list
bug_list.sort(key=lambda x: x['assignedTo']['realname'], reverse=True)  # 降序排列


num = 0
for bug in bug_list:
    if bug['statusName'] == '激活':
        num = num + 1
        message["text"][
            "content"] += f"{bug['id']} {bug['title']} {bug['statusName']} {bug['assignedTo']['realname']}\n"

message["text"]["content"] += f"激活总数：{num}\n\n"

print(message["text"]["content"])

message["text"]["content"] += f"{now} 已解决问题\n"
num_resolved = 0

for bug in bug_list:
    if bug['statusName'] == '已解决' and datetime.datetime.strptime(bug['resolvedDate'],'%Y-%m-%dt%H:%M:%SZ').day == now.day:
        num_resolved += 1
        message["text"]["content"] += f"{bug['id']} {bug['title']} {bug['statusName']} {bug['resolvedBy']['realname']}\n"

message["text"]["content"] += f"已解决问题总数：{num_resolved}\n"

'''
message["text"]["content"] += f"{now} 已关闭问题\n"
num_closed = 0

for bug in bug_list:
    if bug['statusName'] == '已关闭' and datetime.datetime.strptime(bug['resolvedDate'], '%Y-%m-%dt%H:%M:%SZ').day == now.day:
        num_closed += 1
        message["text"]["content"] += f"{bug['id']} {bug['title']} {bug['statusName']} {bug['resolvedBy']['realname']}\n"

message["text"]["content"] += f"已关闭问题总数：{num_closed}\n"
'''

print(message["text"]["content"])

# 发送钉钉消息
dingding_url = "https://oapi.dingtalk.com/robot/send?access_token=68e55c3021017692953a278bbd65e70b799a37975f80f4b59042e81eb401e9cb"
requests.post(dingding_url, json=message)
