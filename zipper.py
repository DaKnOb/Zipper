#!/usr/bin/python
from __future__ import division

import os,time,sys
import argparse

parser = argparse.ArgumentParser(
	description="""
	Determine the optimal amount of layers a compression tool like zip(1) or 
	gzip(1) must run for a specific file size containing specific data.
	""",
	formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument(
	"--startunit",
	help="The initial file size to check for",
    type=int,
    default=1)
parser.add_argument(
	"--endunit",
	help="The maximum file size to check for",
	type=int,
	default=100)
parser.add_argument(
	"--startzip",
	help="The minimum amount of compression layers to apply",
	type=int,
	default=1)
parser.add_argument(
	"--endzip",
	help="The maximum amount of compression layers to apply",
	type=int,
	default=10)
parser.add_argument(
	"--zipwith",
	help="The tool to use(zip, gzip)",
	default="gzip")
parser.add_argument(
	"--sourcefile",
	help="The file from which Zipper will read data",
	default="/dev/zero")
parser.add_argument(
	"--unitsize",
	help="""The units in which Start Unit and End Unit are measured.
	Possible values are b(512), kB(1000), K(1024), MB(1000*1000), M(1024*1024),
	GB(1000*1000*1000), and G(1024*1024*1024)
	""",
	default='B')
parser.add_argument(
	"--timestorun",
	help="""Define how many times each command will run. When set to higher 
	values than 1, the time measured will be the average of all runs.""",
	type=int,
	default=1)

args = parser.parse_args()

StartUnit = args.startunit
EndUnit = args.endunit
StartZIP = args.startzip
EndZIP = args.endzip

ZipWith = '|' + args.zipwith
SourceFile = args.sourcefile

UnitSize = args.unitsize
TimesToRun = args.timestorun or 1 # To prevent running zero times

####

def totalBytes(size, unitSize):
	'''
	Converts size with unitSize such K, MB, M, etc
	into respective total bytes
	'''
	multipliers = {
		'b':512,
		'kB': 1000,
		'K': 1024,
		'MB': 1000*1000,
		'M': 1024*1024,
		'GB': 1000*1000*1000,
		'G': 1024*1024*1024,
	}

	return size * multipliers.get(unitSize, 1)



def writeCSV(s,f):
	sys.stdout.write(s)
	fi = open(f, "a+")
	fi.write(s)
	fi.close()

def silentRemove(filename):
	try:
		os.remove(filename)
	except OSError:
		pass

TimeTable = []
StorageTable = []
for t in range(0, (EndUnit - StartUnit + 1)):
	TimeTable.append([])
	StorageTable.append([])

for size in range(StartUnit, EndUnit+1):
	for times in range(StartZIP, EndZIP+1):
		FileName = str(size) + UnitSize + "." + str(times) + "T.gz"
		command = "head -c " + str(totalBytes(size, UnitSize)) + " " + SourceFile
		command = command + (ZipWith * times)
		command = command + ">" + FileName
		print(command)

		# Run command TimesToRun times and calculate average
		TotalTime = 0
		for i in range(TimesToRun):

			# Delete file created by previous run of same command
			# Run this first because we may want to read size of the file
			# created after execution ends
			silentRemove(FileName)

			init = time.time()
			os.system(command)
			end = time.time()

			TotalTime += end - init

		AverageTime = TotalTime / TimesToRun
		print(" Ran: " + str(TimesToRun) + " times")
		print(" Took: " + str(AverageTime) + " seconds")
		print(" Size: " + str(os.path.getsize(FileName)) + " bytes")
		TimeTable[size - StartUnit].append(AverageTime)
		StorageTable[size - StartUnit].append(os.path.getsize(FileName))

os.system("rm -vfR *.gz > /dev/null 2> /dev/null")

print("Generating Storage CSV File...")
open("size.csv", "w+").close()

writeCSV("X", "size.csv")
for size in range(StartZIP, EndZIP + 1):
	writeCSV("," + str(size) + " Layers", "size.csv")
writeCSV("\n", "size.csv")
InitialLayer = StartUnit
for size in StorageTable:
	writeCSV(str(InitialLayer) + " " + UnitSize + "B", "size.csv")
	InitialLayer = InitialLayer + 1
	for layer in size:
		writeCSV("," + str(layer), "size.csv")
	writeCSV("\n", "size.csv")
sys.stdout.flush()

print("Generating Time CSV File...")
open("time.csv", "w+").close()

writeCSV("X", "time.csv")
for size in range(StartZIP, EndZIP + 1):
	writeCSV("," + str(size) + " Layers", "time.csv")
writeCSV("\n", "time.csv")
InitialLayer = StartUnit
for size in TimeTable:
	writeCSV(str(InitialLayer) + " " + UnitSize + "B", "time.csv")
	InitialLayer = InitialLayer + 1
	for layer in size:
		writeCSV("," + str(layer), "time.csv")
	writeCSV("\n", "time.csv")
sys.stdout.flush()
