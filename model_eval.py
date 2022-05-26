import os
import json

import cv2
import pandas as pd
import numpy as np

from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.applications import MobileNetV2
from tensorflow.python.keras import Sequential
from tensorflow.python.keras.layers import Dense
import tensorflow as tf

def eval_h5model():
    with open('config/config.json', 'r') as f:
        cfg = json.load(f)

    shape = (int(cfg['height']), int(cfg['width']), 3)
    n_class = int(cfg['class_number'])

    model = Sequential()
    model.add(MobileNetV2(input_shape=shape, include_top=False, pooling='avg', weights=None))
    model.add(Dense(n_class, activation='softmax'))

    model.load_weights('./save/Udun_weights_V1.h5', by_name=True)
    opt = Adam(lr=float(cfg['learning_rate']))
    model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])

    datagen = ImageDataGenerator(rescale=1. / 255)
    eval_generator = datagen.flow_from_directory(
        './U_data/test/',
        target_size=shape[:2],
        batch_size=16,
        class_mode='categorical')

    test_loss,test_acc = model.evaluate(eval_generator)

    test_img = cv2.imread('./U_data/test/3/25.jpg')
    test_img = cv2.resize(test_img,(224,224))
    test_img = np.expand_dims(test_img,axis=0)/255.0
    result = model.predict(test_img)
    print(np.max(result),np.argmax(result))

def eval_tflite(model_path):
    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    print(input_details)
    output_details = interpreter.get_output_details()
    print(output_details)

    test_path = './U_data/test/'
    classes = os.listdir(test_path)
    for i,clas in enumerate(classes):
        clas_path = os.path.join(test_path,clas)
        images = os.listdir(clas_path)
        for image in images:
            image_path = os.path.join(clas_path,image)
            x = cv2.imread(image_path)
            x = cv2.resize(x, (224, 224))
            x = np.expand_dims(x, axis=0) / 255.0
            x = np.array(x, dtype='float32')
            interpreter.set_tensor(input_details[0]['index'], x)

            interpreter.invoke()
            output_data = interpreter.get_tensor(output_details[0]['index'])

            print(clas,i,np.argmax(output_data, axis=1),np.max(output_data))



eval_tflite('./save/Udun_model_V1.tflite')
