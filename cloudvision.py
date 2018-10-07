#!/usr/bin/env python3
import base64
import json
from requests import Request, Session
from bs4 import BeautifulSoup

URL = "https://vision.googleapis.com/v1/images:annotate?key="

class GoogleCloudVision:
    def __init__(self,api_key):
        self.api_key = api_key

    def _img_to_bin(self, img):
        captcha = open(img, 'rb').read()
        return base64.b64encode(captcha).decode("utf-8")

    def object_recognition(self, img):
        encoded_img = self._img_to_bin(img)
        method = "POST"
        headers = {"Content-Type" : "application/json"}

        json_data = {
            'requests': [
                {
                    'image': {
                        'content': encoded_img
                    },
                    'features': [
                        {
                            'type': "FACE_DETECTION",
                            'maxResults': 10
                        }
                    ]
                }
            ]
        }
        body = json.dumps(json_data).encode("utf-8")

        session = Session()
        request = Request(method, URL + self.api_key, data=body,headers=headers)
        prepped = session.prepare_request(request)
        response = session.send(prepped, verify=True, timeout=60)
        if response.status_code == 200:
            return response.text
        else:
            return "error"
