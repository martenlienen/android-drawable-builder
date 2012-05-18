#!/usr/bin/env python

import argparse
import glob
import os
import shutil

# Mapping from a dpi category to an export dpi relative to the default DPI in inkscape and CSS3 in the ratio 3:4:6:8
dpiMap = {
	"ldpi": 67.5,
	"mdpi": 90,
	"hdpi": 135,
	"xhdpi": 180
}
dpiCategories = dpiMap.keys()

parser = argparse.ArgumentParser(description="Dynamically create drawables from svg files")
parser.add_argument("--src", nargs=1, required=True, help="Directory where your svg templates are saved")
parser.add_argument("--out", nargs=1, required=True, help="Directory where the png images will be exported to")

args = parser.parse_args()
src = args.src[0]
res = args.out[0]

def contains (string, strings):
	for search in strings:
		if string.find(search) is not -1:
			return True
	return False

def isSvgFile (file):
	return file.lower().endswith(".svg")

def scaleSvg (svgFile, resDir, drawableDirName, dpiMap):
	dpiCategories = dpiMap.keys()
	strippedFilename = os.path.basename(os.path.splitext(svgFile)[0])

	for category in dpiCategories:
		categorizedDir = os.path.join(resDir, drawableDirName + "-" + category)

		if not os.path.exists(categorizedDir):
			os.makedirs(categorizedDir, exist_ok=True)

		dpi = dpiMap[category]
		exportPath = os.path.join(categorizedDir, strippedFilename + ".png")
		os.system("inkscape --file=" + svgFile + " --export-area-page --export-dpi=" + str(
			dpi) + " --export-png=" + exportPath)

def expandDir (fromDir, toDir, dirName):
	for file in glob.glob(os.path.join(fromDir, dirName, "*")):
		if not os.path.isfile(file):
			continue
		if isSvgFile(file):
			scaleSvg(svgFile=file, resDir=res, drawableDirName=dirName, dpiMap=dpiMap)
		else:
			dstDir = os.path.join(toDir, dirName)
			if not os.path.exists(dstDir):
				os.makedirs(name=dstDir)
			shutil.copy(src=file, dst=dstDir)

def copyTree (src, dst):
	if not os.path.exists(dst):
		os.makedirs(dst)

	if not os.path.isdir(dst):
		return

	for root, dirs, files in os.walk(src):
		relativeRoot = os.path.relpath(path=root, start=src)
		print(root, dirs, files)
		for file in files:
			shutil.copy(src=os.path.join(root, file), dst=os.path.join(dst, relativeRoot))
		for dir in dirs:
			os.mkdir(os.path.join(dst, relativeRoot, dir))

nonCategorizedDirs = []
dpiCategorizedDirs = []

for path in glob.glob(os.path.join(src, "drawable*")):
	dirName = os.path.basename(path)
	if contains(dirName, dpiCategories):
		dpiCategorizedDirs.append(dirName)
	else:
		nonCategorizedDirs.append(dirName)

for dirName in nonCategorizedDirs:
	expandDir(fromDir=src, toDir=res, dirName=dirName)

for dirName in dpiCategorizedDirs:
	copyTree(src=os.path.join(src, dirName), dst=os.path.join(res, dirName))