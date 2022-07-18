---
title: MQTT
date: "2022-07-18"
description: "MQTTの概要と具体的な利用方法"
---

# 概要
（編集中）

# チュートリアル
インストール
```bash
sudo apt install mosquitto            # brokerのみ
sudo systemctl status mosquitto       # インストール確認（動作状況の確認）
sudo apt install mosquitto-clients    # mosquitto_sub、mosquitto_pubなど
```


```bash
mosquitto_sub -h localhost -t sub
```
