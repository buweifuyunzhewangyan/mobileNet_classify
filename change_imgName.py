'''
修改图像名称，确保使用cv2读取是不会出现none的情况
'''

import os

data_dir = './U_data/test/'
classes = os.listdir(data_dir)
i = 0
for clas in classes:
    clas_path = os.path.join(data_dir,clas)
    images = os.listdir(clas_path)
    for image in images:
        image_path = os.path.join(clas_path,image)
        if '_nobg' not in image:
            new_image = str(i) + '.' + image.split('.')[-1]
            new_image_path = os.path.join(clas_path,new_image)
            os.rename(image_path,new_image_path)
        else:
            new_image = str(i) + '_nobg.' + image.split('.')[-1]
            new_image_path = os.path.join(clas_path, new_image)
            os.rename(image_path, new_image_path)
        i+=1
