#Basic Requirement
import os
import sys
import json

#Usage
usage = '''
Usage: sudo docker run -p <host listen port>:8080 -v <host data volume>:/data font-identifier-rest-api

Note: A config file named 'config.json' in <host data volume> is required.

Example config.json -> {
    "Access_Key_ID": "",
    "Access_Key_Secret": "",
    "OSS_Endpoint": "",
    "OSS_Bucket_Name": "",
    "OCR_Location": "",
    "Min_Height_Scale": (float),
    "Min_Probability": (float),
    "Model_Path": "",
    "Label_Path": "",
    "Auth_List_Path": "",
    "Allowed_Extensions_List": "",
    "Upload_Limit": (int),
    "Cert_Path": "",
    "Key_Path": "",
    "Debug": (bool)
}

Assume <host data volume> is the current root directory, all the '*_Path' value in the config.json would be which the absolute path that removed <host data volume> path. 
'''

#Conf loader
try:
    conf = json.load(open('/data/config.json', encoding = 'utf-8'))

except Exception as error:
    print('Cannot open config file \'/data/config.json\' in <docker data volume>\n')
    print(usage)

    sys.exit()

#Check if file exist
for key in conf:
    if '_Path' in key:
        #Bypass ssl path check
        if (not key in list(['Cert_Path', 'Key_Path'])) or ((key in list(['Cert_Path', 'Key_Path'])) and conf[key]):
            conf.update({key: os.path.join('/data/', conf[key])})

            #Check if file exist
            if not os.path.isfile(conf[key]):
                print('Cannot found file -> \'' + conf[key] + '\' in <docker data volume>')
                print(usage)

                sys.exit()

#Set listen host and port
conf.update({"Listen": "0.0.0.0", "Port": 8080})

#Save config.json for server.py
with open('/src/config.json', 'w') as outfile:
    json.dump(conf, outfile)

#Exec server.py
command = 'python \'/src/server.py\' \'/src/config.json\''
os.system(command)
