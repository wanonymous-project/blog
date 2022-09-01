---
title: Raspberry Pi で tensorflow-lite
date: "2022-09-01"
description: "tensorflow-lite で画像認識"
---

# 概要
PINTO0309という人のGithubレポジトリ（以下PINTO0309とする）を使うことで、簡単にインストール可能。

ポイント
・パフォーマンスを考えると、TensorflowよりTensorflow-liteのほうが無難。
・「aarch64 OS」のほうがパフォーマンスが良いらしい
・USBカメラの画像を取得するにはOpenCVのVideoCapturメソッドを使う。

# インストール
## PINT0309の#USAGE

PINT0309の#USAGE
・apt パッケージのインストール。最初の$が不要なだけでそのままコピペ。
・TFVER=2.10.0-rc1　以降はbash変数の設定
こんな感じ
```bash
TFVER=2.9.0
PYVER=39
ARCH=aarch64

# そのあと　sudo -H pip3 install \　以降の行を実行（そこでこれらの変数が使われる）
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


# モデルファイルのダウンロード



# 認識
