---
title: MQTT
date: "2022-07-18"
description: "MQTTの概要と具体的な利用方法"
---

# 概要
軽量なソケット通信プロトコル。<br>
通信ポート：TCP1883 TLS8883<br>
<br>
・送信者（Publisher）、受信者（Subscriber）、中継者（Broker）の３つでネットワークを構成。<br>
・Publisher→Broker→Subscriberとデータは送られる。<br>
・Brokerはクラウドサーバーが担う事が多い。（オンプレでも問題はない）<br>
・Publisherは送信先、Subscriberは送信元を<b>一切気にせずに通信を行う事ができる</b>のが特徴。<br>


# 用語
## Topic
メッセージ種別の識別子。「/」で区切られた階層構造。（例）sensor/temp<br>
Subscriberは受信したいトピックを指定することで、欲しいメッセージだけを手に入れることができる。<br>
> 例　sensor/# を指定するとsensor/temp, sensor/humid などを受信できるが camera/detectなどは受信しない。<br>
補足：「+」「#」はワイルドカードで、「+」が一階層のみ、「#」が複数階層。

## Retain
メッセージをBroker が保持しておく機能。<br>
例えば10分毎にPublishされる情報をSubscriberがいつでも取りに来られるようにする為の機能。<br>
（比較）QoS<br>

## QoS
通信品質。Subscriberに確実にメッセージを届ける為の機能。<br>
| 値 |  意味 |
| ---- | ---- |
| QoS0 | メッセージを受信の保証なしに送信。 |
| QoS1 | 受信の保証付きで送信。重複受信の可能性あり。 |
| QoS2 | M受信の保証付きで送信。重複受信の可能性なし。 |

> QoS0しか実装されていないBrokerも多いらしいので注意
（比較）Retain<br>
<br>
## Will
Publisherが通信ができなくなった時に指定メッセージを送信する機能。
<br>
<br>
# パッケージ

|  パッケージ名  |  概要  |
| ---- | ---- |
|  mosquitto  |  最も有名なMQTTブローカー  |
|  paho-mqtt  |  pythonでMQTTを使う際のライブラリ  |
|  MQTT.js  |  MQTTをhtml(JavaScript)で使う際のライブラリ  |



# mosquitto チュートリアル
インストール
```bash
sudo apt install mosquitto            # brokerのみ
sudo systemctl status mosquitto       # インストール確認（動作状況の確認）
sudo apt install mosquitto-clients    # mosquitto_sub、mosquitto_pubなど
```

サブスクライブ
```bash
mosquitto_sub -h localhost -t test/topic
```

パブリッシュ
```bash
mosquitto_pub -h localhost -t test/topic -m "Hello"
```


# mosquitto 外部からの接続
mosquitto は初期設定では外部からの接続が出来ない（許可されているのはlocalhostのみ）
他PCなどから接続する際には設定ファイルの変更が必要。<br>

[ etc/mosquitto/mosquitto.conf ]
```
listener 1883               # MQTTのポート（外部からの接続の際、必須）
listener 9001               # WebSocket用（任意）
listener 8883               # TLS接続用（任意）
protocol websockets

allow_anonymous true 		# パスワード認証しない場合はこれが必要
```

mosquittoデーモンの再起動
```bash
sudo systemctl restart mosquitto
```


# paho-mqtt チュートリアル
インストール
```bash
pip3 install paho-mqtt
```

[ mqtt_test.py（サンプル）]

```python
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    client.subscribe('test/topic')          # Subscribe開始

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))   # 受信メッセージのTopic と内容の表示

client = mqtt.Client()
client.on_connect = on_connect              # イベントの設定：接続時
client.on_message = on_message              # イベントの設定：メッセージ受信(Subscribe)
client.connect(host='localhost', port=1883, keepalive=60)
client.loop_forever()                       # 無限ループでメッセージを待機
```


# MQTT.js チュートリアル

ポイントは<br>
・Broker で WebSocket用の通信ポートを開く事。（今回の場合9001番）<br>
・プロトコルをws:（WebSocket）にする事。（Webブラウザでは直接MQTTプロトコルを扱えない）<br>

[ index.html @htmlサーバー]
```html
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <title>MQTT.js Test</title>
        <script src="https://unpkg.com/mqtt/dist/mqtt.min.js"></script>     <!-- ライブラリの読み込み --> 
    </head>
    <body>
        <script>
            var client = mqtt.connect('ws://192.168.1.1:9001');             // ソケット通信用のポートを選択する
            client.subscribe("test/topic");

            client.on('message', function (topic, message) {                // メッセージ受信イベント
                console.log(message.toString());
            });

            function OnButtonClick() {
                console.log('onClick');
                client.publish('test/topic', 'message from html!');         // 送信（Publish）
            }
        </script>
        <input type="button" value="Publish" onclick="OnButtonClick()"/><!--このボタンを押すとPublishする-->
    </body>
</html>
```


# ESP32での利用
以下のURLから最新(latest) のPubSubClient をダウンロード<br/>
https://www.arduino.cc/reference/en/libraries/pubsubclient/

ArduinoStudioを起動<br/>
メニュー：スケッチ→ライブラリをインクルード→.zip形式のライブラリをインストール で先程のダウンロードした.zipファイルを選択
<br/>
<br/>
[ Arduino Studioサンプルソース ]

```cpp
#include <MQTTClient.h>
#include "EspMQTTClient.h"

EspMQTTClient mqttClient(
  "YOUR_SSID",
  "PASSWORD",
  "192.168.1.1"           // Broker のIPアドレス
);

void setup() {
  Serial.begin(115200);
  delay(50);              // シリアルコンソールの起動を待機する(50mSec)
}

void onConnectionEstablished() {
  Serial.println("Connection Established.");
  
  mqttClient.subscribe("test/topic", [] (const String &payload)  {
    Serial.println(payload);
  });

  mqttClient.publish("test/topic", "message from ESP32!");
}

void loop() {
  mqttClient.loop();
}
```

> 補足：ファイル → スケッチ例 → カスタムライブラリのスケッチ例 → PubSubClient にもいくつか例がある。