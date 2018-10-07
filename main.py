#!/usr/bin/env python3
from os.path import abspath, join, dirname, exists
from datetime import datetime
from time import sleep
from threading import Thread
import argparse
import json
import logging

import configparser

from projection import ProjectionMapping
from wmv04n import Webcam
from situation import Situation

def read_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--img", help='optional')
    return parser.parse_args()

def change_vpt(pm, num):
    if num == 3 :
        pm.arukisumaho()
        sleep(10)
    elif num == 4 :
        pm.wide_cross()
        sleep(10)
    elif num == 1 :
        pm.normal_cross()
        sleep(10)
    else:
        pass

def main():
    # コマンドライン引数を読む
    args = read_args()

    # confファイルの読み込み
    conf = configparser.ConfigParser()
    conf.read('./setting.ini', 'UTF-8')

    # log設定
    logging.basicConfig(level=logging.DEBUG,
                        format="%(relativeCreated)08d[ms] - %(name)s - %(levelname)s - %(processName)-10s - %(threadName)s -\n*** %(message)s",
                        filename="log/app.log",
    )

    # 歩きスマホ人数
    arukisumaho_num = 0
    # 人数
    person_num = 0

    if args.img:
        img = abspath(args.img)
    else:
        # 画像ファイル名を設定
        basename = datetime.now().strftime("%Y%m%d-%H%M%S")
        img = "./media/"+basename+".jpg"

        # 画像を撮影
        wc = Webcam(conf.get("webcam", 'ip') ,
                    conf.get("webcam", 'port') ,
                    conf.get("webcam", 'user') ,
                    conf.get("webcam", 'password')
        )
        wc.setup_basic_auth()
        wc.take_picture(img)

    # 写真が存在しない場合終了する
    if not exists(img):
        print('画像がないよ')
        return

    # インスタンス作成
    situation = Situation()
    pm = ProjectionMapping(
        conf.get("vpt", 'ip') ,
        conf.getint("vpt", 'port')
        )

    # 最初に車の動画を流す
    pm.waiting()

    while True:
        if not args.img:
            wc.take_picture(img)
        situation.recognize(img)
        person_num = situation.get_person_num()
        arukisumaho_num = situation.get_arukisumaho_num()
        print('検出された人数： %d' % person_num)
        print('歩きスマホ人数： %d' % arukisumaho_num)

        try :
            # 歩きスマホいる場合
            if arukisumaho_num >= 1:
                pm.arukisumaho()
                sleep(10) # TODO : 動画時間入れる
                pm.waiting()
            else:
                # 歩行者が大勢いる場合
                if person_num > 1:
                    pm.wide_cross()
                    sleep(10) # TODO : 動画時間入れる
                    pm.waiting()
                # 歩行者ひとりいる場合
                elif person_num == 1:
                    pm.normal_cross()
                    sleep(10) # TODO : 動画時間入れる
                    pm.waiting()
                # 歩行者がいない場合
                else:
                    sleep(1)
                    pass

        except KeyboardInterrupt:
            print('バックドア')
            pm_key = int(input('数値を入力 : '))
            change_vpt(pm, pm_key)
            pm.waiting()



if __name__ == "__main__":
    main()
