from removeLabelCopy import *
from email.mime import image
from PIL import Image
from tqdm import tqdm

import time
import glob
import os, os.path
import cv2 as cv2
import numpy as np

def main(): #                                                       *** MAIN ***


    mainMenu() # START MAIN MENU

def mainMenu():                                                     # Start Program
    print("*** Image Cleanup Tool V.1.0 ***")                       # Menu Screen

    images_retrieved = []                                           # Array of Images Extracted from Folder
    valid_imageExtensions = [".tif", ".png"]                        # Approved Image extentions used later to verify output files

    directoryInput = input ("Enter Image/s Retrieval Directory:")   # User Input of Retrieval Directory
    folderInspection(directoryInput)
    directoryInput = directoryInput + '\*'                          # the addition of '*' symbol is proper semantics when accessing files in folders
    imageRetrieval(directoryInput,images_retrieved)                 # Sending directyInput & the array to store the images in to the image retrieval function

    imageToCV2(images_retrieved)                                    # After imageRetrieval completion program sends imported images array to CV2 editor


def imageToCV2(images_retrieved):
    imageCounter = 1
    for i in tqdm(images_retrieved):                                      #  traversing through the image loop to find each image and pass forward to removeLabel
        print("image " + i) # DEBUG PURPOSES

        #for Desktop !!CHANGE THIS FOR YOUR COMPUTER!!
        img = cv2.imread(i) 

        result = removeLabel(img) 

        #to show that the original size/resolution of the images are maintained
        print("Image Shape: " + (str)(img.shape))
        print("Result Shape: " + (str)(result.shape))

        cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        cv2.namedWindow('result', cv2.WINDOW_NORMAL)
        cv2.imshow("image", img)
        cv2.imshow("result", result)

        #for desktop !!CHANGE THIS FOR YOUR COMPUTER!!

        cv2.imwrite("D:\GITHUB\CEG-4121-Project\Mak's Work\OutputImages\result" + str(image) + ".jpg", result)

        #for laptop
        #cv2.imwrite("C:/Users/ashto/OneDrive/Desktop/CEG 6120 Managing the Software Process/Group E Project/Output Images/" + "MASK" + image, mask)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

        print("Image: " + i + " Succesful")
        imageCounter += 1
        time.sleep(0.3)


def folderInspection(directoryInput):                               # Function designed to check if folder exists
    print("Checking Folder Path (" + directoryInput + ")...")

    if os.path.exists(directoryInput):                              # Does directory exist?
        print("File Path Exists") 
    else:
        print("File Path Does Not Exist: Would You Like to Enter a new directiory?")    # Path Does NOT EXIST
        newDirectory = input
        folderInspection(newDirectory)                              # If User wants to enter new directory, program will send the new directory to be inspected


def imageRetrieval(directoryInput, images_retrieved):               # Function Retrieves Images from Directory and Stores In 'images_retrieved' array
    imageIntegrity(images_retrieved)                                # Sends Retrieved Images to get checked for file integrity
    for f in glob.iglob(directoryInput):
        print('found ' + f)
        images_retrieved.append(f)                                  # Adds Image to Array


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