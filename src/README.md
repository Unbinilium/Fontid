## Install Dependencies

```bash
sudo python3 -m pip install -r font-identifier/src/requirements.txt --use-feature=2020-resolver
```

## Run Server

```bash
sudo pyrhon3 font-identifier/src/server.py <configuration file path>
```
Replace <configuration file path> with yours.

## Configuration

```json
{
    "Access_Key_ID": "LTAI4GGHnoZxjeprgmeiWdde",
    "Access_Key_Secret": "uDRC7ld9qiWXWQraWtqE9bFAC5Wfn8",
    "OSS_Endpoint": "https://oss-cn-shanghai.aliyuncs.com",
    "OSS_Bucket_Name": "unbinilium",
    "OCR_Location": "cn-shanghai",
    "Min_Height_Scale": 0.05,
    "Min_Probability": 0.3,
    "Model_Path": "../models/keras.h5",
    "Label_Path": "../models/labels.json",
    "Auth_List_Path": "auth/allowed.json",
    "Allowed_Extensions_List": "['.png', '.jpg', '.jpeg', '.gif']",
    "Listen": "localhost",
    "Port": 443,
    "Cert_Path": "ssl/selfsigned-cert.crt",
    "Key_Path": "ssl/selfsigned-key.key",
    "Debug": true
}
```

For further information, please view `../docs`.
