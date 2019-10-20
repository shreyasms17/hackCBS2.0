# -*- coding: utf-8 -*-
"""
Created on Sun Oct 20 03:40:05 2019

@author: ASUS
"""
import csv
import re
from fuzzywuzzy import fuzz 
from fuzzywuzzy import process  
import pytesseract
import cv2
import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
Date=""
Price=""
Invoice=""
mm=""
def addData(inv='NULL', date='NULL', amt='NULL'):
    fp = open("retailData1.csv", 'a+')
    buf = str(inv)+','+str(date)+','+str(amt)
    fp.writelines('\n')
    fp.writelines(buf)
    
    fp.close()
def removeLines(image):
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
   
    # Find and remove horizontal lines
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (35,2))
    detect_horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
    cnts = cv2.findContours(detect_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(thresh, [c], -1, (0,0,0), 3)
   
    # Find and remove vertical lines
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,35))
    detect_vertical = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
    cnts = cv2.findContours(detect_vertical, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(thresh, [c], -1, (0,0,0), 3)
   
    # Mask out unwanted areas for result
    result = cv2.bitwise_and(image,image,mask=thresh)
    result[thresh==0] = (255,255,255)
   
    #cv2.imshow('thresh', thresh)
    #cv2.imshow('result', result)
    #cv2.waitKey()
   
    return result
    #res = np.hstack((grey, new))
    return new
def increase_brightness(img, value=30):
    print(np.mean(img))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    print(np.mean(img))
    return img
image_loc='G://Hackcbs2.0//131882_.png'
file_loc="G://Hackcbs2.0//text_file//myfile.txt"
img=cv2.imread(image_loc)
value=int(np.mean(img))
toinc=abs(180-value)
if(value>180):
    toinc=0
img=increase_brightness(img,toinc)
#img=removeLines(img)
cv2.imwrite('G://Hackcbs2.0//invoice_images//test.jpg',img)

stringy = pytesseract.image_to_string(img,lang='trainiee',config='--psm 6 -c preserve_interword_spaces=1')
file1=open(file_loc,'w+')
file1.write(stringy)
file1.close()
templates=['COMPUTER','SHAH',' OM ELEC ','JYOT','VINAYAK']
pair=process.extractOne(stringy,templates)

def computertemp(img):
    Date=""
    Price=""
    Invoice=""
    mm=""
    img=removeLines(img)
    #img=binarization(img)
    stringy = pytesseract.image_to_string(img,lang='trainiee',config='--psm 6 -c preserve_interword_spaces=1')
    #file1=open()
    file1=open(file_loc,'w+')
    #str=file1.readlines()
    #print(str)
    file1.write(stringy)
    file1.close()

    #file open to read files
    file1 = open(file_loc,"r+") 
    stringy=file1.read()

    #Date extration template 1
    m=re.findall('[from|From]*[ ]*[0-9]{1,2}-[a-z|A-Z]{3}-[0-9]{4}',stringy)
    #print(m)
    for i in m:
        if(re.search("From",i)==None):
            Date=i
            Date=Date.strip()
            
    #------------------------------------------------
    #invoice number extration
    m=re.findall('MARKET[ ]*[0-9]{1,5}',stringy)
    strm=''.join(m)
    mm=re.findall('[0-9]{1,5}',strm)
    Invoice=''.join(mm)
    
    #-------------------------------------------------
    #Price extraction
    m=re.findall('[0-9|,]+[.][0-9]{2}',stringy)
    #if(m is not None):
     #   Price=m[0]
    maxi=0.0
    for i in m:
        i=i.replace(',','')
        temp=float(i)
        if(temp>maxi):
            maxi=temp
    Price=maxi
    
    #---------------------------------------------------------
    m=re.findall('PCS.*PCS.*\n.*',stringy)
    mm=''.join(m)
    mm=mm[mm.find('\n')+1:]
    if not Date and not Invoice and not Price:
        print("Completely blurred image")
    elif not Date and not Invoice:
        print("Partially blurred image")
        print("Price"+float(Price))
        addData('NULL','NULL',Price)
    elif not Date and not Price:
        print("Partially blurred image")
        print(Invoice)
        addData('NULL',Invoice,'NULL')
    else:  
        print("Entered computer Electronics")
        print("Date "+str(Date))
        print("Invoice "+str(Invoice))
        print("Price "+str(Price))
        print("Serial no"+mm)
        addData(Date,Invoice,Price)
    
    #print(ztrm)
    file1.close()
def shahtemp(img):
    Date=""
    Price=""
    Invoice=""
    mm=""
    #print("Shah company")
    #img=increase_brightness(img)
    #cv2.imwrite(name,img)
    #img=binarization(img)
    #img=rotate_image(img,90)
   # cv2.imwrite(name,img)
    stringy = pytesseract.image_to_string(img,lang='trainiee',config='--psm 6 -c preserve_interword_spaces=1')
    #file1=open()
    file1=open(file_loc,'w+')
    #str=file1.readlines()
    #print(str)
    file1.write(stringy)
    file1.close()

    #file open to read files
    file1 = open(file_loc,"r+") 
    stringy=file1.read()

    #Date extration template 2
    m=re.findall('[0-9]{1,2}-[a-z|A-Z]{3}-[0-9]{4}',stringy)
    Date="".join(m)
    #print(Date)
    #------------------------------------------------
    #invoice number extration
    m=re.findall('AM[ ]*-*[0-9]{1,5}',stringy)
    strm=''.join(m)
    mm=re.findall('[0-9]{1,5}',strm)
    Invoice=''.join(mm)
    #print(Invoice)
    #-------------------------------------------------
    #Price extraction
    m=re.findall('[0-9|,|.]+[.][0-9]{2}',stringy)
    #if(m is not None):
     #   Price=m[0]
    maxi=0.0
    for i in m:
        i=i.replace(',','')
        i=i.replace('.','')
        temp=float(i)
        if(temp>maxi):
            maxi=temp
    Price=maxi/100
  #  print(Price)
    #---------------------------------------------------------
    m=re.findall('AMOUNT[ ]*\n.*',stringy)
    mm=''.join(m)
    mm=mm[mm.find('\n')+1:]
    
    if not Date and not Invoice and not Price:
        print("Completely blurred image")
    elif not Date and not Invoice:
        print("Partially blurred image")
        print("Price"+str(Price))
        addData('NULL','NULL',Price)
    elif not Date and not Price:
        print("Partially blurred image")
        print("Invoice"+str(Invoice))
        addData('NULL',Invoice,'NULL')
    else:  
        print("Entered shah Electronics")
        print("Date "+str(Date))
        print("Invoice "+str(Invoice))
        print("Price "+str(Price))
        print("Serial no"+mm)
        addData(Date,Invoice,Price)
    
    #print(ztrm)
    file1.close()
def omelectemp(img):
    Date=""
    Price=""
    Invoice=""
    mm=""
    print("Om Electronics")
    value=int(np.mean(img))
    #img=increase_brightness(img)
    cv2.imwrite(name,img)
    #img=binarization(img)
    stringy = pytesseract.image_to_string(img,lang='trainiee',config='--psm 3 -c preserve_interword_spaces=1')
    #file1=open()
    file1=open(file_loc,'w+')
    #str=file1.readlines()
    #print(str)
    file1.write(stringy)
    file1.close()

    #file open to read files
    file1 = open(file_loc,"r+") 
    stringy=file1.read()

    #Date extration template 1
    m=re.findall('[0-9]{1,2}[-|.][0-9]{1,2}[-|.][0-9]{2}',stringy)
    #print(m)
    for i in m:
        if(re.search("From",i)==None):
            Date=i
            Date=Date.strip()
     #       print(Date)
    #------------------------------------------------
    #invoice number extration
    m=re.findall('Invoice No[,|. ]*[0-9]{3,5}',stringy)
    strm=''.join(m)
    mm=re.findall('[0-9]{1,5}',strm)
    Invoice=''.join(mm)
    #print(Invoice)
    #-------------------------------------------------
    #Price extraction
    m=re.findall('[0-9|,|.]+[.][0-9]{2}',stringy)
    #if(m is not None):
     #   Price=m[0]
    maxi=0.0
    for i in m:
        i=i.replace(',','')
        i=i.replace('.','')
        temp=float(i)
        if(temp>maxi):
            maxi=temp
    Price=maxi/100
    #print(Price)
    #---------------------------------------------------------
    m=re.findall('Amount[ ]*.*\n.*',stringy)
    mm=''.join(m)
    mm=mm[mm.find('\n')+1:]
    
    if not Date and not Invoice and not Price:
        print("Completely blurred image")
    elif not Date and not Invoice:
        print("Partially blurred image")
        print("Price"+str(Price))
        addData('NULL','NULL',Price)
    elif not Date and not Price:
        print("Partially blurred image")
        print(Invoice)
        addData('NULL',Invoice,'NULL')
    else:  
        print("Entered om Electronics")
        print("Date "+str(Date))
        print("Invoice "+str(Invoice))
        print("Price "+str(Price))
        print("Serial no"+mm)
        addData(Date,Invoice,Price)
    
    #print(ztrm)
    file1.close()
def jyottemp(img):
    Date=""
    Price=""
    Invoice=""
    mm=""
    #img=increase_brightness(img)
    #print("Jyot or vinayak electronics")
    cv2.imwrite(name,img)
    #img=binarization(img)
    height, width = img.shape[:2]
    # Let's get the starting pixel coordiantes (top left of cropped top)
    start_row, start_col = int(0), int(0)
    # Let's get the ending pixel coordinates (bottom right of cropped top)
    end_row, end_col = int(height * .5), int(width)
    cropped_top = img[start_row:end_row , start_col:end_col]
    print (start_row, end_row) 
    print (start_col, end_col)
    
    
    #cv2.waitKey(0) 
    #cv2.destroyAllWindows()
    
    # Let's get the starting pixel coordiantes (top left of cropped bottom)
    start_row=int(0)
    end_row=int(height* 0.5)
    start_col=int(width*0.5)
    #start_row, start_col = int(height * .5), int(0)
    # Let's get the ending pixel coordinates (bottom right of cropped bottom)
    end_col =int(width)
    cropped_bot = img[start_row:end_row , start_col:end_col]
    cv2.imwrite("Croppedbot.jpg",cropped_bot) 
    stringy = pytesseract.image_to_string( cropped_bot,lang='trainiee',config='--psm 6 -c preserve_interword_spaces=1')
    #file1=open()
    file1=open(file_loc,'w+')
    #str=file1.readlines()
    #print(str)
    file1.write(stringy)
    file1.close()

    #file open to read files
    file1 = open(file_loc,"r+") 
    stringy=file1.read()

    #Date extration template 1
    m=re.findall('[0-9]{1,2}/[0-9]{1,2}/[0-9]{2}',stringy)
    #print(m)
    for i in m:
        if(re.search("From",i)==None):
            Date=i
            Date=Date.strip()
     #       print(Date)
    #------------------------------------------------
    #invoice number extration
    m=re.findall('Invoice.*',stringy)
    strm=''.join(m)
    mm=re.findall('[0-9]{1,5}',strm)
    Invoice=''.join(mm)
    #print(Invoice)
    #-------------------------------------------------
    #Price extraction
    m=re.findall('[0-9]{1,2},[0-9]{1,3}',stringy)
    #if(m is not None):
     #   Price=m[0]
    #print(m)
    maxi=0.0
    for i in m:
       # print(i)
        i=i.replace(',','')
        #i=i.replace('.','')
        if not i:
            temp=0
        else:
            temp=int(i)
        if(temp>maxi):
            maxi=temp
    Price=maxi
    #print(Price)
    #---------------------------------------------------------
    m=re.findall('Amount[ ]*.*\n.*',stringy)
    mm=''.join(m)
    mm=mm[mm.find('\n')+1:]
    
    if not Date and not Invoice and not Price:
        print("Completely blurred image")
    elif not Date and not Invoice:
        print("Partially blurred image")
        print("Price"+float(Price))
        addData('NULL','NULL',Price)
    elif not Date and not Price:
        print("Partially blurred image")
        print(Invoice)
        addData('NULL',Invoice,'NULL')
    else:  
        print("Entered Jyot and vinayak Electronics")
        print("Date "+str(Date))
        print("Invoice "+str(Invoice))
        print("Price "+str(Price))
        print("Serial no"+mm)
        addData(Date,Invoice,Price)
    
    #print(ztrm)
    file1.close()
choice=pair[0]
if choice=='COMPUTER':
    computertemp(img)
elif choice=='SHAH':
    shahtemp(img)
elif choice=='OM ELEC':
    omelectemp(img)
else:
    jyottemp(img)

