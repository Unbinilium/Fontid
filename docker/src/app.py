#Basic Requirement
import os
import sys
import json

#Usage
usage = '''
Usage: docker run -p <host listen port>:8080 -v <host data volume>:/data font-identifier-rest-api

Note: A config file named 'config.json' in <host data volume> is required.

Example config.json -> {
    "Access_Key_ID": "LTAI4GGHnoZxjeprgmeiWdde",
    "Access_Key_Secret": "uDRC7ld9qiWXWQraWtqE9bFAC5Wfn8",
    "OSS_Endpoint": "https://oss-cn-shanghai.aliyuncs.com",
    "OSS_Bucket_Name": "unbinilium",
    "OCR_Location": "cn-shanghai",
    "Min_Height_Scale": 0.05,
    "Min_Probability": 0.3,
    "Model_Path": "models/keras.h5",
    "Label_Path": "models/labels.json",
    "Auth_List_Path": "auth/allowed.json",
    "Allowed_Extensions_List": "['.png', '.jpg', '.jpeg', '.gif']",
    "Cert_Path": "ssl/selfsigned-cert.crt",
    "Key_Path": "ssl/selfsigned-key.key",
    "Debug": true
}

Assume <host data volume> is the current root directory, all the '*_Path' value in the config.json would be which the absolute path that removed <host data volume> path. 
'''

#Conf loader
try:
    conf = json.load(open('/data/config.json', encoding = 'utf-8'))

except Exception as error:
    print('Cannot open config file \'config.json\' in <host data volume>\n')
    print(usage)
    sys.exit()

#Check if file exist
for key in conf:
    if '_Path' in key:
        conf[key] = '/data/' + conf[key]

        if not os.path.isfile(conf[key]):

            #Bypass ssl path check
            if not key in list(['Cert_Path', 'Key_Path']):
                print('Cannot found file -> \'' + conf[key][len('/data/'):] + '\' in <host data volume>')
                print(usage)
                sys.exit()

#Set listen host and port
conf.update({"Listen": '0.0.0.0', "Port": 8080})

#Save config.json for server.py
with open('/app/config.json', 'w') as outfile:
    json.dump(conf, outfile)

#Exec server.py
command = 'python \'/app/server.py\' \'/app/config.json\''
os.system(command)
