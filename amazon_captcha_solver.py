# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 00:25:12 2017

@author: Xianyang
"""

import numpy as np
import argparse
import cv2
import os
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'

def captcha_solver(path,threshold):
    image = cv2.imread(path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    colmean = image.sum(axis=0)/70
    colmean_index = np.where(colmean < threshold)
    min_val = np.min(colmean_index)
    max_val = np.max(colmean_index)
    
    colmean_index = list(colmean_index)
    separators = []
    
    for i in np.arange(0,len(colmean_index[0]) - 1):
        if colmean_index[0][i] != colmean_index[0][i+1] - 1:
            separators.append(colmean_index[0][i])

    if len(separators) == 5: 
        cv2.imwrite('Digit1.jpg', image[:,min_val:separators[0]])
        cv2.imwrite('Digit2.jpg', image[:,separators[0]+1:separators[1]])
        cv2.imwrite('Digit3.jpg', image[:,separators[1]+1:separators[2]])
        cv2.imwrite('Digit4.jpg', image[:,separators[2]+1:separators[3]])
        cv2.imwrite('Digit5.jpg', image[:,separators[3]+1:separators[4]])
        cv2.imwrite('Digit6.jpg', image[:,separators[4]+1:max_val])
        
        string = []
        for i in np.arange(1,7):
            if i == 1:
                img = Image.open('Digit'+str(i)+'.jpg')
                # converted to have an alpha layer
                im2 = img.convert('RGBA')
                # rotated image
                rot = im2.rotate(15, expand=1)
                # a white image same size as rotated image
                fff = Image.new('RGBA', rot.size, (255,)*4)
                # create a composite image using the alpha layer of rot as a mask
                out = Image.composite(rot, fff, rot)
                            
                out.convert(img.mode).save('pic.jpg')
                 
                char = pytesseract.image_to_string(Image.open('pic.jpg'),
                                                   config='-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ -psm 10')[0].upper()   
                                                           
                string = char
            elif i in [3,5]:
                img = Image.open('Digit'+str(i)+'.jpg')
                # converted to have an alpha layer
                im2 = img.convert('RGBA')
                # rotated image
                rot = im2.rotate(15, expand=1)
                # a white image same size as rotated image
                fff = Image.new('RGBA', rot.size, (255,)*4)
                # create a composite image using the alpha layer of rot as a mask
                out = Image.composite(rot, fff, rot)
                            
                out.convert(img.mode).save('pic.jpg')
                 
                char = pytesseract.image_to_string(Image.open('pic.jpg'),
                                                   config='-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ -psm 10')[0].upper()   
                                                           
                string += char
            else:
                img = Image.open('Digit'+str(i)+'.jpg')
                # converted to have an alpha layer
                im2 = img.convert('RGBA')
                # rotated image
                rot = im2.rotate(-15, expand=1)
                # a white image same size as rotated image
                fff = Image.new('RGBA', rot.size, (255,)*4)
                # create a composite image using the alpha layer of rot as a mask
                out = Image.composite(rot, fff, rot)
                            
                out.convert(img.mode).save('pic.jpg')
                 
                char = pytesseract.image_to_string(Image.open('pic.jpg'),
                                                   config='-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ -psm 10')[0].upper()   
                                                           
                string += char
    else: 
        string='Cannot solve Captcha'
        
    return(string)