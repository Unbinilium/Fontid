## Overview

- `app.py` - docker command exec handler source

- `build.sh` - build docker image

## Docker Image

![Fontid Action](https://github.com/Unbinilium/Fontid/workflows/Fontid%20Action/badge.svg?branch=master&event=push)

```bash
sudo docker pull unbinilium/font-identifier-rest-api:latest
```

## Build Image

```bash
sudo bash build.sh
```

## Run Image

```bash
sudo docker run -p <host listen port>:8080 -v <host data volume>:/data font-identifier-rest-api
```

Replace `<host listen port>` and `<host data volume>` with yours, then open `https(or http)://localhost:<port>` in browser to test.

## Configuration

```json
{
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
```

For further information, please view `../docs`.
