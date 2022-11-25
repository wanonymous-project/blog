---
title: Raspberry Pi で tensorflow-lite
date: "2022-09-01"
description: "tensorflow-lite で画像認識"
---

# 概要
PINTO0309という人のGithubレポジトリ（以下PINTO0309とする）を使うことで、簡単にインストール可能。
https://github.com/PINTO0309/TensorflowLite-bin

ポイント<br>
・パフォーマンスを考えると、TensorflowよりTensorflow-liteのほうが無難。<br>
・「aarch64 OS」のほうがパフォーマンスが良いらしい<br>
・USBカメラの画像を取得するにはOpenCVのVideoCaptureメソッドを使う。<br>

# 環境
使用OS：2022-09-06-raspios-bullseye-arm64.img
https://www.raspberrypi.com/software/operating-systems/

# インストール
## PINT0309の#USAGE
PINT0309の#USAGE<br>
https://github.com/PINTO0309/TensorflowLite-bin#usage<br>
・apt パッケージのインストール。最初の$が不要なだけでそのままコピペ。<br>
```bash
# $ を省いたスクリプトをここにも記述。
sudo apt install -y \
swig libjpeg-dev zlib1g-dev python3-dev \
unzip wget python3-pip curl git cmake make

sudo pip3 install numpy==1.23.2
sudo pip3 install Pillow                # これも有った方が良いので追加
```

<br>
・TFVER=2.10.0-rc1　以降はbash変数の設定<br>
こんな感じ<br>

```bash
TFVER=2.10.0		# 2022-11-26現在で動作確認できている ver:2.9.0, 2.10.0
PYVER=39
ARCH=aarch64
```

| 変数名 |  意味 |
| ---- | ---- |
| TFVER | tensorflow-liteのバージョン。値：2.1.0~2.10.0 |
| PYVER | pythonのバージョン。 |
| ARCH | OSのアーキテクチャー。 |

```bash
# PYVERの確認方法
python3 -V
# ARCHの確認方法
python -c 'import platform; print(platform.machine())'
```

## インストール
そのあと　sudo -H pip3 install \　以降の行を実行する事でtensorflow-lite をインストール出来る。<br>
（上で設定した変数は、ここで使われる）<br>
https://github.com/PINTO0309/TensorflowLite-bin#usage<br>

```bash
# 念の為、まったく同じスクリプトをここにも記述。
sudo -H pip3 install \
--no-cache-dir \
https://github.com/PINTO0309/TensorflowLite-bin/releases/download/v${TFVER}/tflite_runtime-`echo ${TFVER} | tr -d -`-cp${PYVER}-none-linux_${ARCH}.whl

# インストールが終了したら確認
python -c 'import tflite_runtime as tf;print(tf.__version__)'
```


## 準備
必要なファイルをダウンロード<br/>
まとめてダウンロードできるので、以下のスクリプトがおすすめ。<br/>
```bash
mkdir -p all_models
wget https://dl.google.com/coral/canned_models/all_models.tar.gz
tar -C models -xvzf all_models.tar.gz
rm -f all_models.tar.gz
```
参考：https://github.com/google-coral/examples-camera/blob/master/download_models.sh

［追記］ラベルファイルは以下から取った方が良い。上記のは色々とおかしかった。
https://github.com/amikelive/coco-labels/blob/master/coco-labels-2014_2017.txt

# 物体検出（Object detection）
物体検出の基礎部分の理解の為、出来る範囲で最小限コードにした。<br/>


## ディレクトリ構成
<hr>
├ images \<br/>
│ ├ grace_hopper.bmp    (テスト画像。なんでも良い)<br/>
├ models \<br/>
│ ├ coco_labels.txt    (ラベルファイル)<br/>
│ ├ mobilenet_ssd_v2_coco_quant_postprocess.tflite    (モデルファイル)<br/>
├ detect_lite.py<br/>
<hr>

## ソースコード
[detect_lite.py]

