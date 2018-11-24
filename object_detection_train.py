# -*- coding: utf-8 -*-
#
# 对象检测模型训练
# Author: alex
# Created Time: 2018年11月24日 星期六 10时02分30秒
from imageai.Prediction.Custom import ModelTraining

model_trainer = ModelTraining()
model_trainer.setModelTypeAsResNet()
model_trainer.setDataDirectory("/var/www/tmp/faces/model")
model_trainer.trainModel(num_objects=3,
                         num_experiments=30,
                         enhance_data=True,
                         batch_size=8,
                         show_network_summary=True)
