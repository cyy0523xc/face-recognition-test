# -*- coding: utf-8 -*-
#
# 人脸统计
# Author: alex
# Created Time: 2018年11月23日 星期五 21时50分48秒
import cv2
from os import listdir
from datetime import datetime
import face_recognition as fr

faces = []
faces_count = []
new_face_files = []


def save_new_face(img, filename, locs):
    for i in locs:
        cv2.rectangle(img, (i[3],i[0]), (i[1],i[2]), color=(0,255,255),
                        thickness=3)
    cv2.imwrite('/tmp/'+filename, img)


def count(path, rate=10):
    """统计一个目录下的图片的人脸数量"""
    if not path.endswith('/'):
        path += '/'

    global faces, new_face_files, faces_count
    files = sorted(listdir(path))
    i = 0
    for f in files:
        i += 1
        if i % rate != 2:
            continue

        print(datetime.now(), f)
        img = fr.load_image_file(path+f)
        f_locations = fr.face_locations(img, model='cnn')
        # f_locations = fr.face_locations(img, number_of_times_to_upsample=0, model='cnn')
        if len(f_locations) == 0:
            # 没有识别到人脸
            faces_count.append((f, 0))
            continue

        encodings = fr.face_encodings(img, f_locations)
        f_count = len(encodings)
        faces_count.append((f, f_count))
        if f_count == 0:
            continue
        if len(faces) == 0:
            faces = encodings
            new_face_files.append(f)
            save_new_face(img, f, f_locations)
            continue
        has_new_face = False
        for e in encodings:
            match = fr.compare_faces(faces, e, tolerance=0.7)
            if match[0]:
                # 已经存在
                continue
            faces.append(e)
            new_face_files.append(f)
            has_new_face = True

        if has_new_face is False:
            continue
        save_new_face(img, f, f_locations)

    return len(faces)


if __name__ == '__main__':
    import sys
    print(count(sys.argv[1]))
    for i in faces_count:
        print(i)

    print(new_face_files)
