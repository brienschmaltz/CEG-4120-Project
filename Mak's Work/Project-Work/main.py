from email.mime import image
from PIL import Image
import glob
import os, os.path

import cv2 as cv2
import numpy as np
from removeLabelCopy import *

def main(): # Driver
    ######################################### MAIN #########################################
    #reads in image
    ## image = "Q016316C1520U02.tif" #1


    #for Desktop !!CHANGE THIS FOR YOUR COMPUTER!!
    img = cv2.imread("D:\GITHUB\CEG-4121-Project\Mak's Work\SampleImages\Q016316C1520U02.jpg") 

    #for laptop
    #img = cv2.imread("C:/Users/ashto/OneDrive/Desktop/CEG 6120 Managing the Software Process/Group E Project/DoD SAFE-3oqh62xzQKrKPmpj/" + image)

    result = removeLabel(img) 

    #to show that the original size/resolution of the images are maintained
    print("Image Shape: " + (str)(img.shape))
    print("Result Shape: " + (str)(result.shape))

    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.namedWindow('result', cv2.WINDOW_NORMAL)
    cv2.imshow("image", img)
    cv2.imshow("result", result)

    #for desktop !!CHANGE THIS FOR YOUR COMPUTER!!
    cv2.imwrite("D:\GITHUB\CEG-4121-Project\Mak's Work\OutputImages" + "RESULT" + str(image), result)

    #for laptop
    #cv2.imwrite("C:/Users/ashto/OneDrive/Desktop/CEG 6120 Managing the Software Process/Group E Project/Output Images/" + "MASK" + image, mask)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    mainMenu()


def mainMenu(): # Begins Calling Funtions 
    print("*** Image Retrieval Tool V.1.0.5 ***")                   # Just for fun!

    images_retrieved = []                                           # Array of Images Extracted from Folder
    valid_imageExtensions = [".tif", ".png"]                        # Approved Image extentions used later to verify output files

    directoryInput = input ("Enter Image/s Retrieval Directory:")   # User Input of Retrieval Directory
    directoryInput = directoryInput + '\*'                          # the addition of '*' symbol is proper semantics when accessing files in folders
#    directoryOutput = input("Enter Image/s Output Directory:")      # User Inputs directory to store output images

    imageRetrieval(directoryInput,images_retrieved)                 # Sending directyInput & the array to store the images in to the image retrieval function


def imageRetrieval(directoryInput, images_retrieved):               # Function Retrieves Images from Directory and Stores In 'images_retrieved' array

    for f in glob.iglob(directoryInput):
        print('found ' + f)
        images_retrieved.append(f)                                  # Adds Image to Array
        ImportedImage = Image.open(f)                               # Retrieving The Image(ImportedImage) using Image.Open(filename)
        ImportedImage.show()                                        # Shows Images that it is opening

    imageIntegrity(images_retrieved)                                # Sends Retrieved Images to get checked for file integrity

#        if ImportedImage is not None:
#            imageIntegrity(images_retrieved)                        # If image exists check its file type
#            images_retrieved.append(ImportedImage)                  # Append the image into (images_retrieved) arr
        

def imageIntegrity(images_retrieved):
    print("Now Checking File Integrity")                            # Debug Purposes
    for fp in images_retrieved:

        print('checking ', end= "")                                 # DEBUG purposes
        print(fp)                                                   # DEBUG purposes
        print(" ")
        
        split_extension = os.path.splitext(fp)[1].lower()           # Split the extension from the path and normalise it to lowercase.

        if split_extension == ".jpg":                               # DEBUG purposes
            print("File Integrity: It is a .jpg!")
            print(" ")
        elif split_extension != ".jpg":
            print("File Integrity: It is not .jpg!")

def showImage(images_retrieved):                                    # Shows user current image
    for images in images_retrieved:
        images.show()                                               # Shows image received / Debug purposes
if __name__ == "__main__":
    main()