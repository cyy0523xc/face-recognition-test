# -*- coding: utf-8 -*-
#
# 对象检测
# Author: alex
# Created Time: 2018年11月24日 星期六 10时01分39秒
from imageai.Prediction.Custom import CustomImagePrediction

output_path = '/tmp/'
json_path = '/var/www/tmp/faces/model/json/model_class.json'
model_path = '/var/www/tmp/faces/model/models/model_ex-100_acc-0.250000.h5'

detector = CustomImagePrediction()
detector.setModelTypeAsResNet()

# 载入已训练好的文件
print('Load model...')
detector.setModelPath(model_path)
detector.setJsonPath(json_path)
detector.loadModel(num_objects=3)
print('Load model end!')


def detect(path):
    # 将检测后的结果保存为新图片
    print('Input File: ', path)
    predictions, probabilities = detector.predictImage(path, result_count=5)

    for eachPrediction, eachProbability in zip(predictions, probabilities):
        print(eachPrediction + " : " + eachProbability)


if __name__ == '__main__':
    import sys
    detect(sys.argv[1])
