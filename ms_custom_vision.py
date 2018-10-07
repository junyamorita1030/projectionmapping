#!/usr/bin/env python3
import base64
import io, http.client, urllib.request, urllib.parse, urllib.error
import json
from requests import Request, Session
from bs4 import BeautifulSoup
from logging import getLogger


logger = getLogger(__name__)

class MsCustomVision:
    def __init__(self,prediction_key,iteration_id,endpoint):
        self.prediction_key = prediction_key
        self.iteration_id = iteration_id
        self.endpoint = endpoint
        logger.debug('オブジェクト生成')


    def classification(self, img):
        headers = {
            # Request headers
            'Content-Type': 'multipart/form-data',
            'Prediction-key': self.prediction_key,
        }

        params = urllib.parse.urlencode({
            # Request parameters
            'iterationId': self.iteration_id,
        })

        result = None
        try:
            conn = http.client.HTTPSConnection('southcentralus.api.cognitive.microsoft.com')
            with open(img, "rb", buffering=0) as f:
                conn.request("POST", "/customvision/v2.0/Prediction/"+self.endpoint+"/image?%s" % params, f.readall(), headers)
                response = conn.getresponse()
                # HTTP通信正常時
                if response.status == 200:
                    data = response.read()
                    logger.debug('リクエスト成功　MVSステータスコード：200')
                    result = json.loads(data.decode('utf-8'))
                # HTTP通信エラー時
                else:
                    logger.debug('リクエスト失敗　MVSステータスコード：' + str(response.status))
            conn.close()
            return result
        except Exception as e:
            logger.exception('Error : %s', e)
