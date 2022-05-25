'''https://github.com/nadermx/backgroundremover'''

'''
1、安装backgroundremover库
2、去除图像背景
'''

import os

base_path = './U_data/'
classes = range(14)
classes = ['0']
for clas in classes:
    class_path = os.path.join(base_path,clas)
    pics = os.listdir(class_path)
    for pic in pics:
        print(clas+'_'+pic)
        pic_path = os.path.join(class_path,pic)
        out_pic_path = os.path.join(class_path,pic[0:-4]+'_nobg'+pic[-4:])
        os.system('backgroundremover -i %s -o %s' % (pic_path,out_pic_path))