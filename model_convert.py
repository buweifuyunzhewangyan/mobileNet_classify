import json

import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.python.keras import Sequential
from tensorflow.python.keras.layers import Dense

def convertModel():
    with open('config/config.json', 'r') as f:
        cfg = json.load(f)

    shape = (int(cfg['height']), int(cfg['width']), 3)
    n_class = int(cfg['class_number'])

    model = Sequential()
    model.add(MobileNetV2(input_shape=shape, include_top=False, pooling='avg', weights=None))
    model.add(Dense(n_class, activation='softmax'))

    model.load_weights('./save/Udun_weights_V1.h5', by_name=True)

    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = converter.convert()
    open("./save/Udun_model_V1.tflite", "wb").write(tflite_model)

convertModel()
