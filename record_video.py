# -*- coding: utf-8 -*-
#
# 从源视频中录制一段视频
# Author: alex
# Created Time: 2018年11月26日 星期一 22时13分02秒
import cv2


def record(path):

    capture = cv2.VideoCapture(path)
    fps = capture.get(cv2.CAP_PROP_FPS)
    ret, frame = capture.read()

    i = 0
    print(fps)
    VideoWriter = cv2.VideoWriter(
        "./overwatch.avi",
        cv2.VideoWriter_fourcc('X', 'V', 'I', 'D'), fps,
        (frame.shape[1], frame.shape[0]))
    while i < fps * 30:
        i += 1
        ret, prev = capture.read()
        if ret is True:
            VideoWriter.write(prev)
        else:
            break

    VideoWriter.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    record('/var/www/tmp/faces/v01.mp4')
