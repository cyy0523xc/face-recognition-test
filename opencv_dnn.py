# -*- coding: utf-8 -*-
#
#
# Author: alex
# Created Time: 2018年12月08日 星期六 22时16分15秒
import os
import cv2
from cv2 import dnn

inWidth = 400
inHeight = 400
confThreshold = 0.5

prototxt = 'data/deploy.prototxt'
caffemodel = 'data/res10_300x300_ssd_iter_140000.caffemodel'
net = dnn.readNetFromCaffe(prototxt, caffemodel)


def path_detect(path):
    filenames = sorted(os.listdir(path))
    for fn in filenames:
        if fn.endswith(('jpg', 'jpeg', 'png')) is False:
            continue
        print("===> ", fn)
        image = cv2.imread(os.path.join(path, fn))
        face_detect(image)


def face_detect(image):
    cols = image.shape[1]
    rows = image.shape[0]

    net.setInput(dnn.blobFromImage(image, 1.0, (inWidth, inHeight),
                                   (104.0, 177.0, 123.0), False, False))
    detections = net.forward()

    perf_stats = net.getPerfProfile()
    print('Inference time, ms: %.2f' % (perf_stats[0] / cv2.getTickFrequency() * 1000))

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence < confThreshold:
            continue
        xLeftBottom = int(detections[0, 0, i, 3] * cols)
        yLeftBottom = int(detections[0, 0, i, 4] * rows)
        xRightTop = int(detections[0, 0, i, 5] * cols)
        yRightTop = int(detections[0, 0, i, 6] * rows)

        cv2.rectangle(image, (xLeftBottom, yLeftBottom),
                      (xRightTop, yRightTop), (0, 255, 0))
        label = "face: %.4f" % confidence
        print(label)
        labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX,
                                              0.5, 1)

        cv2.rectangle(image, (xLeftBottom, yLeftBottom - labelSize[1]),
                      (xLeftBottom + labelSize[0], yLeftBottom + baseLine),
                      (255, 255, 255), cv2.FILLED)
        cv2.putText(image, label, (xLeftBottom, yLeftBottom),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))

    cv2.imshow("dnn-detect", image)
    cv2.waitKey(0)


if __name__ == '__main__':
    import sys
    path_detect(sys.argv[1])
