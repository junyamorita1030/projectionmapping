#!/usr/bin/env python3
#なにこれ？
#カメラから映像を撮影し、集めるだけのジェネレータ
#人の部分を自動でトリミングし、クラス分類に最適な画像をあつめることができる
#カメラが人を捉えなければ、トリミングは行わない。

#事前にやること
#以下のようにフォルダを事前につくっておく。
#media/training/cropped/aruki_sumaho/
#media/training/cropped/pedestrian/
#media/training/non_cropped/



from os.path import join, dirname
from datetime import datetime
import json
import logging
import os
import configparser
import io, http.client, urllib.request, urllib.parse, urllib.error
import logging
from dotenv import load_dotenv
from PIL import Image
from time import sleep

from projection import ProjectionMapping
from wmv04n import Webcam
from situation import Situation


env_path = ".env"
load_dotenv(dotenv_path=env_path)
logger = logging.getLogger(__name__)
p_key = os.environ.get("PEDESTRIAN_PREDICTION_KEY")
i_id = os.environ.get("PEDESTRIAN_ITERATION_ID")

def crop_body(img, body_box,train_type):
    # 画像のサイズ
    im = Image.open(img)
    w,h = im.size
    ix = w * body_box['left']
    iy = h * body_box['top'] * 0.8 #なんか頭のほうがぬけやすいため、すこしboxを上のほうまで拡張させてる。
    ex = w * (body_box['width'] + body_box['left'])
    ey = h * (body_box['height'] + body_box['top'])

    basename = datetime.now().strftime("%Y%m%d-%H%M%S")
    cropped_image_path = ""

    if train_type == "1":
        cropped_image_path = "./media/training/cropped/aruki_sumaho/"+basename+".jpg"
        print(cropped_image_path)
    else:
        cropped_image_path = "./media/training/cropped/pedestrian/"+basename+".jpg"



    im.crop((ix, iy, ex, ey)).save(cropped_image_path)
    im.close()

def detect(p_key, i_id, img):
    headers = {
        # Request headers
        'Content-Type': 'multipart/form-data',
        'Prediction-key': p_key,
    }

    params = urllib.parse.urlencode({
        # Request parameters
        'iterationId': i_id,
    })



    try:
        conn = http.client.HTTPSConnection('southcentralus.api.cognitive.microsoft.com')
        f = open(img, "rb", buffering=0)
        conn.request("POST", "/customvision/v2.0/Prediction/e14525c5-d709-4b5e-8405-13a1530e951c/image?%s" % params, f.readall(), headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        return json.loads(data.decode('utf-8'))

    except Exception as e:
        # print("[Errno {0}] {1}".format(e.errno, e.strerror))
        print(e)


def main():
    # confファイルの読み込み
    conf = configparser.ConfigParser()
    conf.read('./setting.ini', 'UTF-8')

    # log設定
    logging.basicConfig(level=logging.DEBUG,
                        format="%(relativeCreated)08d[ms] - %(name)s - %(levelname)s - %(processName)-10s - %(threadName)s -\n*** %(message)s",
                        filename="log/app.log",
    )

    print("0: correct pedestrian image, \n1: aruki_sumaho image")
    train_type = input('> type 0 or 1\n')
    print(train_type)




    # 画像ファイル名を設定
    basename = datetime.now().strftime("%Y%m%d-%H%M%S")
    img = "./media/training/non_cropped/"+basename+".jpg"
    #img = "./media/testimage_1.jpg"
    num = 0

    while num < 100:
        num += 1

        # 画像を撮影
        wc = Webcam(conf.get("webcam", 'ip') ,
                    conf.get("webcam", 'port') ,
                    conf.get("webcam", 'user') ,
                    conf.get("webcam", 'password')
         )
        wc.setup_basic_auth()
        wc.take_picture(img)
        mcv_result=detect(p_key,i_id,img)
        sleep(1)
        # logger.debug('TRAINING_MCV結果: %s' % mcv_result)

        threshold = 0.9
        for i in range(0,len(mcv_result['predictions'])):
            if mcv_result['predictions'][i]['probability'] > threshold:
                if mcv_result['predictions'][i]['tagName'] == 'pedestrian':
                    print("I detect you!",  num)
                    body_box = mcv_result['predictions'][i]['boundingBox']
                    crop_body(img, body_box, train_type)


if __name__ == "__main__":
    main()
