#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 30 15:12:30 2022

@author: ftan1

modified from https://www.codetd.com/en/article/6571119
"""
import cv2
import numpy as np
import matplotlib.pyplot as plt

def draw_roi(event, x, y, flags, param):
    '''
    Mouse event function

    '''
    img2 = img.copy()
    pts = param
    
    # left click add vertices / points
    if event == cv2.EVENT_LBUTTONDOWN:
        pts.append((x, y))  
    
    # right click delete previous vertex / point
    if event == cv2.EVENT_RBUTTONDOWN:
        pts.pop()  
    
    # middle click draw roi
    # if event == cv2.EVENT_MBUTTONDOWN:
    #     mask = np.zeros(img.shape, np.uint8)
    #     points = np.array(pts, np.int32)
    #     points = points.reshape((-1, 1, 2))

    #     mask = cv2.polylines(mask, [points], True, (255, 255, 255), 2)
    #     mask2 = cv2.fillPoly(mask.copy(), [points], (255, 255, 255))
    #     mask3 = cv2.fillPoly(mask.copy(), [points], (0, 255, 0))

    #     show_image = cv2.addWeighted(src1=img, alpha=0.8, src2=mask3, beta=0.2, gamma=0)

    #     cv2.imshow("mask", mask2)
    #     cv2.imshow("show_img", show_image)

    #     ROI = cv2.bitwise_and(mask2, img)
    #     cv2.imshow("ROI", ROI)
    #     cv2.waitKey(0)

    if len(pts) > 0:
        cv2.circle(img2, pts[-1], 1, (255, 0, 0), -1)

    if len(pts) > 1:
        for i in range(len(pts) - 1):
            cv2.circle(img2, pts[i], 1, (255, 0, 0), -1)
            cv2.line(img=img2, pt1=pts[i], pt2=pts[i + 1], color=(255, 0, 0), thickness=1)

    cv2.imshow('image', img2)

def poly_roi(img, value=1):
    '''
    Draw polygon ROI on image and assign value 

    Parameters
    ----------
    img : numpy array
        2D image for ROI drawing.
    value : IND, optional
        value assigned to the ROI. The default is 1.

    Returns
    -------
    mask : numpy array
        2D polygon ROI.

    '''
    # list to store points
    pts = []
    
    # show image
    cv2.namedWindow('image', cv2.WINDOW_AUTOSIZE)
    cv2.moveWindow('image', 800, 500)
    cv2.imshow('image', img)
    
    # catch mouse click
    cv2.setMouseCallback('image', draw_roi, pts)
    
    # Esc to exit, 's' to save ROI
    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            break
        if key == ord("s"):
            # convert points to ROI mask
            mask = np.zeros(img.shape, np.uint8)
            points = np.array(pts, np.int32)
            points = points.reshape((-1, 1, 2))
            mask = cv2.fillPoly(mask, [points], (value, value, value))
            break
    cv2.destroyAllWindows()
    return mask

if __name__ =='__main__':
    img_path_list = [ 
    # '/data/larson4/UTE_Lung/2018-06-05_pat/cfl/P12800/xdgrasp.npy',
    # '/data/larson4/UTE_Lung/2018-08-08_pat/cfl/P49152/xdgrasp.npy',
    # '/data/larson4/UTE_Lung/2018-09-05_pat1/cfl/P45568/xdgrasp.npy',
    # '/data/larson4/UTE_Lung/2018-10-26_pat/cfl/P15872/xdgrasp.npy',
    # '/data/larson4/UTE_Lung/2019-02-15_pat/cfl/P13312/xdgrasp.npy',
    # '/data/larson4/UTE_Lung/2019-03-07_pat/cfl/P35840/xdgrasp.npy',
    # '/data/larson4/UTE_Lung/2019-03-25_pat/cfl/P86528/xdgrasp.npy',
    '/data/larson4/UTE_Lung/2019-04-10_pat/cfl/P62464/xdgrasp.npy',
    '/data/larson4/UTE_Lung/2019-05-29_pat/cfl/P21504/xdgrasp.npy',
    '/data/larson4/UTE_Lung/2020-01-09_pat/cfl/P05120/xdgrasp.npy',
    '/data/larson4/UTE_Lung/2021-03-15_pat/cfl/P43008/xdgrasp.npy',
    '/data/larson4/UTE_Lung/2021-04-06_pat/cfl/P37888/xdgrasp.npy',
    '/data/larson4/UTE_Lung/2021-04-12_pat/cfl/P12800/xdgrasp.npy',
    '/data/larson4/UTE_Lung/2021-04-19_pat/cfl/P00512/xdgrasp.npy',
    # '/data/larson4/UTE_Lung/2021-11-16_pat/cfl/P71168/xdgrasp.npy',
    '/data/larson4/UTE_Lung/2022-04-21_pat/cfl/xdgrasp.npy',
    '/data/larson4/UTE_Lung/2022-04-22_pat/cfl/P15872/xdgrasp.npy',
    '/data/larson4/UTE_Lung/2022-05-20_pat/cfl/P31232/xdgrasp.npy',
    '/data/larson4/UTE_Lung/2022-06-14_pat/cfl/P63488/xdgrasp.npy',
    
    ]

    roi_dir_list = [ 
    # '/data/larson4/UTE_Lung/2018-06-05_pat/seg/P12800/',
    # '/data/larson4/UTE_Lung/2018-08-08_pat/seg/P49152/',
    # '/data/larson4/UTE_Lung/2018-09-05_pat1/seg/P45568/',
    # '/data/larson4/UTE_Lung/2018-10-26_pat/seg/P15872/',
    # '/data/larson4/UTE_Lung/2019-02-15_pat/seg/P13312/',
    # '/data/larson4/UTE_Lung/2019-03-07_pat/seg/P35840/',
    # '/data/larson4/UTE_Lung/2019-03-25_pat/seg/P86528/',
    '/data/larson4/UTE_Lung/2019-04-10_pat/seg/P62464/',
    '/data/larson4/UTE_Lung/2019-05-29_pat/seg/P21504/',
    '/data/larson4/UTE_Lung/2020-01-09_pat/seg/P05120/',
    '/data/larson4/UTE_Lung/2021-03-15_pat/seg/P43008/',
    '/data/larson4/UTE_Lung/2021-04-06_pat/seg/P37888/',
    '/data/larson4/UTE_Lung/2021-04-12_pat/seg/P12800/',
    '/data/larson4/UTE_Lung/2021-04-19_pat/seg/P00512/',
    # '/data/larson4/UTE_Lung/2021-11-16_pat/seg/P71168/',
    '/data/larson4/UTE_Lung/2022-04-21_pat/seg/',
    '/data/larson4/UTE_Lung/2022-04-22_pat/seg/P15872/',
    '/data/larson4/UTE_Lung/2022-05-20_pat/seg/P31232/',
    '/data/larson4/UTE_Lung/2022-06-14_pat/seg/P63488/',
    ]
    
    slc_list = [
        # 167,
        # 156,
        # 123,
        # 141,
        # 141,
        # 184,
        # 224,
        147,
        187,
        116,
        127,
        132,
        157,
        180,
        # 0,
        183,
        158,
        179,
        167,
                ]
    
    for n in range(len(img_path_list)):

        # load image
        img3d = np.load(img_path_list[n])
        img3d = img3d[0,:,:,:] # select phase
        #img3d = np.flip(img3d,(0,1,2))###new
        
        slc = slc_list[n]
        img = np.abs(img3d[:,slc,:]) # input slice
        img = img / np.amax(img)
        #img = np.flip(img, (0,1))
        
        # draw roi for parenchyma, vessel, airway, background, liver
        mask = np.zeros(img.shape, np.uint8)
        for ind in range(5):
            mask = mask + poly_roi(img, ind + 1)
        
        #cv2.imshow('mask', mask*50)
        #mask = np.flip(mask, (0,1))
        
        mask3d = np.zeros(img3d.shape, np.uint8)
        mask3d[:,slc,:] = mask
        
        #mask3d = np.uint8(mask3d)
        plt.figure()
        plt.imshow(mask + img*10)
        plt.show()
        np.save(roi_dir_list[n] + 'mask_roi.npy', mask3d)