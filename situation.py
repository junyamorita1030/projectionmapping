#!/usr/bin/env python3
import os
from datetime import datetime

from dotenv import load_dotenv
import json
import logging
from functools import wraps
import time

from cloudvision import GoogleCloudVision
from ms_custom_vision import MsCustomVision
from ms_custom_vision_object_detect import MsCustomVision_object_detection
from PIL import Image
from stop_watch  import stop_watch

logger = logging.getLogger(__name__)

THRESHOLD = 0.9 # 確からしさはこの程度が妥当

class Situation:

    def __init__(self):
        self._wheelchair_flag = False
        self._person_num = 0
        self._arukisumaho_num = 0
        self.load_env()
        logger.debug('環境変数読み込み')

    def load_env(self):
        env_path = ".env"
        load_dotenv(dotenv_path=env_path)

    def get_wheelchair_flag(self):
        return self._wheelchair_flag

    def get_arukisumaho_num(self):
        return self._arukisumaho_num

    def get_person_num(self):
        return self._person_num

    def __count_person_num(self, gcv_json):
        return len(gcv_json['responses'][0]['faceAnnotations'])

    def __get_face_range(self, gcv_json, i):
        # jsonファイルから顔画像の左上と右下の座標を取り出してtupleで返す
        vbox_1 = gcv_json['responses'][0]['faceAnnotations'][i]['boundingPoly']['vertices'][0]['x']
        vbox_2 = gcv_json['responses'][0]['faceAnnotations'][i]['boundingPoly']['vertices'][0]['y']
        vbox_3 = gcv_json['responses'][0]['faceAnnotations'][i]['boundingPoly']['vertices'][2]['x']
        vbox_4 = gcv_json['responses'][0]['faceAnnotations'][i]['boundingPoly']['vertices'][2]['y']
        logger.debug('face_range: %s, %s, %s, %s' %(vbox_1, vbox_2, vbox_3, vbox_4))
        return (vbox_1, vbox_2, vbox_3, vbox_4)

    def __crop_body_img_old(self, img, face_range):
        # 画像のサイズ
        im = Image.open(img)
        w, h = im.size
        # s:左上の点 e:右下の点
        s_x = max( (2 * face_range[0]) - face_range[2], 0)
        e_x = min( (2 * face_range[2]) - face_range[0], w)
        s_y = max( face_range[1], 0)
        e_y = min( face_range[3] + (4 * (face_range[3] - face_range[1])), h)
        logger.debug('body_range: %s, %s, %s, %s' % (s_x, s_y, e_x, e_y))
        cropped_img = im.crop((s_x, s_y, e_x, e_y))
        im.close()
        # TODO:cropped_imgがcloseしてないかも、、、
        return cropped_img


    def __crop_body(self, img, body_box):
        # 画像のサイズ
        im = Image.open(img)
        w,h = im.size
        ix = w * body_box['left']
        iy = h * body_box['top']# * 0.8 #なんか頭のほうがぬけやすいため、すこしboxを上のほうまで拡張させてる。
        ex = w * (body_box['width'] + body_box['left'])
        ey = h * (body_box['height'] + body_box['top'])
        logger.debug('body_range: %s, %s, %s, %s' % (ix, iy, ex, ey))
        # cropped_img = im.crop((ix, iy, ex, ey))

        basename = datetime.now().strftime("%Y%m%d-%H%M%S")
        dirname = os.path.dirname(img)
        # FIXED mediaディレクトリに保存されていなかった
        cropped_image_path = dirname + "/cropped_" + basename + ".jpg"
        im.crop((ix, iy, ex, ey)).save(cropped_image_path)
        im.close()
        return cropped_image_path



    def recognize(self,img):
        # 環境変数の読み込み( todo : 後々変えたい)
        aruki_sumaho_prediction_key = os.environ.get("ARUKI_SUMAHO_PREDICTION_KEY")
        aruki_sumaho_iteration_id = os.environ.get("ARUKI_SUMAHO_ITERATION_ID")
        aruki_sumaho_endpoint = os.environ.get("ARUKI_SUMAHO_ENDPOINT")

        pedestrian_prediction_key = os.environ.get("PEDESTRIAN_PREDICTION_KEY")
        pedestrian_iteration_id = os.environ.get("PEDESTRIAN_ITERATION_ID")
        pedestrian_endpoint = os.environ.get("PEDESTRIAN_ENDPOINT")

        # 認識ごとにカウントを0にする。
        self._person_num = 0
        self._arukisumaho_num = 0

        # 人体検知の準備をする
        pedestrian_mcv = MsCustomVision(pedestrian_prediction_key,
                                        pedestrian_iteration_id,
                                        pedestrian_endpoint # TODO エンドポイント外出し FIXED ichi
                                         )
        arukisumaho_mcv = MsCustomVision(aruki_sumaho_prediction_key,
                                         aruki_sumaho_iteration_id,
                                         aruki_sumaho_endpoint
                                         )

        # 歩行者を物体検知して処理結果をJSONで受け取る
        pedestrian_mcv_result = pedestrian_mcv.classification(img)
        logger.debug('MCV結果: %s' % pedestrian_mcv_result)

        # エラーの場合はbreak
        if pedestrian_mcv_result == None:
            return None


        for result in pedestrian_mcv_result['predictions']:
            if result['probability'] > THRESHOLD:
                if result['tagName'] == 'pedestrian':
                    self._person_num += 1

                    body_box = result['boundingBox']
                    cropped_image_path = self.__crop_body(img, body_box)
                    print(cropped_image_path)

                    arukisumaho_mcv_result = arukisumaho_mcv.classification(cropped_image_path)
                    logger.debug(arukisumaho_mcv_result)
                    print(arukisumaho_mcv_result)
                    
                    # 90%以上歩きスマホと判定した場合
                    if arukisumaho_mcv_result['predictions'][0]['probability'] > THRESHOLD and arukisumaho_mcv_result['predictions'][0]['tagName'] == 'aruki_sumaho':
                        self._arukisumaho_num += 1
                        logger.debug('%d番目に歩きスマホおる' % self._person_num)