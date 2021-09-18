---
title: 人感センサを使ってみる（Raspi）
date: "2021-09-13"
description: "Rasberry PIで人感センサを使ってみる"
---

## 目次

```toc
# 目次はここに追加されます。
```

***
<br>

## 準備物

- Rasberry Pi zero WH
- 人感センサ
  焦電型赤外線センサーモジュール SB612A（秋月電子）
- 導線
  メス－メス　３本

## 人感センサの接続

このサイトが参考になる。
https://portaltan.hatenablog.com/entry/2018/05/16/094219


### 接続テスト
スーパーユーザで実行が必要
```Bash
sudo su
sudo echo 18 > /sys/class/gpio/export
sudo echo in > /sys/class/gpio/gpio18/direction
```

catで確認したとき、1なら検知できている。

```Bash
cat /sys/class/gpio/gpio18/value
1
```


## GOOGLE SPREAD SHEET に記録する

### GOOGLE SPREAD SHEET を準備

Spread Sheet のスクリプトエディタで、データを受けてSpread Sheetに書き込むプログラムを作る。

```javascript

function doGet(e) {

  //データを受信する（人感センサの状態を受け取る）
  var sensing = e.parameter.sensing;

  //現状Activeになっているsheetを取得
  var sheet = SpreadsheetApp.getActiveSheet();
 
  //現在日時をspreadsheetへ書き込み
  sheet.appendRow([new Date(),sensing]);
}

```

WEBアプリとしてデプロイ

参考サイト
https://monomonotech.jp/kurage/raspberrypi/google_spreadsheet.html

### プログラムを準備

```python

```

参考サイト
https://portaltan.hatenablog.com/entry/2018/05/16/094219

