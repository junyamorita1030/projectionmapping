## Title: STreet OPerator [STOP]

### English Ver. is written BELOW.

## Related challange:

* Tensor Flow

* Microsoft Custom Vision

* Open CV

* Pillow

* Video Projection Tool (VPT)

* Adobe After Effect


## Functional description:
交通安全を願う市民のために、私たちは全く新しい交通制御システム -STreet OPerator (以下STOPと呼ぶ)を作りました。

残念なことに、今も私たちは、歩行者を巻き込む悲惨な交通事故を耳にすることがあります。
最近は特に、歩きスマホが原因で、道路横断中に向かってくる車両に気がつかず、命を落とす例が顕著になってきました。(米国では、歩きスマホに対する罰金も始まっているようです。)

そんな中、自動運転車等の車に対する技術革新が進んでいるにも関わらず、歩行者に対する交通技術は、「3色の信号機」の時代から進化していません。

このような問題を解決するため、ダイナミックかつインテリジェントな交通制御システム、STOPを開発しました。

STOPはITSの一種と考えることができます。ただ、これは従来の信号制御技術のようなものよりずっと、歩行者にとってインタラクティブです。

これは非常にシンプルな技術で、プロジェクションマッピングの技術を使って、道路標示を道路上に投影します。

しかし、STOPは道路上のどこでも、いつでも、交通状況に応じた道路標示を投影できます。

* 歩行者が側道で立ち止まった時は、歩行者を検出して横断歩道を投影します.

* 歩行者が歩きスマホをしながら道路上に現れた時は、歩行者の姿勢を検出し、歩行者・車両双方にわかるような緊急信号を道路に表示します。

* たくさんの歩行者がいた時は、横断歩道の幅を広げます。

これらの機能によって、STOPは歩行者の安全を守り、交通事故を減らします。

## Functional prototype:

https://gitlab.ballpark.altemista.cloud/moritajny/hackathon2018_CORP_STOP/tree/master


## Technical description:

### Archtecture

STOPには3種類のデバイスを使います。

1. プロジェクタ

1. ネットワークカメラ

1. 機械学習用サーバ


### Logic

3つのステップによって本システムが機能します。

1. 歩行者の検出

1. 交通状況(歩きスマホ)の識別

1. 道路標示の投影


#### 歩行者の検出

低画質のネットワークカメラを用いて、歩行者の映像を取得します。
取得した映像は、1秒ごとのフレーム画像で切り出されます。

機械学習サーバに取得したフレーム画像を送信し、歩行者を検出します。
この検出には、非常にシンプルなAIを利用しています。

[AIの設計]
Microsoft製の物体検出アルゴリズム(Custom Vision - Object Detection)を用いました。本アルゴリズムは、転移学習を用いることで、既存の人物検出アルゴリズムを、横断中の人物検出に適応させることで高い精度を実現しています。

[AIの学習]
30枚程度の横断歩道画像を準備し、その中から歩行者の部分に該当するエリアを手動で指定し、学習させました。

[AIの評価]
結果、学習したモデルはほぼ100%の確率で横断中の歩行者を検出可能となり、また一枚の画像から歩行者に該当するエリアを切り取ることができます。

#### 交通状況(歩きスマホ)の識別

画像中から小さなスマートフォンを検出することが難しいため、歩きスマホの識別はすこし高難度です。

この問題を解決するため、私たちはクラス分類を用いて歩行者の姿勢を識別することにしました。

[AIの設計]
Microsoftのクラス分類アルゴリズムを用いて、画像のラベル付けを行います。
一枚の画像に対して1つのラベルのみをつける仕組みを採用することで、高い精度を実現します。

[AIの学習]
歩きスマホ画像、歩行中画像を250組用意し、学習データとして入力しました。

[AIの評価]
この結果、本モデルは歩きスマホの歩行者と普通の歩行者を高い精度(Racall 80%, Presicion 80%)で実現しました。

#### 道路標示の投影

道路標示の投影は非常にシンプルで、機械学習サーバのレスポンスに応じて、投影する映像を切り替えています。
ただし、どのような場所からでも適切な道路標示を行えるよう、VPTとよばれるマッピングソフト用いています。
このマッピングソフトは、これまでの機械学習エンジンと連携しないため、コントローラにおいてマッピングソフトとの連携処理を記述しています。


## Teams for developing the work result in the Global Final:

現在、STOPは歩行者の状態のみを識別し、道路上にサインを標示するのみとなっています。
今後、以下のような改良を加え、よりダイナミックでインタラクティブな交通制御を実現します。

自動車およびそのほか交通車両の検出による、より複雑な道路状況の識別
エッジ側にて処理可能な軽量モデルの実装による、よりニアリアルタイムでの検出と道路標示投影
道路標示の3次元投影の実現による、より直感的な情報量の多いサインの投影

## Innovation:

主なイノベーションは以下です。

* プロジェクションマッピング技術と機械学習技術の融合

