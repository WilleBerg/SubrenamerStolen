#!/usr/bin/env python3

'''
Author: Eshaan Bansal
github: github.com/eshaan7
						 WHAT THE SCRIPT DOES:
	You download a TV show from torrent and find the suitable subtitle files from some website.
	Renaming every subtitle file to match the video file is a pain in the ass, isn't it?
	That's where this script comes in handyy
'''

import os
import s_logging
#import msvcrt

s_logging.setup("subRenamer.log", 10)
log = s_logging.log

def menu():
	print("\t"+"*"*8+"MENU"+"*"*8)
	print("\n\t"+"-"*20)
	print("\tFor subs and video files,")
	print("\t1. In same directory")
	print("\t2. In different directory")
	print("\t3. In current directory: {0}".format(os.getcwd()))
	print("\t4. or good one")
	print("\t"+"-"*20)
	choice = int(input("\n\tEnter choice(1-3): "))
	return choice

def diff_path(): #choice=2
	vid_path = str(input("Full path to video directory(example: /home/...): "))
	sub_path = str(input("Full path to subtitles directory(example: /home/...): "))
	sub_format = str(input("Extension of subtitle files(ex: .sub, .srt, etc): "))
	vidFiles = []
	subFiles = []
	for name in os.listdir(vid_path):
		if (name.endswith('.mp4') or name.endswith('.mkv') or name.endswith('.avi')):
			vidFiles.append(name)
	for name in os.listdir(sub_path):
		if (name.endswith(sub_format)):
			subFiles.append(name)
	rename_files(sub_path, vidFiles, subFiles, sub_format)
	return 

def same_path(): #choice=1
	dir_path = str(input("Full path to video directory(example: /home/...): "))
	sub_format = str(input("Extension of subtitle files(ex: .sub, .srt, etc): "))
	dirFiles = os.listdir(dir_path)
	log(dirFiles)
	vidFiles = []
	subFiles = []
	for name in dirFiles:
		if (name.endswith('.mp4') or name.endswith('.mkv') or name.endswith('.avi')):
			vidFiles.append(name)
		elif (name.endswith(sub_format)):
			subFiles.append(name)
	rename_files(dir_path, vidFiles, subFiles, sub_format)
	return

def for_current_dir(): #choice=3
	dir_path = os.getcwd()
	dirFiles = os.listdir(dir_path)
	log(dir_path)
	log(dirFiles)
	vidFiles = []
	subFiles = []
	sub_format = str(input("Extension of subtitle files(ex: .sub, .srt, etc): "))
	for name in dirFiles:
		if (name.endswith('.mp4') or name.endswith('.mkv') or name.endswith('.avi')):
			vidFiles.append(name)
		elif (name.endswith(sub_format)):
			subFiles.append(name)
	rename_files(dir_path, vidFiles, subFiles, sub_format)
	return

def fillList(subList, vidList):
	if len(vidList) == 0:
		return None
	for i in range(len(subList)):
		vidList.append(vidList[0][0:len(vidList[0]) - 4] + "_" + str(i + 1) + vidList[0][len(vidList[0]) - 4:])
		if len(vidList) == len(subList):
			break
	vidList[0] = vidList[0][0:len(vidList[0]) - 4] + "_0" + vidList[0][len(vidList[0]) - 4:]
	log("fixed vidList: {0}".format(vidList))
	return vidList


def for_nested_folders(root, sub_format):
	log("\n\nNEW FILE\n\n")
	dir_path = root
	log("Current root" + dir_path)
	dirFiles = os.listdir(dir_path)
	log("Dirfiles:")
	log(dirFiles)
	newList = []
	for files in dirFiles:
		log("Current file: " + files)
		if os.path.isdir(root + "/" +files):
			log(files + " is a directory")
			for_nested_folders(root=(root + "/" +files), sub_format=sub_format)
			log("Removing directory: {0}".format(files))
		else: 
			log(files + " is not a directory")
			newList.append(files)
	dirFiles = newList
	log("No dirs left")
	log("Trying to rename files")
	vidFiles = []
	subFiles = []
	for name in dirFiles:
		if (name.endswith('.mp4') or name.endswith('.mkv') or name.endswith('.avi')):
			vidFiles.append(name)
		elif (name.endswith(sub_format)):
			subFiles.append(name)
	if len(subFiles) > len(vidFiles):
		vidFiles = fillList(subFiles, vidFiles)
	if vidFiles == None:
		return
	log("vidFiles: {0}".format(vidFiles))
	log("subFiles: {0}".format(subFiles))
	rename_files(dir_path, vidFiles, subFiles, sub_format)	
			
	log("Returning to parent directory")
	return



def rename_files(path, vidFiles, subFiles, sub_format):
	#vidFiles.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
	#subFiles.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
	os.chdir(path)
	try:
		assert(len(subFiles)==len(vidFiles))
		for i,vname in enumerate(vidFiles):
			print("{0} renamed to {1} ".format(subFiles[i], os.path.splitext(vname)[0]))
			log("{0} renamed to {1} ".format(subFiles[i], os.path.splitext(vname)[0]))
			os.rename(subFiles[i], os.path.splitext(vname)[0]+sub_format)
	except AssertionError:
		print(len(subFiles))
		print(len(vidFiles))
	#print("\nPress Q to Quit")
	#msvcrt.getch()
	return 

def main():
	choice = menu()
	if choice==1:
		same_path()
	elif choice==2:
		diff_path()
	elif choice==3:
		for_current_dir()
	elif choice==4:
		sub_format = str(input("Extension of subtitle files(ex: .sub, .srt, etc): "))
		for_nested_folders(os.getcwd(), sub_format)
		
main()
