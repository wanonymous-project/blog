---
title: IoTボタン
date: "2022-07-05"
description: "ダイソーのボタンでIoTボタン実現"
---

# 目的

日常のタスク（ペットの餌やり・水やり）の記録を試験的に実施

# 全体概要

ダイソーのボタンをクリックすると、Google Spread Sheetに記録される。同時に記録されたことがわかるよう、google home speakerから音声通知される。

▼アーキテクチャ
![](2022-07-05-22-04-23.png)


# 手順

## Rasberry PIとボタンのbluetooth接続

ペアリング作業を実施する

### ①必要なパッケージのインストール
https://qiita.com/h-sakano/items/bffe4aafb8316659be8a

### ②ペアリング
以下を参考に実施。
※bluetoothctlはsudoで実行しないと失敗するため注意

https://monomonotech.jp/kurage/raspberrypi/daiso_btshutter.html

## pythonプログラムの開発

pythonでコードを開発する。Google Homeへの接続は、node.jsを利用するため別でプログラムを用意する。

### ①ソースコード全体像

まずはソースコード全体像

```python
#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Python IoT Button"""


import evdev
from evdev import InputDevice, categorize, ecodes
import datetime
from time import time, sleep
from urllib import request, error
import requests
import subprocess
#import settings


# 長押しされたとみなす時間(秒)
hold_time_sec = 0.5
button_symbol = "A"

def main():
    print("Waiting for device to become ready...")
    dev_path = ""
    while(True):
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]

        for device in devices:
            if("B8:27:EB:A2:AE:CE" in device.phys):
                dev_path = device.path
        if (dev_path == "") :
            sleep(1)
        else : break

    dev = InputDevice(dev_path)
    dev_name = dev.name
    dev_phys = dev.phys

    print("IoT Button is ready.")
    old = 0
    button_android = 0
    button_ios = 0

    for event in dev.read_loop():

        if event.type == ecodes.EV_KEY:

            print("------------調査用-------------")
            print("type:" + str(event.type))
            print("value" + str(event.value))
            print("code" + str(event.code))
            print(evdev.ecodes.KEY[115])
            print("-------------------------------")

            if event.value == 1: #キーを押し下げる
                if event.code == evdev.ecodes.KEY_VOLUMEUP:  #キーコード：115。なぜかどちらのボタンをクリックしてもkey:115が飛ぶ
                    button_android = 1
                    button_ios = 1
                    push_time = time() #押した時間の記録

            if event.value == 0: #キーを押し上げる

                if time() - push_time > hold_time_sec: #長押しのとき
                    record_and_notice(dev_name,dev_phys,"hold")
                else:
                    record_and_notice(dev_name,dev_phys,"push")


def record_and_notice(dev_name,dev_phys,button):

    try:
        url = 'https://script.google.com/macros/s/AKfycgagaogpajgpjmUod2y_3eNAeyBJKS6bafageX3FtW-STFAFY24vbhS1iWEafaXyuPaarAqp2An0A/exec'+'?device_name='+dev_name+'&device_phys='+dev_phys+'&button_symbol='+button_symbol+'&button='+button
        print(button_symbol)
        print(button)
        print(url)
        requests.get(url)

    except error.HTTPError as err:
        print(err.code)
    except error.URLError as err:
        print(err.reason)

    command = "sudo node /home/yukiyoshi1992/google_home/IoT_button_"+button_symbol+"_" + button + ".js"
    print(command)

    subprocess.run([command],shell = True)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
print("\n")
```

### ②ポイントの解説

- `evdev`を利用する。
- `code`には本来ボタンごとに違うコードがはいってくるはずなので、それでボタンを判別できる。（何故か今回はどのボタンでも同じ値が入ってきたため判別できなかったが）
- `value`にはボタンを押したとき1、ボタンを離したとき0が入ってくるため、その時間差で長押しを判定している
- `subprocess`で、Google Home動作用のnode.jsを起動している


※ソースコード雑でごめんなさい。必要に応じてブラッシュアップしていきますｗ


## サービスとして、pythonを継続起動

以下を参考に実施
https://my-web-note.com/raspberry-pi-python-daemon/

▼サービスの設定ファイル
```
[Unit]
Description=IoT_button_A

[Service]
ExecStart=/usr/bin/python3 /home/yukiyoshi1992/IoT_button/IoT_button_A.py
Restart=always
RestartSec=10
type=simple

[Install]
WantedBy=multi-user.target
```

※`ExcecStart`のコマンドを絶対パスで指定しないとうまくいかない可能性が高いので注意


## Google App Scriptで受信したデータをGoogle Spread Sheetに書き込む

ソースコードは以下
```
function doGet(e) {

  //データを受信する
  var device_name = e.parameter.device_name;
  var device_phys = e.parameter.device_phys;
  var button_symbol = e.parameter.button_symbol;
  var button = e.parameter.button;

  //現状Activeになっているsheetを取得
  var sheet = SpreadsheetApp.getActiveSheet();
 
  //現在日時をspreadsheetへ書き込み
  sheet.appendRow([new Date(),device_name,device_phys,button_symbol,button]);
}
```

## Google Homeをしゃべらせるため、node.jsのプログラムを開発

▼ソースコード
```node.js
// ライブラリ参照
var googlehome = require('./node_modules/google-home-notifier');
// 言語設定
var language = 'ja';
// GoogleHomeのIPアドレスに書き換えてくださいね
googlehome.ip('192.168.11.5');
// 第一引数を自分のもっているGoogleHomeの名前に書き換えてくださいね
googlehome.device('Google-Home-Mini', language);
// Google Homeにしゃべって欲しい文章をここに記入してくださいね
var text = 'ハッピーの餌やりを、記録しました';
// メイン処理
try {
// 実行
googlehome.notify(text, function(notifyRes) {
// ログ出力
console.log(notifyRes);
});
// エラー処理
} catch(err) {
// ログ出力
console.log(err);
}

```
▼参考サイト
https://rikei-life.com/raspberry-pi-google-home-how-to-speak/

https://rooter.jp/alexa/how-to-setup-google-home-notifier/


# 総括
簡単なようで、つまづきまくったので、初心者には厳しいと思われ。
