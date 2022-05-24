import os

base_path = './data/'
classes = range(20)
classes = [str(i) for i in classes]
for clas in classes:
    class_path = os.path.join(base_path,clas)
    pics = os.listdir(class_path)
    for pic in pics:
        print(clas+'_'+pic)
        pic_path = os.path.join(class_path,pic)
        out_pic_path = os.path.join(class_path,pic[0:-4]+'_nobg'+pic[-4:])
        os.system('backgroundremover -i %s -o %s' % (pic_path,out_pic_path))