```python
import numpy as np
from PIL import Image                                 # pip3 install Pillow
from tflite_runtime.interpreter import Interpreter

if __name__ == '__main__':
    # モデルファイル読み込み
    interpreter = Interpreter(
      model_path="models/mobilenet_ssd_v2_coco_quant_postprocess.tflite",
    )
    
    # メモリ確保
    interpreter.allocate_tensors()

    # 学習モデルの入力層・出力層のプロパティを取得
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # 入力層の情報から画像サイズを取り出す
    height = input_details[0]['shape'][1]
    width = input_details[0]['shape'][2]
    
    # 画像ファイルの読み込み
    img = Image.open("images/grace_hopper.bmp")
    img = img.resize((width, height))
    
    # 入力画像の変換（行列≒配列の次元を増やす）
    input_data = np.expand_dims(img, axis=0)

    # 入力テンソル（≒配列）の設定
    interpreter.set_tensor(input_details[0]['index'], input_data)

    # 推論実行
    interpreter.invoke()
	
    # 推論結果
    boxes = interpreter.get_tensor(output_details[0]['index'])[0]       # 検出のバウンディングボックス
    classes = interpreter.get_tensor(output_details[1]['index'])[0]     # 分類されたラベル情報
    scores = interpreter.get_tensor(output_details[2]['index'])[0]      # 一致率

    # 結果を表示する
    print('boxes:\n%s' % boxes)
    print('classes:\n%s' % classes)
    print('scores:\n%s' % scores)
```

```python
    # バウンディングボックスの処理
    index = 0
    draw = ImageDraw.Draw(frame)
    
    for score in scores[scores >= 0.4]:      # 結果をスコアで抽出(numpy 独自の抽出法)
        # 座標位置
        x_min = int(boxes[index][1] * frame.width)
        y_min = int(boxes[index][0] * frame.height)
        x_max = int(boxes[index][3] * frame.width)
        y_max = int(boxes[index][2] * frame.height)

        # 確認（任意）
        print('index:%s\tscore:%0.2f\tbox:%s' %  (index, score, boxes[index]))

        # バウンディングボックスの描写
        draw.rectangle((x_min, y_min, x_max, y_max))

        # カウントアップ
        index +=1 

    frame.save('images/result.jpg', quality=95)
```


## 参考資料
https://github.com/rianrajagede/object-detection/blob/master/scripts/TFLite_detection_image.py<br/>
<br/>

## 推論結果の見方
> ・それぞれの list の大きさ(len) は、推論実行の結果検出した物体の数を示す。<br/>
> ・boxes 内には座標情報を格納した list が格納されている。（list の list になっている） <br/>
> 構造は [y_min, x_min, y_max, x_max] らしい。<br/>
> ・classes （物体の種類）の数値 ≒ ラベルファイルの行番号。<br/>
> ・scores は 0 < n < 1 の小数値で格納され、パーセンテージを示す。<br/>
<br/>

## 動作確認できたモデル
・ Mobilenet SSD version2<br/>
（上記の方法でダウンロードできる）<br/>
<br/>
・EfficientDet-Lite4<br/>
DL：https://tfhub.dev/tensorflow/lite-model/efficientdet/lite4/detection/default/2<br/>
<br/>
<br/>

# USBカメラを使った物体検出
USBカメラは OpenCV の VideoCaptureメソッドを使うのが楽。<br>

## 準備
[bash]
```bash
# OpenCV をインストール
sudo pip3 opencv-python	

# ビデオデバイスの番号を確認
v4l2-ctl --list-devices
# > 例
# > C505 HD Webcam (usb-0000:01:00.0-1.3):
# > 	/dev/video0
# video{n} の n のところの数値を覚えておく。
# → この例の場合 0
```


