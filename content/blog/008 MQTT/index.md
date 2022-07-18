---
title: MQTT
date: "2022-07-18"
description: "MQTTの概要と具体的な利用方法"
---

# 概要
軽量なソケット通信プロトコル。
通信ポート：TCP1883 TLS8883

・送信者（Publisher）、受信者（Subscriber）、中継者（Broker）の３つでネットワークを構成。
・Publisher→Broker→Subscriberとデータは送られる。
・Brokerはクラウドサーバーが担う事が多い。（オンプレでも問題はない）
・Publisherは送信先、Subscriberは送信元を--一切気にせずに通信を行う事ができる--のが特徴。


# 用語
## 

## Topic
メッセージ種別の識別子。「/」で区切られた階層構造。（例）sensor/temp
Subscriberは受信したいトピックを指定することで、欲しいメッセージだけを手に入れることができる。
（例）sensor/ を指定するとsensor/temp, sensor/humid などを受信できるが camera/detectなどは受信しない。

## Retain
メッセージをMQTTサーバーが保持しておく機能。
例えば10分毎にPublish更新される情報をSubscriberがいつでも取りに来られるようにする為の機能。
（比較）QoS

## QoS
通信品質。Subscriberに確実にメッセージを届ける為の機能。
(QoS0しか実装されていないBrokerも多いらしいので注意)
0	メッセージを受信の保証なしに送信。
1	受信の保証付きで送信。重複受信の可能性あり。
2	受信の保証付きで送信。重複受信の可能性なし。
（比較）Retain

## Will
Publisherが通信ができなくなった時に指定メッセージを送信する機能。


# パッケージ
mosquito    最も有名なMQTTブローカー
MQTT.js     MQTTをWeb(JavaScript)で使う際のライブラリ


# mosquitto チュートリアル
インストール
```bash
sudo apt install mosquitto            # brokerのみ
sudo systemctl status mosquitto       # インストール確認（動作状況の確認）
sudo apt install mosquitto-clients    # mosquitto_sub、mosquitto_pubなど
```

サブスクライブ
```bash
mosquitto_sub -h localhost -t sub
```

パブリッシュ
```bash
mosquitto_pub -t test -m "Hello"
```
