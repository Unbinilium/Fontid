## Configurations

### Identical

- Used for aliyun OSS and OCR auth.

```json
"Access_Key_ID": "",
"Access_Key_Secret": "",
```

- Set OSS endpoint(*https*) and bucket name used for upload identity required images, auto remove uploaded images from OSS after OCR finished.

```json
"OSS_Endpoint": "",
"OSS_Bucket_Name": "",
```

- Set OCR datacenter location, the minimum heigh scale to the image height which smaller the OCR will ignore to recognize, and discard the OCR result which text boxes probability is less than minimum probability.

```json
"OCR_Location": "",
"Min_Height_Scale": (float),
"Min_Probability": (float),
```

- Model path and label path, label path would contain a json file that stored all the font names matched the generated model, dict stored in json format. See `font-identifier.ipynb` to train a model with labels.

```json
"Model_Path": "",
"Label_Path": "",
```

- For API auth, close the connection if it not in the json, dict stored in json format.

```json
"Auth_List_Path": "",
```
 
- Allow image extensions for upload, dict stored.
 
```json
"Allowed_Extensions_List": "",
```

- Upload limit for single image(MB).

```json
"Upload_Limit": (int),
```

- Config SSL, leave them blank or one of them is blank to disable SSL.

```json
"Cert_Path": "",
"Key_Path": "",
```

- Debug

```json
"Debug": (bool),
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
"Listen": "",
"Port": (int),
```

- All the `*_Path` should be the absolute path or relative path to the host machine.

## Misc

The *blur kernel size* and *predict image size* is uncustomizable in `config.json`.
