---
title: ArUcoタグ
date: "2022-11-29"
description: "OpenCV で ArUco マーカーを扱う"
---

# 概要

# マーカーの作成

[create_markers.py]<br>
```python
# pip でインストールが必要なもの
import cv2
import numpy as np

aruco = cv2.aruco

def create_single_markers():
    '''
    １枚ずつマーカー画像ファイルを作成します。
    '''
    dictionary  = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)

    for i in range(30):
        marker = aruco.drawMarker(dictionary , i, 75) # 75x75 px
        cv2.imwrite(f'marker{i}.png', marker)

def create_markers():
    '''
    複数のマーカーを１枚の画像ファイルに作成します。
    '''
    dictionary  = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)

    # 空の画像データを作成
    frame = np.ones((600, 500), np.uint8) * 255

    for i in range(30):
        # 第3 引数で画像サイズを指定する（らしい）
        marker = aruco.drawMarker(dictionary , i, 75) # 75x75 px
        
        # マーカーの幅、高さの取得
        h, w = marker.shape

        # 座標作成
        x_min, y_min = int(i%5 * 100), int(i/5) * 100
        x_max, y_max= x_min+w, y_min+h

        # 色々確認
        # print('counter:%i x:%i y:%i' % (i,x_min,y_min))

        # ROI [縦の範囲, 横の範囲] で指定（スライス）
        frame[y_min:y_max, x_min:x_max]=marker
    
    # 静止画の保存
    cv2.imwrite('markers.png', frame)


if __name__ == '__main__':
    # create_single_markers()
    create_markers()
```


