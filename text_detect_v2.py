# -*- coding: utf-8 -*-
#
# 文本模块提取（效果太差）
# Author: alex
# Created Time: 2018年11月24日 星期六 11时50分50秒
import sys
import cv2
import matplotlib.pyplot as plt

def detect(path):
    img = cv2.imread(path)
    mser = cv2.MSER_create(_min_area=300)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    regions, boxes = mser.detectRegions(gray)

    for box in boxes:
        x, y, w, h = box
        cv2.rectangle(img, (x,y),(x+w, y+h), (255, 0, 0), 2)

    plt.imshow(img, 'brg')
    plt.show()


if __name__ == '__main__':
    path = sys.argv[1]
    detect(path)
