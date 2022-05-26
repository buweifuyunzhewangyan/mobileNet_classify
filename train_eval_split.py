import shutil
import os
import random

classes_path = './U_data/train/'
classes = os.listdir('./U_data/train/')

for clas in classes:
    clas_path = os.path.join(classes_path, clas)
    pic_list = os.listdir(clas_path)
    eval_num = int(len(pic_list) * 0.2)
    eval_path = './U_data/eval/' + clas + '/'

    while os.path.exists(eval_path) == 0:  # 判断括号里的文件是否存在
        os.mkdir(eval_path)  # 创建文件夹
        print(eval_path)

    for pic in random.sample(pic_list, eval_num):
        pic_path = os.path.join(clas_path, pic)
        shutil.move(pic_path, eval_path)  # 原文件夹路径、目标文件夹路径