## ソース
ディレクトリ構成は「物体検出」と同じ<br>
[detect_cv.py]
```python
import cv2
import numpy as np
from tflite_runtime.interpreter import Interpreter

# クラスごとに色分けをする仕組み（任意）
colors = [
  (0, 0, 255),
  (0, 64, 255),
  (0, 128, 255),
  (0, 192, 255),
  (0, 255, 255),
  (0, 255, 192),
  (0, 255, 128),
  (0, 255, 64),
  (0, 255, 0),
  (64, 255, 0),
  (128, 255, 0),
  (192, 255, 0),
  (255, 255, 0),
  (255, 192, 0),
  (255, 128, 0),
  (255, 64, 0),
  (255, 0, 0),
  (255, 0, 64),
  (255, 0, 128),
  (255, 0, 192),
  (255, 0, 255),
  (192, 0, 255),
  (128, 0, 255),
  (64, 0, 255),
]

def load_labelfile(filename):
    label_list = []
    input_file = open(filename, 'r')
    for l in input_file:
        label_list.append(l.strip())
    return label_list


if __name__ == '__main__':
    # ラベルファイル読み込み
    label_list = load_labelfile('models/coco_labels.txt')
    
    # モデルファイル読み込み
    interpreter = Interpreter(
        model_path="models/mobilenet_ssd_v2_coco_quant_postprocess.tflite",
    )
    
    # メモリ確保
    interpreter.allocate_tensors()
    
    # 学習モデルの入力層・出力層のプロパティを取得
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    
    # 入力層の情報から画像サイズを取り出す
    height = input_details[0]['shape'][1]
    width = input_details[0]['shape'][2]
    
    # カメラの使用を開始
    cap=cv2.VideoCapture(0)                 # 上で確認した数値を入れる
	
	# カメラの設定（任意）
    #cap.set(cv2.CAP_PROP_FPS, )            # カメラFPSを設定

    # カメラ画像の幅と高さを取得
    frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    # カメラが有効な限りループ
    while cap.isOpened():
        # 画像を取得
        ret, frame = cap.read()

        if not ret:
            break
        
        # サイズを変更
        img = cv2.resize(frame, dsize=(height,width))

        # 入力画像の変換（行列≒配列の次元を増やす）
        input_data = np.expand_dims(img, axis=0)

        # 入力テンソル（≒配列）の設定
        interpreter.set_tensor(input_details[0]['index'], input_data)

      	# 推論実行
        interpreter.invoke()

        # 推論結果
        boxes = interpreter.get_tensor(output_details[0]['index'])[0]       # 検出のバウンディングボックス
        classes = interpreter.get_tensor(output_details[1]['index'])[0]     # 分類されたラベル情報
        scores = interpreter.get_tensor(output_details[2]['index'])[0]      # 一致率

        # バウンディングボックスの処理
        index = 0
        for score in scores[scores >= 0.2]:      # 結果をスコアで抽出(numpy 独自の抽出法)
            # 座標位置
            x_min = int(boxes[index][1] * frame_width)
            y_min = int(boxes[index][0] * frame_height)
            x_max = int(boxes[index][3] * frame_width)
            y_max = int(boxes[index][2] * frame_height)

            # クラスのラベル番号
            label_idx = int(classes[index])

            # 90クラスあるモデルファイルがあるらしい。例外になるので弾く。
            if label_idx >= 80: continue

            # バウンディングボックスの色
            color = colors[label_idx % len(colors)]

            # バウンディングボックスの描写
            cv2.rectangle(frame, \
                (x_min, y_min), (x_max, y_max), color, 3)

            # クラスの文字列を描写
            cv2.putText(frame, ('%s (%.3f)' % (label_list[label_idx], score)), (x_min + 10, y_max - 20), \
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 1, cv2.LINE_AA)

            # カウントアップ
            index+=1

        # 画像を表示する
        cv2.imshow('camera capture', frame)

        # q が押されたら終了
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # OpenCV オブジェクトの破棄
    cap.release()
    cv2.destroyAllWindows()
```


## ssh でラズパイにログインする場合
標準では ssh でのGUIは無効なため、カメラ画像を確認する cv2.imshow() メソッドが使えない。<br>
以下の方法の内いずれかを選択する。bash でssh を実行する場合<br>

