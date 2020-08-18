## Overview

- `static` - default webpage for server

## Install Dependencies

```bash
sudo python3 -m pip install -r requirements.txt --use-feature=2020-resolver
```

## Run Server

```bash
sudo python3 server.py <configuration file path>
```

Replace `<configuration file path>` with yours, then open `https(or http)://localhost:<port>` in browser to test.

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
    "Listen": "",
    "Port": (int),
    "Cert_Path": "",
    "Key_Path": "",
    "Debug": (bool)
}
```

For further information, please view `../docs`.
