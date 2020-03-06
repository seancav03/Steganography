import sys, getopt
from PIL import Image

def main(argv):
	saveFile = ""
	inputFile = argv[-1]
	if(inputFile[0] != '-'):
		argv = argv[0:-1]
	try:
		opts, args = getopt.getopt(argv,"o:",["help"])
	except getopt.GetoptError:
		sys.exit("INVALID INPUT: Correct arguments and try again. Note: last argument must be input file")

	for opt, arg in opts:
		if opt == "--help":
			sys.exit("--help   Displays the usage text and exits\n-o <output>  Outputs the unencoded data to a text file.  This is an optional parameter, so if it's missing then display the text on the screen.\n<file>   The file to decode")
		elif opt == "-o":
			saveFile = arg
	try:
		imageIN = Image.open(inputFile)
	except:
		sys.exit("Failed to Open Image file. Did you put the correct file name as the last argument?")
	image = imageIN.convert("RGB")
	currentCharNum = 0
	spotInChar = 0
	message = ""
	isFirst = True
	endCombo = [127, 10, 13]
	is13 = 0

	dataType = 0

	# JPEG support
	imageArr = []
	imageRow = []
	pixel = []
	endRowCombo = [10, 13, 127]
	is127 = 0

	for y in range(0, image.size[1]):
		for x in range(0, image.size[0]):
			tup = image.getpixel((x, y))
			for v in tup:
				val = v & 3
				val = val << (2*spotInChar)
				currentCharNum = currentCharNum | val
				spotInChar+=1
				if(spotInChar > 3):
					if( not isFirst):
						if(currentCharNum == endCombo[is13]):
							is13+=1
						else:
							is13 = 0
						theChar = chr(currentCharNum)
						if(dataType == 1 or dataType == 2):
							message += theChar
						elif(dataType == 3):
							if(currentCharNum == endRowCombo[is127]):
								is127+=1
							else:
								is127 = 0
							pixel.append(currentCharNum)
							if(len(pixel) >= 3):
								imageRow.append(pixel)
								pixel = []
							if(is127 > len(endRowCombo)-1):
								imageRow = imageRow[:-3]
								imageArr.append(imageRow)
								imageRow = []
								is127 = 0
						currentCharNum = 0
					else:
						dataType = currentCharNum
						isFirst = False
						currentCharNum = 0
					spotInChar = 0
			if(is13 > len(endCombo)-1):
				break
		if(is13 > len(endCombo)-1):
			break

	if(dataType == 1 or dataType == 2):
		message = message[:-3]
		if(saveFile == ""):
			print(message)
		else:
			text_file = open("saveFile" + ".txt", "w")
			text_file.write(message)
			text_file.close()
	elif(dataType == 3):
		imgObj = Image.new("RGB", (len(imageArr[0]), len(imageArr)))
		img = imgObj.load()
		for rowNum in range(0, len(imageArr)):
			row = imageArr[rowNum]
			for pixelNum in range(0, len(row)):
				pixel = row[pixelNum]
				# Build Image
				img[pixelNum, rowNum] = (pixel[0], pixel[1], pixel[2])
		if(saveFile == ""):
			imgObj.show()
		else:
			imgObj.save(saveFile + ".jpg")


if __name__ == "__main__":
	main(sys.argv[1:])