* 歩きスマホをしている人の高精度な検出.

* 動画情報に対する、セミリアルタイムでの検出処理の実現


## Impact and users:

本アイデアのインパクトは下記です。

* 歩行者がいつでもどこでも安全に道路を渡れるようになる

* 横断歩道上での事故の撤廃

* 道路から信号機を撤廃できる


## Videos:
https://gitlab.ballpark.altemista.cloud/moritajny/hackathon2018_CORP_STOP/blob/master/movie.mp4



## Requirements
- Python Version 3.4 or later
- requests
- bs4
- python-osc
- python-dotenv
- Pillow
- tensorflow
- opencv-python

## How to use
- when you use by taking images by web cam
```
python main.py
```
- when you use by loading static images on your computer
```
python main.py --img=(path)
```





###日本語の説明は本文上部に記載しております。

## Related challange:

* Tensor Flow

* Microsoft Custom Vision

* Open CV

* Pillow

* Video Projection Tool (VPT)

* Adobe After Effect


## Functional description:
we developed the STreet OPerator, hereinafter reffered to as STOP, for the pedestrian who want traffic safety.

Unfortunately, we still hear the terrible traffic accidents involving a pedestrian.

Moreover, recently the accident is increasing because pedestrians are texting while crossing the road.

Even the time is coming to start sell self-driving car, the technologies for pedestrian is not evolved from "traffic lights".


In order to solve this problem, we developed dynamic intelligent traffic system, STOP.

STOP is a kind of Intelligent Traffic System, but it is far more interactive.

STOP just projects images of traffic signs on road, to pedestrian and automotive.

But it works in everywhere, in real time, and in different situation;

* when the pedestrian stands at any side of the road, STOP detect the pedestrians and projects the crosswalk image on road.

* when the pedestrian is carelessly crossing while texting, STOP detect the one who are viewing their electronic devices and projects the "stop sign" to protect the pedestrian.

* when there are a lot of pedestrians, STOP widen the crosswalk depends on the number of them.


Possessing these features, STOP can protect the pedestrians and reduce the traffic accidents.

## Functional prototype:

https://gitlab.ballpark.altemista.cloud/moritajny/hackathon2018_CORP_STOP/tree/master


## Technical description:

### Archtecture

there are 3 devices in STOP.

1. Projector

1. Network camera

1. Machine learning server


### Logic

there are 3 parts.

1. Detecting pedestrians

1. Recognizing traffic Situation

1. Projecting the traffic signs on road.


#### Detecting pedestrians

By using normal network camera, we take a photos of pedestrians in high frequency.

Machine learning server get images from network camera, and detect the pedestrians.

We simply made this function by using AI.

We took over 200 images on the road, and cropped the pedestrians manually, and give them to machine learning program as training data.

As a consequence, the trained model can detect the pedestrians and moreover find the coordinate position of them as bounding box.

#### Recognizing traffic Situation

Recognizing traffic situation is a little bit difficult, specifically in recognizing the one who are viewing their electronic devices.

Even if we do the same thing in detection, the machine learning model cannot detect tiny difference of pedestrians posture.

In order to solve this challenge, we decide to use another kind of AI, classification.

First, we cropped the pedestrian's body by using the function of detection, and prepare 200 sets of normal posture image and viewing smartphone images.

Then we made the classification model by using these images as training data.

After this, the model can recognize the one who are viewing electronic devices or not in high recall and precision (over 80%).

#### Projecting the traffic signs on road.

This function is easy to image.

The projector get the 4 type response of Machine Learning Server;

* 1 is that there is no pedestrian.

* 2 is there is a pedestrian.

* 3 is there is over 2 pedestrians.

* 4 is there is the careless pedestrian who are starting cross the road.

depends on the response, the projector projects the sinn on road.


## Teams for developing the work result in the Global Final:

Currently STOP is projecting the sign on the static position.

But in order to become our concept true, STOP should be able to project the dynamic sign in any place depends on situation.

In the global final, STOP will detect not only the existence of pedestrians or automotives, but also of the "accurate position and status" of them.
by this update, STOP will projects not only static sign, but also dynamic sign below;

the sign for the cars in the hide of corner.
the sign emphasizing walking pedestrian.
the sign indicating the best route for the pedestrian.

## Innovation:

the innovative point of this system is;

* Detecting if the one texting or not by using crassification.

* Detecting the object in near-real time

## Impact and users:

* Pedestrians can cross road at any point they want

* we can replase all traffic lights.

* we can keep safety for those who are crossing the road while tecting


## Videos:
https://gitlab.ballpark.altemista.cloud/moritajny/hackathon2018_CORP_STOP/blob/master/movie.mp4




## Requirements
- Python Version 3.4 or later
- requests
- bs4
- python-osc
- python-dotenv
- Pillow
- tensorflow
- opencv-python

## How to use
- when you use by taking images by web cam
```
python main.py
```
- when you use by loading static images on your computer
```
python main.py --img=(path)
```

