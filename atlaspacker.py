#!/usr/bin/env python

########################################################################
#
# Copyright(C) 2014 Sandro Luiz S. de Paula <me@ansdor.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# For more information, see <http://www.gnu.org/licenses/>.
#
########################################################################

#Check if Pillow is available, do necessary imports
import math, sys, os, argparse
try:
	from PIL import Image
except ImportError:
	print("ERROR: PIL/Pillow library not found.")
	sys.exit(0)

#Argparser stuff
parser = argparse.ArgumentParser()
parser.add_argument("input", help="The file(s) or folder you want to convert into a TextureAtlas", type=str, nargs="+")
parser.add_argument("output", help="Filename for the TextureAtlas files", type=str)
parser.add_argument("-f", "--filter", help="Type of filter to use in the configuration files. (Default: Nearest)", type=str, choices=["linear", "nearest"])
parser.add_argument("-p2", "--powerof2", help="Force power-of-2 sized output image.",  action="store_true")
parser.add_argument("-sq", "--square", help="Force square output image.", action="store_true")
parser.add_argument("-o", "--overwrite", help="Overwrite existing files with the same name without any prompts.", action="store_true")
parser.add_argument("-s", "--spacing", help="amount of space (in pixels) between the sprites", type=int)
args = parser.parse_args()

#CONSTANTS
#List of supported image types
IMAGETYPES = [".png", ".jpg", ".gif", ".bmp"]
#Max image size
MAXSIZE = (8192, 8192)

#ARGUMENTS
if args.spacing:
    SPACING = args.spacing
else:
    SPACING = 0
#Force square output
FORCESQUARE = args.square
#Force po2 output
FORCEPO2 = args.powerof2
#Overwrite without prompts
OVERWRITE = args.overwrite
if args.filter:
    IMAGEFILTER = args.filter.capitalize()
else:
    IMAGEFILTER = "Nearest"

#Yes & No strings
YESSTRINGS = ("Yes", "yes", "YES", "Y", "y")
NOSTRINGS = ("No", "no", "NO", "N", "n")

#FUNCTIONS
#Returns the distance between two points
def pointDistance(a, b):
	return math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)

#Searches the input arguments (files, folders) for supported image types and returns a list with their data.
def getImages(target):
    finalList = []
    for item in target:
        if os.path.isdir(item):
            dirContents = os.listdir(item)
            for entry in dirContents:
                if os.path.splitext(entry)[-1] in IMAGETYPES:
                    currentImage = Image.open(os.path.join(item, entry))
                    finalList.append({"file": os.path.join(item, entry), "size": currentImage.size, "position":None, "image": currentImage})
       	elif os.path.isfile(item):
            if os.path.splitext(item)[-1] in IMAGETYPES:
                currentImage = Image.open(item)
                finalList.append({"file": item, "size": currentImage.size, "position":None, "image": currentImage})
    return finalList

#Finds the best cell to pack an image.        
def findCell(img, cells, size):
    for cell in cells:
        if cell["position"][0]+img["size"][0] <= size[0] and cell["position"][1]+img["size"][1] <= size[1]:
            if img["size"][0] <= cell["size"][0] and img["size"][1] <= cell["size"][1]:
                return cell
    for cell in cells:
        if img["size"][0] <= cell["size"][0] and img["size"][1] <= cell["size"][1]:
            return cell
    return None

if args.output[-4:] == ".png":
    outputFilename = args.output
else:
    outputFilename = args.output + ".png"

if os.path.isfile(outputFilename) and not OVERWRITE:
    while True:
        print("File", outputFilename, "already exists, overwrite?")
        answer = raw_input("(Y/n):\t")
        if answer in NOSTRINGS:
            sys.exit(0)
        elif answer in YESSTRINGS or answer == "":
            break
        else:
            print("ERROR: Invalid answer.")
        

#Create a list of image files in the files/folders the user entered
atlasImages = getImages(args.input)
if atlasImages == []:
    print("ERROR: Input doesn't contain any image files.")
    sys.exit(0)
#Sort the list based on the largest size of the image
atlasImages = sorted(atlasImages, key=lambda img: max(img["size"][0], img["size"][1]))
#Reverse the list so the larger images come first
atlasImages.reverse()

freeCells = [{"size": MAXSIZE, "position": (SPACING, SPACING)}]
baseSize = (SPACING, SPACING)
for image in atlasImages:
    packedCell = findCell(image, freeCells, baseSize)
    if packedCell:
        image["position"] = packedCell["position"]
        
        vcell = {
        "size": (image["size"][0], packedCell["size"][1]-(image["size"][1]+SPACING)),
        "position": (packedCell["position"][0], packedCell["position"][1]+image["size"][1]+SPACING)
        }
        
        hcell = {
        "size": (packedCell["size"][0]-(image["size"][0]+SPACING), packedCell["size"][1]),
        "position": (packedCell["position"][0]+image["size"][0]+SPACING, packedCell["position"][1])
        }
        
        freeCells.append(vcell)
        freeCells.append(hcell)
        freeCells.remove(packedCell)

        if image["position"][0]+image["size"][0] > baseSize[0]:
            baseSize = (image["position"][0]+image["size"][0], baseSize[1])
        if image["position"][1]+image["size"][1] > baseSize[1]:
            baseSize = (baseSize[0], image["position"][1]+image["size"][1])
    else:
        print("Unable to pack", image["file"])
    for cell in freeCells:
        if cell["position"][0] >= MAXSIZE[0] or cell["position"][1] >= MAXSIZE[1]:
            freeCells.remove(cell)
    freeCells = sorted(freeCells, key=lambda cell: pointDistance(cell["position"], (0, 0)))

baseSize = (baseSize[0]+SPACING, baseSize[1]+SPACING)

if FORCEPO2:
    a = 1
    while 2**a < baseSize[0]:
        a += 1
    b = 1
    while 2**b < baseSize[1]:
        b += 1
    baseSize = (2**a, 2**b)

if FORCESQUARE:
    baseSize = (max(baseSize), max(baseSize))

#Create image
finalImage = Image.new("RGBA", baseSize)
for image in atlasImages:
    if image["position"] != None:
        finalImage.paste(image["image"], image["position"])
finalImage.save(outputFilename)

tFile = open(os.path.splitext(outputFilename)[0] + ".txt", "w")
tFile.write(outputFilename + "\nformat: RGBA8888")
tFile.write("\nfilter: " + IMAGEFILTER + "," + IMAGEFILTER)
tFile.write("\nrepeat: none")
for image in atlasImages:
    tFile.write("\n" + os.path.split(image["file"])[-1][:-4])
    tFile.write("\n  rotate: false")
    tFile.write("\n  xy: " + str(image["position"][0]) + ", " + str(image["position"][1]))
    tFile.write("\n  size: " + str(image["size"][0]) + ", " + str(image["size"][1]))
    tFile.write("\n  orig: " + str(image["size"][0]) + ", " + str(image["size"][1]))
    tFile.write("\n  offset: 0, 0")
    tFile.write("\n  index: -1")
