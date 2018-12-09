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
    files = []
    for fn in filenames:
        if fn.endswith(('jpg', 'jpeg', 'png')) is False:
            continue
        image = cv2.imread(os.path.join(path, fn))
        locations = face_detect(image)
        if len(locations) > 0:
            confidences = [i[0] for i in locations]
            files.append((fn, locations, max(confidences)))

    files = sorted(files, key=lambda x: x[2], reverse=True)[:5]
    for fn, locations, _ in files:
        print(fn, locations)
        image = cv2.imread(os.path.join(path, fn))
        show_image(image, locations)


def face_detect(image):
    cols = image.shape[1]
    rows = image.shape[0]

    net.setInput(dnn.blobFromImage(image, 1.0, (inWidth, inHeight),
                                   (104.0, 177.0, 123.0), False, False))
    detections = net.forward()

    perf_stats = net.getPerfProfile()
    print('Inference time, ms: %.2f' % (perf_stats[0] / cv2.getTickFrequency() * 1000))

    locations = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence < confThreshold:
            continue
        left = int(detections[0, 0, i, 3] * cols)
        top = int(detections[0, 0, i, 4] * rows)
        right = int(detections[0, 0, i, 5] * cols)
        bottom = int(detections[0, 0, i, 6] * rows)
        locations.append([confidence, (left, top), (right, bottom)])

    return locations


def show_image(image, locations, wait=0):
    for confidence, (left, top), (right, bottom) in locations:
        cv2.rectangle(image, (left, top),
                      (right, bottom), (0, 255, 0))
        label = "face: %.4f" % confidence
        labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX,
                                              0.5, 1)

        cv2.rectangle(image, (left, top - labelSize[1]),
                      (left + labelSize[0], top + baseLine),
                      (255, 255, 255), cv2.FILLED)
        cv2.putText(image, label, (left, top),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))

    cv2.imshow("dnn-detect", image)
    cv2.waitKey(0)


if __name__ == '__main__':
    import sys
    path_detect(sys.argv[1])
