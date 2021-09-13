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
```
yukiyoshi1992@raspberrypi:~ $ sudo su
root@raspberrypi:/home/yukiyoshi1992# sudo echo 18 > /sys/class/gpio/export
root@raspberrypi:/home/yukiyoshi1992# sudo echo in > /sys/class/gpio/gpio18/dire           ction
root@raspberrypi:/home/yukiyoshi1992#
```

catで確認したとき、1なら検知できている。
```
root@raspberrypi:/home/yukiyoshi1992# cat /sys/class/gpio/gpio18/value
1
```
## プログラムを組んで見る





