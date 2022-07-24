---
title: スマートリモコン
date: "2022-07-19"
description: "スマートリモコンを実現する方法をいくつかまとめる。"
---
（編集中）

# 方法
| 方法 | 難易度 | 概要 |
| ---- | ---- | ---- |
| Nature Remo |  | 市販の製品を使う。 |
| M5 Stack  | 簡単 | ATOM Lite＋赤外線送受信ユニット |
| ラズパイ  | やや難 | ラズパイ+自作基盤 |
| ESP32 | やや難 | ESP32+自作基盤 |


# M5 Stack
## M5 Stack - ハードウェア
おすすめのM5 Stack（コンパクトで安い）
https://www.switch-science.com/catalog/6262/
<br/>
赤外線送受信ユニット
https://www.switch-science.com/catalog/5699/
（補足）「Grove互換コネクタ」付きのM5 Stack ならばなんでも良いらしい


# ラズパイ
## ラズパイ - ハードウェア

（参考）https://qiita.com/takjg/items/e6b8af53421be54b62c9

## 資料

（補足）ラズパイ用の「HAT」も存在するようだが値段が１万円くらいする。
Nature Remo miniが8千円くらいな事を考えると、微妙。
https://www.ratoc-e2estore.com/products/detail.php?product_id=78


# ESP32
## ESP32 - ハードウェア
ESP32は開発ボード（DevBoard）を選んで USB給電する事。
さもないと、電源、リセットボタンなどの対応が必要。その場合の難易度は「難」。
（参考）https://akizukidenshi.com/catalog/g/gM-15674/

## ESP32 - ソフトウェア

以下のURLから最新(latest) のIRremoteESP8266 をダウンロード
https://www.arduino.cc/reference/en/libraries/irremoteesp8266/

ArduinoStudioを起動<br/>
メニュー：スケッチ→ライブラリをインクルード→.zip形式のライブラリをインストール で先程のダウンロードした.zipファイルを選択

補足：ファイル → スケッチ例 → カスタムライブラリのスケッチ例 → IRremoteESP8266 にもいくつか例がある。
