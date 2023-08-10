import datetime
import string

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

# 获取所有执行列表数据

# 1.获取项目
projects_list_url = api_url + "/projects"
# bug_list = response.json()['data']
# 发送GET请求
response = requests.get(projects_list_url, headers=header, params=body1)

# 解析网络数据
projects_list = json.loads(response.text)["projects"]

# 获取项目执行
executions_list_url = api_url + "/projects/{}/executions"

# 获取项目执行的任务列表
executions_task_list_url = api_url + "/executions/{}/tasks"


def get_executions(project_id):
    # 获取项目id对应的执行列表
    executions_response = requests.get(executions_list_url.format(project_id), headers=header, params=body1)
    # 解析项目执行网络数据
    # projects_executions_list = json.loads(executions_response.text)["executions"]
    return json.loads(executions_response.text)


def get_executions_task(execute_id):
    task_response = requests.get(executions_task_list_url.format(execute_id), headers=header, params=body1)
    # 解析项目执行网络数据
    # executions_task_list = json.loads(task_response.text)["tasks"]
    return json.loads(task_response.text)

'''
for project in projects_list:
    executions = get_executions(project["id"])
    if len(executions["executions"]) > 0:
        for execution in executions["executions"]:
            print(execution['name'] + "count:" + f"{len(executions['executions'])}")
            execution_task = get_executions_task(execution['id'])
            if len(execution_task["tasks"]) > 0:
                for task in execution_task["tasks"]:
                    print(f"{task['name']} count: {len(execution_task['tasks'])}")

'''


# 获取当前时间
now = datetime.datetime.now()

message_content = ''

for project in projects_list:
    executions = get_executions(project["id"])
    if len(executions["executions"]) > 0:
        for execution in executions["executions"]:
            print(execution['name'] + "count:" + f"{len(executions['executions'])}")
            execution_task = get_executions_task(execution['id'])
            message_content += f"> {execution['name']}-待处理的任务数量-{len(execution_task['tasks'])}\n\n"
            tasks_list = execution_task["tasks"]
            if len(tasks_list) > 0:
                tasks_list.sort(key=lambda x: x['assignedTo']['realname'], reverse=True)  # 降序排列
                for task in tasks_list:
                    # print(f"{task['name']} count: {len(execution_task['tasks'])}")
                    if task['status'] != 'done' and datetime.datetime.strptime(task['deadline'],'%Y-%m-%d').day < now.day:
                        message_content += f"{task['id']}.{task['name']} {task['assignedTo']['realname']} 截至日期：{task['deadline']} <font color='#dd0000'>已延期</font><br />  \n\n"
                    elif task['status'] == 'done':
                        message_content += f"{task['id']}.{task['name']} {task['assignedTo']['realname']} 截至日期：{task['deadline']} <font color='#00dd00'>已完成</font><br /> \n\n"
                    elif task['status'] == 'wait':
                        message_content += f"{task['id']}. {task['name']} {task['assignedTo']['realname']} 截至日期：{task['deadline']} <font color='#666600'>未开始</font><br /> \n\n"
                    elif task['status'] == 'doing':
                        message_content += f"{task['id']}.{task['name']} {task['assignedTo']['realname']} 截至日期：{task['deadline']} <font color='#00dddd'>进行中</font><br /> \n\n"
                    else:
                        message_content += f"{task['id']}.{task['name']} {task['assignedTo']['realname']} 截至日期：{task['deadline']} <font color='#dd00dd'>未知</font><br /> \n\n"

message = {
    "msgtype": "markdown",
    "markdown": {
        "title": "禅道任务报告-ssit",
        "text": f"#### 禅道任务报告 \n {message_content}\n >\n > \n----------------\n###### {now} [禅道主页](http://192.168.12.195:82/zentao/) \n"
    },
    "at": {
        "atMobiles": [],
        "atUserIds": [],
        "isAtAll": "true"
    }
}

message2 = {
    "msgtype": "text",
    "text": {
        "content": f"#### 禅道任务报告 \n > {message_content}\n >\n > ###### {now} [禅道主页](http://192.168.12.195:82/zentao/)-ssit \n"
    }
}


# ![screenshot](https://img.alicdn.com/tfs/TB1NwmBEL9TBuNjy1zbXXXpepXa-2400-1218.png)

# 发送钉钉消息
dingding_url = "https://oapi.dingtalk.com/robot/send?access_token=68e55c3021017692953a278bbd65e70b799a37975f80f4b59042e81eb401e9cb"
requests.post(dingding_url, json=message)

'''

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


print(message["text"]["content"])

# 发送钉钉消息
dingding_url = "https://oapi.dingtalk.com/robot/send?access_token=68e55c3021017692953a278bbd65e70b799a37975f80f4b59042e81eb401e9cb"
requests.post(dingding_url, json=message)
'''
