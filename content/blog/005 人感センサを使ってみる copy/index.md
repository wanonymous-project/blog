---
title: 人感センサを使ってみる
date: "2021-09-13"
description: "ESP32と人感センサを使ってみる"
---

## 目次

```toc
# 目次はここに追加されます。
```

***
<br>

## 準備物

- ESP32 開発ボード
- 人感センサ
    焦電型赤外線センサーモジュール SB612A（秋月電子）
- 導線
    メス－メス　３本

## 開発環境準備

### Arduino IDE 整備
Arduino IDE環境をインストールし、Arduino core for the ESP32を導入する。
https://www.mgo-tec.com/arduino-core-esp32-install

### ESP32 WIFI設定

SimpleWiFiServerスケッチに、SSIDとPWを書き込む

>Wi-Fiに接続するスケッチ例は接続の方法や用途によって何種類かあるみたい。ボードで"ESP32 Dev Module"を選択していると「ファイル」の「スケッチ例」に"ESP32 Dev Module用のスケッチ例"という項目があって、そこの「WiFi」の中に「SimpleWiFiServer」というスケッチがあるのでこれを使います。

https://miraluna.hatenablog.com/entry/esp32_wifi_setuzoku

## 接続エラーより、断念

残念、無念、また来年。
https://discord.com/channels/849944957446783027/886047311963254835/886879218561073174

## モジュールの接続方法
https://qiita.com/Tsukkey/items/55d4ec1365a980565454


