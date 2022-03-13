from tkinter import N
import cv2 as cv2
import numpy as np
from statistics import mode

#detects the rectangles in the image
#returns a mask image of the detected rectangles
#CURRENTLY NOT BEING USED!!!
# def detectRectangle(image):
    
#     gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #converts to gray

#     rows,cols,_ = image.shape 
#     mask = image.copy() #makes copy of original image

#     #goes pixel by pixel and make every pixel black 
#     #(makes all black image to add rectangles to)
#     for i in range(rows):
#         for j in range(cols):
#             mask[i,j] = [0, 0, 0] #(make it black)

#     #find threshold of the image
#     _, thrash = cv2.threshold(gray_image, 240, 255, cv2.THRESH_BINARY)
#     contours, _ = cv2.findContours(thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

#     for contour in contours:
#         shape = cv2.approxPolyDP(contour, 0.01*cv2.arcLength(contour, True), True)
        
#         if len(shape) == 4:
#             #shape cordinates
#             x,y,w,h = cv2.boundingRect(shape)
#             aspectRatio = float(w)/h

#             #only writes it out if it's a big enough rectangle
#             if(aspectRatio > 2):
#                 cv2.drawContours(mask, [shape], 0, (255,255,255), thickness=cv2.FILLED) #draws in detected rectangles
#                 #cv2.putText(image, "Rectangle", (x_cor, y_cor), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255,0,0))
        
#     return mask #mask of detected rectangles


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

#returns a mask image that contains just the background (uranium replaced with the background color)
def get_background(img, rows, cols):

    #average = np.median(img)
    average = (int)(mode(img.flatten())) #gets the mode of image (most common color value)

    #average = np.median(img)
    # average = (int)(mode(img.flatten()))

    # if(average > 90):
    #     average = (int)(np.median(img)/2)
    
    
    # if(average <= 20):
    #     average = (int)(np.median(img))


    # average = (int)(mode(img.flatten()))

    #if the mode is over 90, half it
    if(average > 90):
        average = (int)(average/2)
    
    #if after halfing it and it is under 20, use the median instead
    if(average <= 20):
        average = (int)(np.median(img))

        #if the median is over 90 half it
        if(average > 90):
            average = (int)(average/2)

    
    #print(average)
    background = img.copy()

    prevPixel = [average,average,average] #initially define a pixel value that is the average
    for i in range(rows):
        for j in range(cols):
            #print(pixel)

            #if the average of the current pixel value is greater than the overall average, its part of the uraniam
            if (np.average(background[i][j]) > average): 
                if(j == 0):
                    background[i][j] = prevPixel #make the pixel the background value
                else:
                    randomInt = np.random.randint(0,j) #get a random index value in the row
                    prevPixel = background[i][randomInt] #set the prevPixel to the value at that random index
                    background[i][j] = prevPixel #it is the new background pixel

    return background


#Brien's remove white pixels function
def remove_white_pixels(original_img, mask_img, rows, cols, background, topLeft):

    result_img = original_img.copy() #Copy 
    #background = get_background(original_img, rows, cols)
    n=0 #background row index
    m=0 #background column index

    if(topLeft):
        n = 45 #if top left is true, start background row index at 45

    backRow, backCol, _ = np.array(background).shape
    #print(backSize)

    #Loop that iterates through each pixel, determines if white, then makes that pixel black. 
    for i in range(rows):
        for j in range(cols):
            mask_pixel_val = mask_img[i,j] #value/color of the current pixel
            #backgroundColor = img[i,0] #get the background color for this row
            
            # Conditional to determine if pixel is white.
            if (np.array_equal(mask_pixel_val, np.array([255, 255, 255]))):
                # Then eradicate white pixels.
                result_img[i,j] = background[n][m] #make it a color 
                
                #keep going until at the end of the row in the background mask, then go to the next row
                m+=1 #if at the end of the row
                if(m == backCol):
                    n+=1 #increment rows 
                    m=0 #set column index back to 0

    return result_img

