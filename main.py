#importing libraries
import cv2
import numpy as np
from matplotlib import pyplot as plt
from numpy.core.fromnumeric import ptp
import pytesseract
from pytesseract import Output
import sys
import re
import datetime, time

#sorting the dates and identifying the DOB, DOI and DOE
def sort_dates(Dates,details):
    if(len(Dates)==0):return
    year = []
    for date in Dates:
        if '/' in date:
            day, month,yr = date.split("/")
            year.append(yr)
        else:
            day, month,yr = date.split("-")
            year.append(yr)

    if(len(Dates)==1):
        dob = Dates[0]
        details['dob']=dob
        return

    if(len(Dates)<=2):
        if(year[0]<year[1]):
            dob=Dates[0]
            issue = Dates[1]
            details['dob']=dob
            details['issued']=issue
        return
    if(year[0]<year[1] and year[0]<year[2]):
        dob = Dates[0]
        if(year[1]<year[2]):
            issue = Dates[1]
            Expiry = Dates[2]
            details['dob']=dob
            details['issued']=issue
            details['expiry']=Expiry
    elif (year[1]<year[0] and year[1]<year[2]):
        dob = Dates[1]
        if(year[0]<year[2]):
            issue = Dates[0]
            Expiry = Dates[2]
            details['dob']=dob
            details['issued']=issue
            details['expiry']=Expiry
    else:
        dob = Dates[2]
        if(year[0]<year[1]):
            issue = Dates[0]
            Expiry = Dates[1]
            details['dob']=dob
            details['issued']=issue
            details['expiry']=Expiry
    return

#defining the path of tesseract 
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

#defining the kerner parameters
rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10,10))

#function to get the details of the image
def get_details(img):
    #initiating variables and a dictionary to store the details
    flag_id =0
    name_id =0
    details = {}

    #storing the eye colors in an array
    eye_c = ['BLU', 'BRO', 'BRN', 'BLK', 'GRY', 'GRN', 'HZL']

    #preprocessing the image
    img = cv2.resize(np.array(img),(800,500)) 
    img = img[100:,280:]
    img = cv2.fastNlMeansDenoisingColored(img,None,10,10,7,21)
    gr = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #ed = cv2.Canny(gr,30,200)
    ret,gr = cv2.threshold(gr,50,255,cv2.THRESH_BINARY_INV)
    
    #getting the text using the tesseract from processed image
    text = pytesseract.image_to_string(gr)
    res = text.split()
    res1 = text.splitlines()
    
    #pattern for identifying the dates in the text
    date_pattern1 = '^\d{2}/\d{2}/\d{4}'
    date_pattern2 = '^\d{2}-\d{2}-\d{4}'
    Dates = []

    #iterating through the text and identifying each element
    for i in range(len(res)):
        if re.match(date_pattern1, res[i]) or re.match(date_pattern2,res[i]):
            Dates.append(res[i])
        if (res[i]=='F' or res[i]=='M'):
            sex = res[i]
            details['sex']=sex 

        if ((len(res[i])>8) and (i <= 3) and flag_id==0):
            flag_id=1
            details['id'] = res[i] 
        if(len(res[i])==3):
            col = res[i]
            for c in range(len(eye_c)):
                if(col == eye_c[c]):
                    details['eyes']=col

    for i in range(len(res1)):
        word = res1[i]
        if(len(word)>3 and word.isalpha() and name_id==0):
            first_name = word
            details['first_name']=first_name
            if(len(res1[i+1])>2):
                last_name = res1[i+1]
            else :
                last_name = res1[i+2]
            details['last_name']=last_name
            name_id=1

        if(len(word)>12 and name_id==1):
            alpha =0
            num =0
            for w in word:
                if(w.isalpha()==True):
                    alpha=alpha+1
                elif (w.isnumeric()==True):
                    num= num+1
            if (alpha>6 and num >1):
                loc = word
                loc = loc + ',  ' +res1[i+1]
                if(len(res1[i+1])<10):
                    loc=loc+res1[i+2]
                details['address']= loc
                break

    #if no dates are identified asking the user to redo 
    if(len(Dates)==0):
        print("retake photo or adjust the threshold")
    else:
        #sorting the dates
        sort_dates(Dates,details)
    #returning the details dictionary
    return (details)