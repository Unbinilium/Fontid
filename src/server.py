#Basic Requirement
import os
import sys
import json

#Usage
usage = 'Usage: python3 ' + sys.argv[0] + ' <configuration file path>'

#Conf Loader
if len(sys.argv) < 2:
    print(usage)
    sys.exit()

else:
    conf = json.load(open(sys.argv[1], encoding = 'utf-8'))

    #Access_key
    access_key_id = conf['Access_Key_ID']
    access_key_secret = conf['Access_Key_Secret']

    #OSS
    endpoint = conf['OSS_Endpoint']
    bucket_name = conf['OSS_Bucket_Name']

    #OCR
    location = conf['OCR_Location']
    min_height_scale = conf['Min_Height_Scale']
    min_probability = conf['Min_Probability']

    #Model
    model_path = conf['Model_Path']
    font_names = json.load(open(os.path.abspath(conf['Label_Path']), encoding = 'utf-8'))

    #Flask Config
    AUTH = json.load(open(os.path.abspath(conf['Auth_List_Path']), encoding = 'utf-8'))
    ALLOWED_EXTENSIONS = json.loads(str(conf['Allowed_Extensions_List']).replace('\'', '"'))
    UPLOAD_LIMIT = conf['Upload_Limit']
    LISTEN = conf['Listen']
    PORT = conf['Port']
    DEBUG = conf['Debug']

    #If Cert and Key are not provided, disable SSL
    c, k = conf['Cert_Path'], conf['Key_Path']
    if c and k:
        APP_SSL = True
        CERT_PATH = os.path.abspath(c)
        KEY_PATH = os.path.abspath(k)

    else:
        APP_SSL = False

#Additional Requirement
import uuid
import math
import time
import codecs
import hashlib
import flask
import PIL
import numpy as np
from matplotlib import cm as cm
from matplotlib import pyplot as plt
from keras.models import load_model
from keras.preprocessing.image import img_to_array

#Aliyun SDK Core
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException

#Aliyun SDK OSS
import oss2

#Aliyun SDK OCR
from aliyunsdkocr.request.v20191230.RecognizeCharacterRequest import RecognizeCharacterRequest

#Dir Path of server.py
PATH = os.path.dirname(os.path.abspath(__file__))

#OSS config
oss_auth = oss2.Auth(access_key_id, access_key_secret)
bucket = oss2.Bucket(oss_auth, endpoint, bucket_name)

#OCR config
client = AcsClient(access_key_id, access_key_secret, location)

#Preload Model
model = load_model(model_path)

def rotate(x, y, o_x, o_y, theta):
    x_r = math.cos(theta) * (x - o_x) - math.sin(theta) * (y - o_y) + o_x
    y_r = math.sin(theta) * (x - o_x) + math.cos(theta) * (y - o_y) + o_y
    return [x_r, y_r]

def rev_conv_label(label):
    return font_names[label]

def blur_image(img):
    blur_img = img.filter(PIL.ImageFilter.GaussianBlur(radius = 3))
    blur_img = blur_img.resize((105, 105))
    return blur_img

def font_identifier(image_path):
    #OCR request
    request = RecognizeCharacterRequest()
    request.set_accept_format('json')

    #Upload with SHA1 hashed name, set image to private
    file_extension = os.path.splitext(image_path)[1]
    key = hashlib.sha1(open(image_path, 'rb').read()).hexdigest() + file_extension
    bucket.put_object_from_file(key, image_path)
    bucket.put_object_acl(key, oss2.OBJECT_ACL_PRIVATE)

    #Get image info from OSS
    info = bucket.get_object(key, process = 'image/info')
    info_content = info.read()
    decoded_info = json.loads(oss2.to_unicode(info_content))

    print('Image Info ->')
    print(json.dumps(decoded_info, indent = 4, sort_keys = True))

    #Struct image URL
    image_url = bucket.sign_url('GET', key, 60)

    print('Image URL -> ' + image_url)

    #Set OCR image_url
    request.set_ImageURL(image_url)

    #Pre-config request
    min_height = int(decoded_info['ImageHeight']['value']) * float(min_height_scale)
    request.set_MinHeight(int(min_height))
    request.set_OutputProbability(True)

    #Send request to OCR server and get response
    try:
        response = client.do_action_with_exception(request)

    except Exception as error:
        print('Error -> ', error)

        #Delete OSS image
        bucket.delete_object(key)

        #Raise Exception to outsider try/except
        raise Exception(error)

    #Delete OSS image
    bucket.delete_object(key)

    #Parse json response
    parsed = json.loads(response)

    print('Response ->')
    print(json.dumps(parsed, indent = 4, sort_keys = True))

    objects = []
    distances = []
    objects_unfiltered = parsed['Data']['Results']

    #Filter probability by min_probability
    for object_unfiltered in objects_unfiltered:
        if float(object_unfiltered['Probability']) > float(min_probability):
            objects.append(object_unfiltered)

    #Cal image center O(o_x0, o_y0)
    o_x0, o_y0 = int(decoded_info['ImageWidth']['value']) / 2.0, int(decoded_info['ImageHeight']['value']) / 2.0

    for object in objects:

        #Cal TextRectangle angle A, start point A(x0, y0) and endpoint B(x1, y1)
        A = object['TextRectangles']['Angle'] / 180.0
        x0, y0 = object['TextRectangles']['Left'], object['TextRectangles']['Top']
        x1, y1 = x0 + object['TextRectangles']['Width'], y0 + object['TextRectangles']['Height']

        #Cal vector AB = (v_x0, v_y0)
        v_x0, v_y0 = x1 - x0, y1 - y0

        #Cal angle A rotated and 1/2 lenthed vector AB' = (v_x1, v_y1)
        v_x1, v_y1 = (v_x0 * math.cos(A) - v_y0 * math.sin(A)) / 2.0, (v_y0 * math.cos(A) + v_x0 * math.sin(A)) / 2.0

        #Cal TextRectangle center point B'(x2, y2)
        x2, y2 = x0 + v_x1, y0 + v_y1

        print('TextRectangleCtr -> ', (x2, y2))

        #Cal distance between point B and O
        d = math.pow(x2 - o_x0, 2) + math.pow(y2 - o_y0, 2)
        distances.append(d)

    index_min = distances.index(min(distances))

    print('Min_Index -> ', index_min)

    A = - objects[index_min]['TextRectangles']['Angle'] / 180.0

    roi = PIL.Image.open(image_path)
    roi = roi.rotate(A)

    #Cal start point A(x0, y0)
    x0, y0 = objects[index_min]['TextRectangles']['Left'], objects[index_min]['TextRectangles']['Top']

    #Cal angle A rotated A'(x1, y1)
    x1, y1 = rotate(x0, y0, o_x0, o_y0, A)

    #Crop text ROI
    roi = roi.crop((x1, y1, (x1 + objects[index_min]['TextRectangles']['Width']), (y1 + objects[index_min]['TextRectangles']['Height'])))

    #Load image and de-noisy
    tmp_img = roi.copy().convert('L')
    tmp_img = blur_image(tmp_img)
    arr_img = img_to_array(tmp_img)

    #Predict using trained model
    data = []
    data.append(arr_img)
    data = np.asarray(data, dtype = "float") / 255.0
    y = np.argmax(model.predict(data), axis = -1)

    return objects[index_min], rev_conv_label(int(y[0]))

#Init Flask APP
app = flask.Flask(__name__)

#Limit Image Size to 3MB
app.config['MAX_CONTENT_LENGTH'] = int(UPLOAD_LIMIT) * 1024 * 1024

#Path /
@app.route('/', methods=['GET'])
def index():
    index = codecs.open(os.path.join(PATH, 'static/index.html'), 'r', 'utf-8').read()

    return index

#Path /api
@app.route('/api', methods=['GET', 'POST'])
def api():
    if flask.request.method == 'POST':
        response = flask.make_response()

        try:
            #Prase args from URL, recieve image
            auth = flask.request.args['auth']
            verify = flask.request.args['verify']
            image = flask.request.files['image']

            #Auth
            if auth in AUTH:
                image_ext = os.path.splitext(image.filename)[1]

                #Verify supported image type
                if image_ext in ALLOWED_EXTENSIONS:
                    #Recieve Image, random uuid named, stored in /tmp
                    path = os.path.join('/tmp/', str(uuid.uuid4()) + image_ext)
                    image.save(path)
                    image_sha1 = hashlib.sha1(open(path, 'rb').read()).hexdigest()

                    print('Image Path -> ', path)
                    print('Image SHA1 -> ', verify, ' - ', image_sha1)

                    #Verify Image SHA1
                    if verify == image_sha1:
                        response.status_code = 200

                        #Exec Font Identifier
                        try:
                            obj, ft = font_identifier(path)

                            #Instruct response
                            res_json = json.loads('{"Font": "' + str(ft) + '", "Text": "' + str(obj['Text']) + '", "Rect": ' + str(obj['TextRectangles']).replace('\'', '"') + ', "Time":' + str(time.time()) + '}')
                            response = app.response_class(response = flask.json.dumps(res_json), status = response.status_code, mimetype = 'application/json')

                            print('Response to client ->')
                            print(json.dumps(res_json, indent = 4, sort_keys = True))

                        except Exception as error:
                            #Server Error
                            response.status_code = 502

                            print('Error -> ', error)

                        #Delete recieved Image
                        os.remove(path)

                    else:
                        #Precondition Failed (SHA1 Verify Failed)
                        response.status_code = 412

                else:
                    #Unsupported Image Type
                    response.status_code = 415

                    print('Extension ->', image_ext)

            else:
                #Not Authorized
                response.status_code = 401

        except Exception as error:
            #Request Error
            response.status_code = 400

            print('Error -> ', error)

        #Return response to client
        return response

    #Fallback to index if uses GET
    else:
        return flask.redirect(flask.url_for('index'))

#Run font-indentifier app server
if APP_SSL:
    app.run(host = LISTEN, port = PORT, ssl_context = (CERT_PATH, KEY_PATH), debug = DEBUG)

else:
    app.run(host = LISTEN, port = PORT, debug = DEBUG)
