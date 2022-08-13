---
title: Raspberry Pi で Android TV
date: "2022-08-13"
description: "話題のチューナーレスTVで使われているAndroid TV をRaspberry Pi で使う。"
---

# 使用機器
・Raspberry Pi 4<br>
・キーボード、マウス、モニタが必要<br>
<br>

# 必要ファイルのダウンロード
以下の2つをダウンロード<br/>
<br/>
LineageOS<br/>

|  https://konstakang.com/devices/rpi4/LineageOS18-ATV/<br/>
|  → Raspberry Pi Imager、Ether、ddなどでmicroSD に書き込む<br/>

参考：<br/>
![lieage osの場所の画像](where_lineage_os_is.png)
<br>

open_gapps<br/>

|  https://opengapps.org/?arch=arm64&api=11.0&variant=tvstock<br/>
|  → USBメモリなどに配置

>2022年8月13日現在、LineageOS 19 Android TV(Android 12L) は存在するが、Android 12Lに対応したopen_gappsはまだ存在しない。そのためLineageOS 18 Android TV(Android 11)を使用する。 
<br>
<br>

# 起動
LineageOSを書き込んだmicroSDをRaspberryPiに挿入して起動。最初はBluetooth機器のペアリングをさせられる。[^1]<br/>
手順（抜粋）<br/>
Start → ... → Language：Englishのままで[^1] → ... → Select Your Wifi Network：Skip → ...<br/>
大きく「Lineage」と表示されたら設定完了。右下の「Start」をクリック。<br/>

> [^1]：周辺のBluetooth機器は電源OFFにした方が良いかも。ペアリング成功するまで先に進めないっぽい。

> [^2]：言語、ロケール、wifiの設定などは今行っても無意味なので飛ばす。AndroidTV起動後に行えば良い。


# 操作方法
|  キー  |  概要  |
| ---- | ---- |
|  F2  | 戻る |
<br>
<br>

# リカバリモードでLineageOSを再起動
## advanced restart options（リカバリモード）を有効にする<br>
Settings（右上の歯車）→  System →  Buttons →  Advanced reboot
## リカバリモードで再起動
System に戻る →  Reboot → Recovery
<br>
<br>

# OpenGAppsのインストール
Install → Select Storage → 先程USBに保存したopen_gapps-arm64-11.0-tvstock-xxxxxxxx.zipを選択 → Swipe to confirm Flash（マウスでスマホ風にスワイプする）→<br>
インストール終了したら、Back →  Wipe →  Factory reset →  再起動<br>
再起動後はAndroid TVになっているはず。
<br>
<br>

# 資料
公式：https://konstakang.com/devices/rpi4/LineageOS18-ATV/<br>
→ 特に「How to install Google apps?」の情報