#returns the image with the black box removed by filling in the black box pixels with pixels from the background mask
def remove_black_box(img, rows, cols, background, topLeft):
    n=0 #background row index
    m=0 #background column index
    backRow, backCol, _ = np.array(background).shape 
    result_img = img.copy()

    #print(img[940, 0])
    #print(img[960, 0])

    #if there is text in the top left
    if(topLeft):
        n=880 #start n at 880 if top left is true
        
        if (np.array_equal(img[933, 0], np.array([1,1,1]))): #if the first pixel at row 933 is black
            
            #loop through and replace the black with a pixel from the background mask
            for i in range(933, rows): 
                for j in range(cols):
                    result_img[i,j] = background[n][m] 
                    
                    #keep going until at the end of the row in the background mask, then go to the next row
                    m+=1 #if at the end of the row
                    if(m == backCol):
                        n+=1 #increment rows 
                        m=0 #set column index back to 0

        elif (np.array_equal(img[960, 0], np.array([1,1,1]))): #if the first pixel at row 960 is black
            
            #loop through and replace the black with a pixel from the background mask
            for i in range(960, rows):
                for j in range(cols):
                    result_img[i,j] = background[n][m] 
                    
                    #keep going until at the end of the row in the background mask, then go to the next row
                    m+=1 #if at the end of the row
                    if(m == backCol):
                        n+=1 #increment rows 
                        m=0 #set column index back to 0

    #if there isnt white pixels in the top left
    else:
        if (np.array_equal(img[933, 0], np.array([1,1,1]))): #if the first pixel at row 933 is black
            
            #loop through and replace the black with a pixel from the background mask
            for i in range(933, rows):
                for j in range(cols):
                    result_img[i,j] = background[n][m] 
                    
                    #keep going until at the end of the row in the background mask, then go to the next row
                    m+=1 #if at the end of the row
                    if(m == backCol):
                        n+=1 #increment rows 
                        m=0 #set column index back to 0

        elif (np.array_equal(img[960, 0], np.array([1,1,1]))): #if the first pixel at row 960 is black
            
            #loop through and replace the black with a pixel from the background mask
            for i in range(958, rows):
                for j in range(cols):
                    result_img[i,j] = background[n][m] 
                    
                    #keep going until at the end of the row in the background mask, then go to the next row
                    m+=1 #if at the end of the row
                    if(m == backCol):
                        n+=1 #increment rows 
                        m=0 #set column index back to 0

    return result_img

#removes the unwated labels from the images
#returns result/final image
def removeLabel(image):
    #copies of the first image (so I dont overwrite the original one)
    img = image.copy()
    img2 = image.copy()
    img3 = image.copy()

    rows,cols,_ = img.shape #gets the image array shape
    background = get_background(img, rows, cols) #gets the background mask
    n=0 #background row index
    m=0 #background column index
    backRow, backCol, _ = np.array(background).shape
    #return background
    
    #removes labels on images with grey area at the bottom
    if(rows == 1530):

        for i in range(1280, 1530):
            for j in range(cols):
                img2[i,j] = background[n][m] #make it a value in the background mask
                
                #keep going until at the end of the row in the background mask, then go to the next row
                m+=1 #inrement column
                if(m == backCol): #if at the end of the row
                    n+=1 #increment rows 
                    m=0 #set column index back to 0
        result = img2


    #removes labels on images with transparent label in the top right
    elif(rows == 1280 and cols == 1280):

        for i in range(0, 150):
            for j in range(555, 1235):
                img2[i,j] = background[i+1130][j] #make it a value in the background mask

        result = img2
        
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

        removedBox = remove_black_box(img3, rows, cols, background, topLeft) #gets the background mask of the image (mask that just contains the background with no uranium)
        
        dect_white = detectWhite(removedBox) #gets mask of detected white
        #dect_rect = detectRectangle(img2) #gets mask of detected rectangles
        
        #combines detected rectangles mask and the detected white mask
        #combMask = dect_white + dect_rect #add the two masks together
        
        result = remove_white_pixels(removedBox, dect_white, rows, cols, background, topLeft) #removes the remaining white pixels from the image

    return result
    
######################################### MAIN #########################################
#STUFF IN THE MAIN ONLY WORKS ON ASHTON'S COMPUTER!!!

