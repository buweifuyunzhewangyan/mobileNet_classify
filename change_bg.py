'''
将扣出来的object，替换不同的背景，进行数据增强
'''

import glob
import os
import cv2
from imgaug import augmenters as iaa
import numpy as np
from PIL import Image
import random
from math import *

from tqdm import tqdm


def add_alpha_channel(img):
    """ 为jpg图像添加alpha通道 """

    b_channel, g_channel, r_channel = cv2.split(img)  # 剥离jpg图像通道
    alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 255  # 创建Alpha通道

    img_new = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))  # 融合通道
    return img_new


def merge_img(jpg_img, png_img, y1, y2, x1, x2):
    """ 将png透明图像与jpg图像叠加
        y1,y2,x1,x2为叠加位置坐标值
    """

    # 判断jpg图像是否已经为4通道
    if jpg_img.shape[2] == 3:
        jpg_img = add_alpha_channel(jpg_img)

    '''
    当叠加图像时，可能因为叠加位置设置不当，导致png图像的边界超过背景jpg图像，而程序报错
    这里设定一系列叠加位置的限制，可以满足png图像超出jpg图像范围时，依然可以正常叠加
    '''
    yy1 = 0
    yy2 = png_img.shape[0]
    xx1 = 0
    xx2 = png_img.shape[1]

    if x1 < 0:
        xx1 = -x1
        x1 = 0
    if y1 < 0:
        yy1 = - y1
        y1 = 0
    if x2 > jpg_img.shape[1]:
        xx2 = png_img.shape[1] - (x2 - jpg_img.shape[1])
        x2 = jpg_img.shape[1]
    if y2 > jpg_img.shape[0]:
        yy2 = png_img.shape[0] - (y2 - jpg_img.shape[0])
        y2 = jpg_img.shape[0]

    # 获取要覆盖图像的alpha值，将像素值除以255，使值保持在0-1之间
    alpha_png = png_img[yy1:yy2, xx1:xx2, 3] / 255.0
    alpha_jpg = 1 - alpha_png

    # 开始叠加
    for c in range(0, 3):
        jpg_img[y1:y2, x1:x2, c] = ((alpha_jpg * jpg_img[y1:y2, x1:x2, c]) + (alpha_png * png_img[yy1:yy2, xx1:xx2, c]))

    return jpg_img


def cover(img, degree):
    """ 旋转图像
    """
    img = np.array(img)
    height, width = img.shape[:2]

    # 旋转后的尺寸
    heightNew = int(width * fabs(sin(radians(degree))) + height * fabs(cos(radians(degree))))
    widthNew = int(height * fabs(sin(radians(degree))) + width * fabs(cos(radians(degree))))

    matRotation = cv2.getRotationMatrix2D((width / 2, height / 2), degree, 1)
    matRotation[0, 2] += (widthNew - width) / 2  # 重点在这步，目前不懂为什么加这步
    matRotation[1, 2] += (heightNew - height) / 2  # 重点在这步

    imgRotation = cv2.warpAffine(img, matRotation, (widthNew, heightNew), borderValue=(255, 255, 255))

    return imgRotation


def Contrast_and_Brightness(alpha, beta, img):
    '''调节对比度和亮度
    '''
    blank = np.zeros(img.shape, img.dtype)
    # dst = alpha * img + beta * blank
    dst = cv2.addWeighted(img, alpha, blank, 1 - alpha, beta)
    return dst

def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized


def create_newpic(folder_path,path_list,num_needed,back_num,U_gen_num):
    '''
    folder_path = './data/'#数据根目录
    path_list = list(range(19))#需要替换背景的类别列表
    num_needed = 60  #需要的图像张数
    back_num = 10    #用到随机背景的数量
    U_gen_num 每一张图像增强的次数

    输出：
    新的图像会自动输出到图像原目录下，自动添加后缀
    '''

    for path in tqdm(path_list):
        currency_folder_path = folder_path+str(path)+'/'
        back_folder = './background/'
        result_path = folder_path+str(path)+'/'

        #最后生成图像数量为：原始图像数*U_gen_num*back_num
        create_num = 0
        for image_name in os.listdir(currency_folder_path):
            if create_num>=num_needed:
                break
            if '_nobg' in image_name:
                image_path = os.path.join(currency_folder_path, image_name)

                name = os.path.basename(image_path)[:-4]
                images = cv2.imread(image_path,cv2.IMREAD_UNCHANGED)
                if images.shape[2]==3:
                    images = add_alpha_channel(images) #添加alpha通道

                images = [images] * U_gen_num
                images_aug = []# 应用数据增强
                for image in images:
                    degree = random.randint(0,365)
                    alpha = random.uniform(0.8,2)
                    beta = random.uniform(0.8,2)
                    image_aug = cover(image,degree)
                    image_aug = Contrast_and_Brightness(alpha, beta, image_aug)
                    images_aug.append(image_aug)

                n = 1
                for each in images_aug:
                    if create_num >= num_needed:
                        break
                    h,w,_ = each.shape
                    max_edge = max(h, w)
                    min_edge = min(h, w)
                    temp_img = np.zeros((max_edge, max_edge, 3), np.uint8)
                    for back_name in random.sample(os.listdir(back_folder),back_num):
                        back_path = os.path.join(back_folder, back_name)
                        back_img = cv2.imdecode(np.fromfile(back_path, dtype=np.uint8), 1)
                        back_img = add_alpha_channel(back_img) #添加alpha通道

                        back_resize_img = cv2.resize(back_img,(max_edge,max_edge),interpolation=cv2.INTER_CUBIC)

                        alpha = random.uniform(0.55,0.8) #控制图像缩放比例[0.3-0.8]
                        alpha_w = int(alpha*w)
                        alpha_h = int(alpha*h)
                        each = cv2.resize(each,(alpha_w,alpha_h),interpolation=cv2.INTER_CUBIC)

                        random_x = random.randint(0,max_edge-alpha_w) #控制x方向随机位置
                        random_y = random.randint(0,max_edge-alpha_h) #控制y方向随机位置

                        #开始融合
                        back_resize_img = merge_img(back_resize_img, each, random_y,alpha_h+random_y, random_x,alpha_w+random_x)

                        resize_img = image_resize(back_resize_img,height = 224)
                        save_path = os.path.join(result_path, '%s_%s.png'%(name,n))
                        cv2.imwrite(save_path,resize_img)
                        n += 1
                        create_num+=1
                        if create_num >= num_needed:
                            break

if __name__ == '__main__':
    folder_path = './U_data/'
    path_list = list(range(14))
    num_needed = 60
    back_num = 15
    U_gen_num = 5
    create_newpic(folder_path, path_list, num_needed, back_num,U_gen_num)