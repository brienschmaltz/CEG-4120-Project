from removeLabel import *
from email.mime import image
from PIL import Image
from tqdm import tqdm

import time
import glob
import os, os.path
import cv2 as cv2
import numpy as np

# ------------------------------------------------------------------- *** MAIN ***
def main(): #                                                           


    mainMenu() # START MAIN MENU
    goToOutput = input("Press Y/y to Open Output Directory.")               # OPEN OUTPUT
# ------------------------------------------------------------------- Function mainMenu() - Purpose:
def mainMenu():                                                             # Start Program
    print("*** Image Cleanup Tool V.1.0 ***")                               # Menu Screen

    images_retrieved = []                                                   # Array of Images Extracted from Folder
    directoryInput = input ("Enter Image/s Retrieval Directory:")           # User Input of Retrieval Directory
    folderInspection(directoryInput, images_retrieved)
    print("\nCurrent Images Stored: ")
    print(images_retrieved)
    
    # imageIntegrity(images_retrieved)   # Check image extensions before sending to CV2

    print("Images After Check")
    print(images_retrieved)



    imageToCV2(images_retrieved)                                            # After imageRetrieval completion program sends imported images array to CV2 editor

# ------------------------------------------------------------------- Function imageToCV2() - ASHTONS CODE + ITERATOR | Removes Labels & Text From Images:
def imageToCV2(images_retrieved):                                       
    imageCounter = 1
    for i in tqdm(images_retrieved):                                        # Traversing through the image loop to find each image and pass forward to removeLabel
        img = cv2.imread(i) 

        result = removeLabel(img) 
# To show that the original size/resolution of the images are maintained
        print("Image Shape: " + (str)(img.shape))
        print("Result Shape: " + (str)(result.shape))

        cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        cv2.namedWindow('result', cv2.WINDOW_NORMAL)
        cv2.imshow("image", img)
        cv2.imshow("result", result)

        cv2.imwrite("D:\GITHUB\CEG-4121-Project\Mak's Work\OutputImages\result" + str(image) + ".jpg", result)

        #for laptop
        #cv2.imwrite("C:/Users/ashto/OneDrive/Desktop/CEG 6120 Managing the Software Process/Group E Project/Output Images/" + "MASK" + image, mask)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

        print("Image: " + i + " Processed")
        imageCounter += 1
        time.sleep(0.05)

# ------------------------------------------------------------------- Function folderInspection() - Purpose: Checks to see if 'directoryInput' path exists
def folderInspection(directoryInput, images_retrieved):                     # Function designed to check if folder exists
    print("Checking Folder Path (" + directoryInput + ")...")

    if os.path.exists(directoryInput):                                      # Does directory exist?
        print("\n-----------------> File Path Check: OK") 
        directoryInput = directoryInput + '\*'                              # the addition of '*' symbol is proper semantics when accessing files in folders
        imageRetrieval(directoryInput, images_retrieved)                    # Sending directyInput & the array to store the images in to the image retrieval function
    else:
        print("\n-----------------> File Path Check: * FAIL * -> Path Does Not Exist")
        newDirectory = input("Please Enter a new directiory: ")
        folderInspection(newDirectory, images_retrieved)                    # If User wants to enter new directory, program will send the new directory to be inspected

# ------------------------------------------------------------------- Function imageRetrieval() - Purpose: Enters directory and extracts images into images_received
def imageRetrieval(directoryInput, images_retrieved):                       # Function Retrieves Images from Directory and Stores In 'images_retrieved' array
    for f in glob.iglob(directoryInput):
        print('found ' + f)
        images_retrieved.append(f)                                          # Adds Image to Array
    
    imageIntegrity(images_retrieved)                                        # Sends Retrieved Images to get checked for file integrity


def whatsIsInside(images_retrieved):
    for f in images_retrieved :
        print(f)


# ------------------------------------------------------------------- Function imageIntegrity() - Purpose: Checks Images collected in images_received array for file integrity
def imageIntegrity(images_retrieved):
    print("\n-----------------> Now Checking File Integrity")                                    # Debug Purposes
    
    print("BEFORE LOOP WHAT IS INSIDE ARRAY")
    whatsIsInside(images_retrieved)

    index = 0
    lengthOfArray = len(images_retrieved)
    for i in range(lengthOfArray):

        print('\nchecking ', end= "")                                         # DEBUG purposes
        print(index)                                                           # DEBUG purposes
        
        split_extension = os.path.splitext(images_retrieved[index])[1].lower()                   # Split the extension from the path and normalise it to lowercase.
        print("Split Extension: ", end="")
        print(split_extension)

        # print("Split = ", end= "")
        # print(split_extension)
        # print(" ")
            
        if split_extension != '.tif' or  split_extension != ".png":                                     # Checks if File is of correct extentsion

            print("File Integrity: * FAIL * for image-> " , end= "")
            print(images_retrieved[index]) 
            print("Accepted Extensions: .tif - .png\n")

            print("Removing Image...")
            if index != 0:
                index -= 1

            images_retrieved.remove(images_retrieved[index])   # Pops out (Removes) image with incorrect extension

            if len(images_retrieved) == 0:
                print("-- NO IMAGES REMAINING IN INPUT FOLDER --")
                exit(0)

            print("REMOVED: ", end="")
            print(images_retrieved[index])


            print("INSIDE LOOP WHAT IS INSIDE ARRAY")
            whatsIsInside(images_retrieved)

        else :
            print("File Integrity: OK -> ", end= "")
            print(images_retrieved[index]) 
            print(" ")   
            index += 1
            print("Index: ", end="")
            print(index)

        

    print("AFTER LOOP WHAT IS INSIDE ARRAY")
    whatsIsInside(images_retrieved)                              
    
# ------------------------------------------------------------------- Function ShowImage() - Purpose: Display Image To User || Debugging
def showImage(images_retrieved):                                            # Shows user current image
    for images in images_retrieved:
        images.show()                                                       # Shows image received / Debug purposes


# ------------------------------------------------------------------- Function Main() - Sets "Main()" as the primary driver to the program
if __name__ == "__main__":
    main()