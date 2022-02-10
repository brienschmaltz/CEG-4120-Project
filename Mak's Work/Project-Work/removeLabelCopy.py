from tkinter import Image
import cv2 as cv2
import numpy as np

#detects the rectangles in the image
#returns a mask image of the detected rectangles
#CURRENTLY NOT BEING USED!!!
def detectRectangle(image):
    
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #converts to gray

    rows,cols,_ = image.shape 
    mask = image.copy() #makes copy of original image

    #goes pixel by pixel and make every pixel black 
    #(makes all black image to add rectangles to)
    for i in range(rows):
        for j in range(cols):
            mask[i,j] = [0, 0, 0] #(make it black)

    #find threshold of the image
    _, thrash = cv2.threshold(gray_image, 240, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    for contour in contours:
        shape = cv2.approxPolyDP(contour, 0.01*cv2.arcLength(contour, True), True)
        
        if len(shape) == 4:
            #shape cordinates
            x,y,w,h = cv2.boundingRect(shape)
            aspectRatio = float(w)/h

            #only writes it out if it's a big enough rectangle
            if(aspectRatio > 2):
                cv2.drawContours(mask, [shape], 0, (255,255,255), thickness=cv2.FILLED) #draws in detected rectangles
                #cv2.putText(image, "Rectangle", (x_cor, y_cor), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255,0,0))
        
    return mask #mask of detected rectangles


#detects the bigger white areas in the image
#returns a mask of the dilated detected white areas
def detectWhite(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) #convert to HSV

    #image preprocessing
    hsv_low = np.array([0, 0, 0], np.uint8)
    hsv_high = np.array([179, 255, 254], np.uint8)
    mask = cv2.inRange(hsv, hsv_low, hsv_high)
    mask = cv2.bitwise_not(mask) #inverts the mask (flips black and white)

    #Gaussian blur and adaptive threshold
    blur = cv2.GaussianBlur(mask, (9,9), 0)
    thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,11,15)

    #Dilate to combine letters (make detected text a blob)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9,9))
    dilate = cv2.dilate(thresh, kernel, iterations=6)

    mask = cv2.cvtColor(dilate,cv2.COLOR_GRAY2BGR) #convert back to RGB (3 channels)
    return mask #mask of detected dilated white areas

##### TESTING AN IDEA #####
#gets the color of the nearest not white pixel
# def getBackgroundColor(img, rows, cols, m, n):
#     for i in range(m, rows):
#             for j in range(n, cols):

#                 try:
#                     if((img[i,j] < [250, 250, 250]).all()):
#                         continue
#                     else:
#                         return img[i,j] #return closest not white character
#                 except:
#                     return [0,0,0] #if something breaks, return black


#Ashton's remove white pixels function
# def remove_white_pixels(img, mask, rows, cols):
#     result = img.copy()
#     for i in range(rows):
#             backgroundColor = img[i,0] #get the background color for this row
#             for j in range(cols):
#                 if((np.array_equal(mask[i,j], np.array([255, 255, 255])))):
#                     result[i,j] = backgroundColor #make it the background color
#     return result

#Brien's remove white pixels function
def remove_white_pixels(original_img, mask_img, rows, cols, img):

    result_img = original_img.copy() #Copy 

    #Loop that iterates through each pixel, determines if white, then makes that pixel black. 
    for i in range(rows):
        for j in range(cols):
            mask_pixel_val = mask_img[i,j] #value/color of the current pixel
            backgroundColor = img[i,0] #get the background color for this row
            
            # Conditional to determine if pixel is white.
            if (np.array_equal(mask_pixel_val, np.array([255, 255, 255]))):
                # Then eradicate white pixels.
                result_img[i,j] = backgroundColor #make it the color at the start of the row
    
    return result_img

#removes the unwated labels from the images
#returns result/final image
def removeLabel(image):
    #copies of the first image (so I dont overwrite the original one)
    img = image.copy()
    img2 = image.copy()
    img3 = image.copy()

    rows,cols,_ = img.shape #gets the image array shape

    #removes labels on images with grey area at the bottom
    if(rows == 1530):

        for i in range(1280, 1530):
            for j in range(cols):
                img[i,j] = img[0,0] #make it the background color
        result = img

    #removes labels on images with transparent label in the top right
    elif(rows == 1280 and cols == 1280):

        for i in range(0, 150):
            for j in range(555, 1235):
                img[i,j] = img[i,0] #make it the background color
        result = img
        
    #removes labels for every other image
    else:
        topLeft = False #bool that is true if a rectangle needs to be in the top left

        #check if there is white in top left
        for i in range(0, 45):
            for j in range(0, 150):
                if(np.array_equal(image[i,j], np.array([255, 255, 255]))):
                    topLeft = True
                    break #stop if white is found
            
            if(topLeft):
                break #stop if white is found

        #if there is white in the top left, add a rectangle   
        if (topLeft):
            for i in range(0, 45):
                for j in range(0, 150):
                    img2[i,j] = [255, 255, 255] #add white mask top

        dect_white = detectWhite(img) #gets mask of detected white
        #dect_rect = detectRectangle(img2) #gets mask of detected rectangles

        #combines detected rectangles mask and the detected white mask
        #combMask = dect_white + dect_rect #add the two masks together

        result = remove_white_pixels(img3, dect_white, rows, cols, image)

    return result
    