```bash
ssh usi@192.168.11.94 -X          # -X オプションを指定
```

~/.ssh/config を使う場合

```bash
Host my_rspi
    HostName 192.168.1.1
    User pi
    ForwardX11 yes              # 【 ここ 】
```

補足：(2022-09-24)
方法は色々あるらしい。[ SSH X11 Forwarding ]で検索すると色々出てくる。




# クラス分類（Classification）
## 必要ファイルをダウンロード
次は PINT0309の #operation-check-classification を参考に。<br>
まずは必要ファイルのダウンロード。<br>
https://github.com/PINTO0309/TensorflowLite-bin#operation-check-classification のEnvironmental preparation<br>
<br>
少し改造したダウンロード用スクリプトをここに記述する。<br>

```bash
# 必要なディレクトリを作成
cd; mkdir tflite-bin; cd tflite-bin; mkdir ~/tflite-bin/images; mkdir ~/tflite-bin/models
# 画像ファイルをダウンロード
curl https://raw.githubusercontent.com/tensorflow/tensorflow/master/tensorflow/lite/examples/label_image/testdata/grace_hopper.bmp > ~/tflite-bin/images/grace_hopper.bmp
# ラベルファイルをダウンロード（画像認識の結果のint値[数値]を文字列に変える為のファイル）
curl https://storage.googleapis.com/download.tensorflow.org/models/mobilenet_v1_1.0_224_frozen.tgz | tar xzv -C ~/
mv ~/mobilenet_v1_1.0_224/labels.txt ~/tflite-bin/models;rm -r ~/mobilenet_v1_1.0_224/
# モデルファイルをダウンロード
curl http://download.tensorflow.org/models/mobilenet_v1_2018_02_22/mobilenet_v1_1.0_224_quant.tgz | tar xzv -C ~/tflite-bin/models
```
<br>

## label_image.py のダウンロード
label_image.py というスクリプトを ~/tflite-bin/ 直下にコピペ<br>
https://github.com/PINTO0309/TensorflowLite-bin#operation-check-classification のlabel_image.py<br>
もしくは<br>
https://github.com/PINTO0309/TensorflowLite-bin/blob/main/label_image.py<br>
<br>
一箇所だけ修正が必要 53行目付近<br>

```python
  #interpreter = Interpreter(
  #  model_path="foo.tflite",
  #  num_threads=args.num_threads
  #)
  # ↓
  interpreter = Interpreter(
    model_path=args.model_file,
    num_threads=args.num_threads
  )
```

<br>
実行<br>

```bash
python3 label_image.py \
--image images/grace_hopper.bmp \
--model_file models/mobilenet_v1_1.0_224_quant.tflite \
--label_file models/labels.txt
```

## 補足
> label_image.py のargparse.ArgumentParser() のdefault の値はそれぞれ変。
> 今回は label_image.py 実行時のコマンドライン引数で調整したが、
> label_image.py 内のdefault 値を変更しても良い


# モデルファイルを自作する（編集中）
まだよく分かっていない。都度編集の予定。<br>
・Google がチュートリアルを出しているので参考にする。<br>
例：https://www.tensorflow.org/lite/guide/model_maker?hl=ja<br>
・モデルファイル作成には強力なGPU が必要。Google Colaboratory を使うのが無難（無料）<br>



# 資料
公式 object detection<br>
https://github.com/tensorflow/models/tree/master/research/object_detection

有志の人がカスタマイズしなおした object detection<br>
https://github.com/karaage0703/object_detection_tools

coral のサンプル<br>
https://github.com/google-coral/examples-camera/tree/master/opencv<br>

OpenCVのバージョンについて<br>
ver== 4.3.0.38, 4.4.0.44, 4.4.0.46 ラズパイ上でのビルドが必要<br>
ver== 4.5.1.48, 4.6.0.66 コンパイル済.whでインストール可能<br>

colab チュートリアル<br>
https://colab.research.google.com/drive/1bb2QfeMEWomL-UA_Y68QqbNA0GnXVQoV?usp=sharing
