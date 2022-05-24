import time

from removebg import RemoveBg
import os

rmbg = RemoveBg("CS6cZssthG3qTMobnQ7LYeWy", "error.log")
base_path = './data/'
classes = [9,10]
classes = [str(i) for i in classes]
for clas in classes:
    class_path = os.path.join(base_path,clas)
    pics = os.listdir(class_path)
    for pic in pics:
        print(clas+'_'+pic)
        pic_path = os.path.join(class_path,pic)
        time.sleep(10)
        rmbg.remove_background_from_img_file(pic_path)