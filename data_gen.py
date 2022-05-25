# keras数据增强
from tensorflow.keras.preprocessing.image import ImageDataGenerator
datagen = ImageDataGenerator(
    featurewise_center=True,
    featurewise_std_normalization=True,
    rotation_range=40,#旋转
    width_shift_range=0.2,#水平平移
    height_shift_range=0.2,#垂直平移
    horizontal_flip=True,#随机水平翻转
    vertical_flip=True,#随机竖直翻转
    shear_range=0.2, # 随机错切换角度
    zoom_range=0.2, # 随机缩放范围
    zca_whitening = True,#白化
    fill_mode='nearest') # 填充新创建像素的方法

paths = [str(i) for i in range(15)]
for path in paths:
    gen = datagen.flow_from_directory("./U_data/",batch_size=5,save_to_dir='./U_data/'+path,
                                     classes=[path],save_prefix='gen',save_format='jpg')
    for i in range(10):
        gen.next()