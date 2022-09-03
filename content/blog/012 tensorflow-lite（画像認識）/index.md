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
・USBカメラの画像を取得するにはOpenCVのVideoCapturメソッドを使う。<br>

# インストール
## PINT0309の#USAGE

PINT0309の#USAGE<br>
https://github.com/PINTO0309/TensorflowLite-bin#usage<br>
・apt パッケージのインストール。最初の$が不要なだけでそのままコピペ。<br>
・apt パッケージのインストール後、念の為作業ディレクトリを作成。＋仮想環境を有効化。<br>
```bash
mkdir tflite-bin
cd tflite-bin
python -m venv venv
source venv/bin/activate
```
・TFVER=2.10.0-rc1　以降はbash変数の設定<br>
こんな感じ<br>
```bash
TFVER=2.9.0
PYVER=39
ARCH=aarch64

# そのあと　sudo -H pip3 install \　以降の行を実行（そこでこれらの変数が使われる）

# インストールが終了したら確認
python -c 'import tensorflow as tf;print(tf.__version__)'
```

| 変数名 |  意味 |
| ---- | ---- |
| TFVER | tensorflow-liteのバージョン。値：2.1.0~2.10.0 |
| PYVER | pythonのバージョン。 |
| ARCH | OSのアーキテクチャー。 |


```bash
python3 -V							                    # PYVERの確認方法
python -c 'import platform; print(platform.machine())'	# ARCHの確認方法
```

# 必要ファイルのダウンロード（任意）
次は PINT0309の #operation-check-classification を参考に必要ファイルをダウンロード<br>
https://github.com/PINTO0309/TensorflowLite-bin#operation-check-classification のEnvironmental preparation<br>
<br>
少し改造したスクリプトをここに記述する<br>

```bash
# 必要なディレクトリを作成
mkdir ~/tflite-bin/images;mkdir ~/tflite-bin/models
# 画像ファイルをダウンロード
curl https://raw.githubusercontent.com/tensorflow/tensorflow/master/tensorflow/lite/examples/label_image/testdata/grace_hopper.bmp > ~/tflite-bin/images/grace_hopper.bmp
# ラベルファイルをダウンロード（画像認識の結果のint値[数値]を文字列に変える為のファイル）
curl https://storage.googleapis.com/download.tensorflow.org/models/mobilenet_v1_1.0_224_frozen.tgz | tar xzv -C ~/tflite-bin/models/labels.txt
# モデルファイルをダウンロード
curl http://download.tensorflow.org/models/mobilenet_v1_2018_02_22/mobilenet_v1_1.0_224_quant.tgz | tar xzv -C ~/tflite-bin/models
# 作業ディレクトリに移動
cd ~/test
```

label_image.py というスクリプトをコピペ<br>
https://github.com/PINTO0309/TensorflowLite-bin#operation-check-classification のlabel_image.py<br>
<br>もしくはダウンロード
https://github.com/PINTO0309/TensorflowLite-bin/blob/main/label_image.py<br>
<br>
<br>
実行<br>

```bash
python3 label_image.py \
--num_threads 4 \
--image images/grace_hopper.bmp \
--model_file models/mobilenet_v1_1.0_224_quant.tflite \
--label_file models/labels.txt
```

# 認識
（編集中）


# USBカメラを使った認識
（編集中）

# モデルファイルを自作する
（編集中）
まだよく分かっていない。都度編集の予定。
・Google がチュートリアルを出しているので参考にする。
例：https://www.tensorflow.org/lite/guide/model_maker?hl=ja<br>
・モデルファイル作成には強力なGPU が必要。Google Colaboratory を使うのが無難（無料）<br>
