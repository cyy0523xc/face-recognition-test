# -*- coding: utf-8 -*-
#
# 视频截图
# Author: alex
# Created Time: 2018年11月23日 星期五 22时34分18秒
import cv2
from os import makedirs


def cut(path, save_path, time_freq=1):
    vc = cv2.VideoCapture(path)
    if vc.isOpened() is False:
        raise Exception('视频文件打开失败')
    rval, frame = vc.read()
    if not save_path.endswith('/'):
        save_path += '/'

    c = 1
    total_img = 0
    mod = int(vc.get(cv2.CAP_PROP_FPS)) * time_freq
    if mod < 2:
        mod = 2

    while rval:
        rval, frame = vc.read()
        if c % mod == 0:
            total_img += 1
            cv2.imwrite(save_path + '%08d.jpg' % c, frame)

        c += 1
        cv2.waitKey(1)

    print("Total Frame: ", c)
    print("Total Image: ", total_img)
    vc.release()


if __name__ == '__main__':
    v_path = '/var/www/tmp/faces/v01.mp4'
    save_path = '/var/www/tmp/faces/detect-label'
    makedirs(save_path, exist_ok=True)
    cut(v_path, save_path)
