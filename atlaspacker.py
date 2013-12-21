#!/usr/bin/env python
try:
	from PIL import Image
except ImportError:
	print "ERROR: Pillow library not found."
	sys.exit(0)
import math, sys, os, argparse

parser = argparse.ArgumentParser()
parser.add_argument("input", help="The file(s) or folder you want to convert into a TextureAtlas", type=str, nargs="+")
#parser.add_argument("output", help="The filename to use in the resulting TextureAtlas files", type=str)
parser.add_argument("-f", "--filter", help="Type of filter to use in the configuration files. (Default: Nearest)", type=str, choices=["linear", "nearest"])
parser.add_argument("-s", "--spacing", help="Amount of empty space (in pixels) between the images in the TextureAtlas", type=int)
args = parser.parse_args()

#CONSTANTS
#List of supported image types
IMAGETYPES = [".png", ".jpg", ".gif", ".bmp"]
#Max image size
MAXSIZE = (2048, 2048)



#List containing image objects in the directory
atlasImages = []

#FUNCTIONS
def pointDistance(a, b):
	return math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)

#Create a list of image files in the files/folders the user entered
for arg in args.input:
	if os.path.isdir(arg):
		folderContents = os.listdir(arg)
		for entry in folderContents:
			if os.path.splitext(entry)[-1] in IMAGETYPES:
				currentImage = Image.open(os.path.join(arg, entry))
				atlasImages.append({"file": os.path.join(arg, entry), "size": currentImage.size, "position":None, "image": currentImage})
	elif os.path.isfile(arg):
		if os.path.splitext(arg)[-1] in IMAGETYPES:
			currentImage = Image.open(arg)
			atlasImages.append({"file": arg, "size": currentImage.size, "position":None, "image": currentImage})
#Sort the list based on the largest size of the image
atlasImages = sorted(atlasImages, key=lambda img: max(img["size"][0], img["size"][1]))
#Reverse the list so the larger images come first
atlasImages.reverse()

for i in atlasImages:
	print i
	
"""

#Create image
finalImage = Image.new("RGBA", (2048, 2048))
for image in atlasImages:
	#print "Writing", image["file"], "at", image["position"]
	finalImage.paste(image["image"], image["position"])
finalImage.save("result.png")	

"""


















'''
for image in atlasImages:
	print "Processing", image["file"]
	for point in anchorPoints:
		for pImage in processedImages:
			if not (point[0] >= pImage["position"][0]+pImage["size"][0] or 
					point[0]+image["size"][0] <= pImage["position"][0] or
					point[1] >= pImage["position"][1]+pImage["size"][1] or
					point[1]+image["size"][1] <= pImage["position"][1]):
						anchorPoints.remove(point)
	anchorPoints = sorted(anchorPoints, key=lambda point: pointDistance(point, (0, 0)))
	image["position"] = anchorPoints[0]
	processedImages.append(image)
	anchorPoints.pop(0)
	topRight = (image["position"][0] + image["size"][0], image["position"][1])
	bottomLeft = (image["position"][0], image["position"][1] + image["size"][1])
	anchorPoints.append(topRight)
	anchorPoints.append(bottomLeft)
	anchorPoints = sorted(anchorPoints, key=lambda point: pointDistance(point, (0, 0)))

#Create image
finalImage = Image.new("RGBA", (2048, 2048))
for image in atlasImages:
	print "Writing", image["file"], "at", image["position"]
	finalImage.paste(image["image"], image["position"])
finalImage.save("result.png")	

'''

































