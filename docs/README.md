## Configurations

### Identical

- Used for aliyun OSS and OCR auth.

```json
"Access_Key_ID": "LTAI4GGHnoZxjeprgmeiWdde",
"Access_Key_Secret": "uDRC7ld9qiWXWQraWtqE9bFAC5Wfn8",
```

- Set OSS endpoint(*https*) and bucket name used for upload identity required images, auto remove uploaded images from OSS after OCR finished.

```json
"OSS_Endpoint": "https://oss-cn-shanghai.aliyuncs.com",
"OSS_Bucket_Name": "unbinilium",
```

- Set OCR datacenter location, the minimum heigh scale to the image height which smaller the OCR will ignore to recognize, and discard the OCR result which text boxes probability is less than minimum probability.

```json
"OCR_Location": "cn-shanghai",
"Min_Height_Scale": 0.05,
"Min_Probability": 0.3,
```

- Model path and label path, `labels.json` stored all the font names matched the generated model, dict stored in json format. See `font-identifier.ipynb` to train a model with labels.

```json
"Model_Path": "keras.h5",
"Label_Path": "labels.json",
```

- For API auth, close the connection if it not in the json, dict stored in json format. See `../src/auth` for example.

```json
"Auth_List_Path": "auth/allowed.json",
```
 
- Allow image extensions for upload. 
 
```json
"Allowed_Extensions_List": "['.png', '.jpg', '.jpeg', '.gif']",
```

- Config SSL, leave them blank or one of them is blank to disable SSL.

```json
"Cert_Path": "selfsigned-cert.crt",
"Key_Path": "selfsigned-key.key",
```

- Debug

```json
"Debug": true,
```

### Docker

- Config file can only named `config.json`, stored in the root of `<host data volume>/`.

- All the `*_Path` is which the absolute path on the host that `<host data volume>` removed.

```
#Absolute path on the host
<host data volume>/foo/bar

#Path in config.json
foo/bar
```

### Python

- Customizable listen host and port.

```json
"Listen": "localhost",
"Port": 443,
```

- All the `*_Path` should be the absolute path or relative path to the host machine.

## Misc

The *blur kernel* size, *predict image size* and *API upload limit* is uncustomizable in `config.json`.
