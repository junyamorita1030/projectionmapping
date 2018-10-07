#!/usr/bin/env python3
import base64
import io, http.client, urllib.request, urllib.parse, urllib.error
import json
from requests import Request, Session
from bs4 import BeautifulSoup


class MsCustomVision_object_detection:
    def __init__(self,prediction_key,iteration_id):
        self.prediction_key = prediction_key
        self.iteration_id = iteration_id


    def object_detection(self, img):
        headers = {
            # Request headers
            'Content-Type': 'multipart/form-data',
            'Prediction-key': self.prediction_key,
        }

        params = urllib.parse.urlencode({
            # Request parameters
            'iterationId': self.iteration_id,
        })

        try:
            conn = http.client.HTTPSConnection('southcentralus.api.cognitive.microsoft.com')
            f = open(img, "rb", buffering=0)
            conn.request("POST", "/customvision/v2.0/Prediction/481a16b3-7e64-44a0-b633-8e43aa648bab/image?%s" % params, f.readall(), headers)
            response = conn.getresponse()
            data = response.read()
            conn.close()
            return json.loads(data.decode('utf-8'))
        except Exception as e:
            # print("[Errno {0}] {1}".format(e.errno, e.strerror))
            print(e)
