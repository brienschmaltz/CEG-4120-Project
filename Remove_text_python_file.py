#!/usr/bin/env python
# coding: utf-8

# In[6]:


pip install opencv-python


# In[1]:


#Note to self: Nothing OTHER than "pip install dependency" is allowed in a cell. It must be that command and nothing else!


# In[ ]:


import cv2 as cv2
import numpy as np

#Be sure to use foward "/" here
img = cv2.imread("C:/Users/stink/Desktop/WSU/2022 Spring/Managing Software Project/Uranium Photos/Q025558C9220U01.png")


#Unaltered code, if Ashton wants to upload his own additions he can call it version 0.2
#Currently version 0.1


# Load image, convert to HSV format, define lower/upper ranges, and perform
# color segmentation to create a binary mask
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
lower = np.array([0, 0, 218])
upper = np.array([157, 54, 255])
mask = cv2.inRange(hsv, lower, upper)

# Create horizontal kernel and dilate to connect text characters
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,3))
dilate = cv2.dilate(mask, kernel, iterations=5)

# Find contours and filter using aspect ratio
# Remove non-text contours by filling in the contour
cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    x,y,w,h = cv2.boundingRect(c)
    ar = w / float(h)
    if ar < 5:
        cv2.drawContours(dilate, [c], -1, (0,0,0), -1)


#display images
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.namedWindow('mask', cv2.WINDOW_NORMAL)
cv2.imshow("image", img)
cv2.imshow("mask", dilate)
cv2.waitKey(0)
cv2.destroyAllWindows()


# In[ ]:




