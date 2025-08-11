import requests
from datetime import date
import datetime,os, json

def ImportPersonalInfo(Customer='', SAPNum='', GroupNum='', Status='', DepartmentCode=''):
    url = r'http://127.0.0.1:8002/PersonalInfo/api_Per/login/'
    url2 = r'http://127.0.0.1:8002/PersonalInfo/Perapi/?'
    # url = r'http://192.168.1.9:8002/PersonalInfo/api_Per/login/'
    # url2 = r'http://192.168.1.9:8002/PersonalInfo/Perapi/?'
    requests.adapters.DEFAULT_RETRIES = 1
    # s = requests.session()
    # s.keep_alive = False  # 关闭多余连接
    # getTestSpec=requests.get(url)
    # headers = {'Connection': 'close'}
    try:
        headers = \
            {
                "Content-Type": "application/json;charset=UTF-8"
            }
        body = \
            {
                "username": "API_CQM", "password": "Qs!3m6Tc7"
            }
        r = requests.post(url, headers=headers, data=json.dumps(body))
    except:
        # time.sleep(0.1)
        print("Can't connect to DDIS Sercer or get token failed")
        return 0
    # print(json.loads(r.text)["token"])
    if json.loads(r.text)["token"]:
        Auth_token = "Bearer " + json.loads(r.text)["token"]
        try:
            # GroupNum = "C1010S3"
            headers = \
                {
                    "Authorization": Auth_token
                }
            content = \
                {
                    "Customer": Customer,
                    "SAPNum": SAPNum,
                    "GroupNum": GroupNum,
                    "Status": Status,
                    "DepartmentCode": DepartmentCode,
                }
            getTestSpec = requests.get(url2, headers=headers, params=content)
        except:
            # time.sleep(0.1)
            print("Got nothing, try request agian")
            return 0
        return getTestSpec.json()

def ImportDeviceInfo(Customer='', NID='', BR_per_code='', BrwStatus='', DevStatus=''):
    # url = r'http://192.168.1.9:8004/DeviceLNV/api/login/'
    # url2 = r'http://192.168.1.9:8004/DeviceLNV/DeviceLNV_api/?'
    url = r'http://127.0.0.1:8003/DeviceLNV/api/login/'
    url2 = r'http://127.0.0.1:8003/DeviceLNV/DeviceLNV_api/?'
    requests.adapters.DEFAULT_RETRIES = 1
    try:
        headers = \
            {
                "Content-Type": "application/json;charset=UTF-8"
            }
        body = \
            {
                "username": "API_DMS", "password": "dX6c9T0i"
            }
        r = requests.post(url, headers=headers, data=json.dumps(body))
    except Exception as e:
        # time.sleep(0.1)
        print(str(e))
        return 0
    # print(json.loads(r.text)["token"])
    if json.loads(r.text)["token"]:
        Auth_token = "Bearer " + json.loads(r.text)["token"]
        try:
            # GroupNum = "C1010S3"
            headers = \
                {
                    "Authorization": Auth_token
                }
            content = \
                {
                    "Customer": Customer,
                    "NID": NID,
                    "BR_per_code": BR_per_code,
                    "BrwStatus": BrwStatus,
                    "DevStatus": DevStatus,
                }
            getTestSpec = requests.get(url2, headers=headers, params=content)
        except:
            print("Got nothing, try request agian")
            return 0
        return getTestSpec.json()

Devicelist = ImportDeviceInfo(BrwStatus='已借出')
Num = 7 #超过多少天提醒
today = date.today()
devicelist = [dict(item, OverDay=(today - date.fromisoformat(item["Plandate"])).days)
          for item in Devicelist
          if (today - date.fromisoformat(item["Plandate"])).days >= Num]
# print(result)
Pers_list = ImportPersonalInfo(Customer='')
group_info_map = {
    p['GroupNum']: (p['DepartmentCode'], p['EngName'])
    for p in Pers_list if p.get('GroupNum')
}


# 为每个设备添加Department字段
for device in devicelist:
    device['Department'] = group_dept_map.get(device.get('Usrname', ''), '')
    group_key = device.get('Usrname', '')

    # 获取部门代码和英文名
    dept_code, eng_name = group_info_map.get(group_key, ('', ''))

    # 添加部门字段
    device['Department'] = dept_code

    # 添加邮箱字段（如果英文名存在）
    if eng_name:
        # 清理英文名中的特殊字符和空格
        clean_name = ''.join(e for e in eng_name if e.isalnum() or e in ['.', '_'])
        device['MailAddress'] = f"{clean_name}@compal.com"
    else:
        device['MailAddress'] = ''