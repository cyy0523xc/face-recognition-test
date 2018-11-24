# -*- coding: utf-8 -*-
#
# 视频截图
# Author: alex
# Created Time: 2018年11月23日 星期五 22时34分18秒
import cv2
from os import makedirs


def cut(path, save_path, time_freq=100):
    vc = cv2.VideoCapture(path)
    if vc.isOpened() is False:
        raise Exception('视频文件打开失败')
    rval, frame = vc.read()
    if not save_path.endswith('/'):
        save_path += '/'

    c = 1
    while rval:
        rval, frame = vc.read()
        if c % time_freq == 0:
            cv2.imwrite(save_path + '%08d.jpg' % c, frame)

        c += 1
        cv2.waitKey(1)

    vc.release()


if __name__ == '__main__':
    v_path = '/var/www/tmp/faces/20180109-1-053700053162-506-1354-201801090000000563-2.mp4'
    save_path = '/var/www/tmp/faces/detect-label'
    makedirs(save_path, exist_ok=True)
    cut(v_path, save_path)
