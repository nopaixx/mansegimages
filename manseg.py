import os
import sys
import numpy as np
import cv2 as cv2
import matplotlib.pyplot as plt 
import traceback
from PIL import Image
import shutil

drawing=False
mode=True
def mask_image(file_orig, train_folder, mask_folder, name):
    print(file_orig)
    #    file_orig = 'sea.jpg'

    allpoints = []
    tmp_point = []  

    def draw(event,former_x,former_y,flags,param):
        global current_former_x,current_former_y,drawing, mode, init_x, init_y, tmp_point
        if event==cv2.EVENT_LBUTTONDOWN:
            drawing=True
            current_former_x,current_former_y=former_x,former_y
            init_x, init_y = former_x, former_y
            tmp_point = []
            tmp_point.append([init_x, init_y])
        elif event==cv2.EVENT_MOUSEMOVE:
            if drawing==True:
                if mode==True:
                    cv2.line(im,(current_former_x,current_former_y),(former_x,former_y),(0,0,255),5)
                    tmp_point.append([former_x, former_y])
                    current_former_x = former_x
                    current_former_y = former_y
        elif event==cv2.EVENT_LBUTTONUP:
            drawing=False
            if mode==True:
                cv2.line(im,(current_former_x,current_former_y),(former_x,former_y),(0,0,255),5)
                tmp_point.append([former_x, former_y])
                current_former_x = former_x
                current_former_y = former_y
                cv2.line(im,(current_former_x, current_former_y), (init_x, init_y),(0,0,255),5)
                tmp_point.append([init_x, init_y])
                allpoints.append(tmp_point)

        return former_x, former_y


    im = cv2.imread(file_orig)
    cv2.namedWindow("image", cv2.WINDOW_NORMAL)
    cv2.setMouseCallback('image',draw)

    while(1):
        cv2.imshow('image',im)
        cv2.resizeWindow('image', 1200,1200)
        k=cv2.waitKey(1)&0xFF
        if k==27:
            sys.exit()
        if k==ord('q'):
            break
        elif k==ord('z'):
            alllines = []
            im = cv2.imread(file_orig)

    img = np.zeros( (im.shape[0],im.shape[1],3) )
    for points in allpoints:
        contours = np.array(points)
        cv2.fillPoly(img, pts =[contours], color=(255,255,255))

    cv2.imwrite(mask_folder+name,img)
    os.rename(file_orig, train_folder+name)

if __name__ == '__main__':

    orig_folder = os.listdir(sys.argv[1])
    train_folder = sys.argv[2]
    mask_folder = sys.argv[3]
    current_dir = os.getcwd()
    for file_orig in orig_folder:
        try:
            mask_image(current_dir+'/'+sys.argv[1]+'/'+file_orig, 
                       current_dir+'/'+train_folder+'/',
                       current_dir+'/'+mask_folder+'/',
                       file_orig)
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            print(e)
