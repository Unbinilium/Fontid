## Build Image

```bash
sudo bash font-identifier/docker/build.sh
```

## Run Image

```bash
sudo docker run -p <host listen port>:8080 -v <host data volume>:/data font-identifier-rest-api
```

Replace `<host listen port>` and `<host data volume>` with yours.

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
    "Model_Path": "models/keras.h5",
    "Label_Path": "models/labels.json",
    "Auth_List_Path": "auth/allowed.json",
    "Allowed_Extensions_List": "['.png', '.jpg', '.jpeg', '.gif']",
    "Cert_Path": "ssl/selfsigned-cert.crt",
    "Key_Path": "ssl/selfsigned-key.key",
    "Debug": true
}
```

For further information, please view `../docs`.