#reads in image (old images)
#image = "Q016316C1520U02.tif" #1
#image = "Q019910C1010U02.tif" #2
#image = "Q019910C1020U01.tif" #3
#image = "Q019910C8040U02.tif" #4
#image = "Q025558C9220U01.png" #5
#image = "Q026480C9030U01.png" #6

#new images
#image = "Q016312C1010U01.tif" #7
#image = "Q016312C1020U01.tif" #8
#image = "Q016312C1030U01.tif" #9
#image = "Q016312C1040U01.tif" #10
#image = "Q016312C1050U01.tif" #11
#image = "Q016312C5010U03.tif" #12
#image = "Q016312C5020U03.tif" #13
#image = "Q016312C5040U01.tif" #14
#image = "Q016312C8020U01.tif" #15
#image = "Q016312C8030U01.tif" #16
#image = "Q016312C8040U01.tif" #17
#image = "Q016314C1010U03.tif" #18
#image = "Q016314C1030U01.tif" #19
#image = "Q016314C8010U02.tif" #20

#array that contains every picture we have so far
images = ["Q016316C1520U02.tif", "Q019910C1010U02.tif", "Q019910C1020U01.tif", "Q019910C8040U02.tif", "Q025558C9220U01.png", "Q026480C9030U01.png", "Q016312C1010U01.tif", "Q016312C1020U01.tif",
 "Q016312C1030U01.tif", "Q016312C1040U01.tif", "Q016312C1050U01.tif", "Q016312C5010U03.tif", "Q016312C5020U03.tif", "Q016312C5040U01.tif", "Q016312C8020U01.tif", "Q016312C8030U01.tif", 
 "Q016312C8040U01.tif", "Q016314C1010U03.tif", "Q016314C1030U01.tif", "Q016314C8010U02.tif"]

#for Desktop !!CHANGE THIS FOR YOUR COMPUTER!!
#img = cv2.imread("C:/Users/Ashton Williams/OneDrive/Desktop/CEG 6120 Managing the Software Process/Group E Project/DoD SAFE-3oqh62xzQKrKPmpj/" + image) #old images 
#img = cv2.imread("C:/Users/Ashton Williams/OneDrive/Desktop/CEG 6120 Managing the Software Process/Group E Project/DoD SAFE-2U8EosQU5YDpX4hC/" + image) #new images
# img = cv2.imread("C:/Users/Ashton Williams/OneDrive/Desktop/CEG 6120 Managing the Software Process/Group E Project/all images/" + image) #new images
# #for laptop
# #img = cv2.imread("C:/Users/ashto/OneDrive/Desktop/CEG 6120 Managing the Software Process/Group E Project/DoD SAFE-3oqh62xzQKrKPmpj/" + image)

# result = removeLabel(img) 

# #to show that the original size/resolution of the images are maintained
# print("Image Shape: " + (str)(img.shape))
# print("Result Shape: " + (str)(result.shape))

# cv2.namedWindow('image', cv2.WINDOW_NORMAL)
# cv2.namedWindow('result', cv2.WINDOW_NORMAL)
# cv2.imshow("image", img)
# cv2.imshow("result", result)

# #for desktop !!CHANGE THIS FOR YOUR COMPUTER!!
# cv2.imwrite("C:/Users/Ashton Williams/OneDrive/Desktop/CEG 6120 Managing the Software Process/Group E Project/Output Images/" + "RESULT" + image, result)

# #for laptop
# #cv2.imwrite("C:/Users/ashto/OneDrive/Desktop/CEG 6120 Managing the Software Process/Group E Project/Output Images/" + "MASK" + image, mask)

# cv2.waitKey(0)
# cv2.destroyAllWindows()

#loops through every image in the images array, removing the unwanted areas and saving the output
for i in images:
    img = cv2.imread("C:/Users/Ashton Williams/OneDrive/Desktop/CEG 6120 Managing the Software Process/Group E Project/all images/" + i) #all images
    result = removeLabel(img) 
    cv2.imwrite("C:/Users/Ashton Williams/OneDrive/Desktop/CEG 6120 Managing the Software Process/Group E Project/Output Images/" + "RESULT" + i, result)