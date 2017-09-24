#!/usr/bin/python
'''
 unsparse.py
 Copyright (C) 2017  Nathan Rennie-Waldock <nathan.renniewaldock@gmail.com>
'''
import xml.etree.ElementTree as ET
from natsort import natsorted

from time import time
import sys, os
import argparse

def is_file (f):
	if not os.path.exists(f):
		msg = "%s doesn't exist" % (f)
		raise argparse.ArgumentTypeError(msg)
	return f

def mksize (bytes):
	suffixes = ("B", "kB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
	suffixesLen = len(suffixes)

	for i in range(suffixesLen):
		if bytes < pow(1000, i + 1) or i + 1 == suffixesLen:
			return "%.2f %s" % (float(bytes) / pow(1024, i), suffixes[i])


def copyfileobj (fsrc, fdst, bufsize=16384, filesize=None):
	progress = 0
	percent = 0
	lastpercent = 0

	lasttime = time()
	lastprogress = 0

	lastprogress_speed = 0
	speed = 0

	eta = None

	while True:
		buf = fsrc.read(bufsize)
		if not buf:
			break
		fdst.write(buf)
		if filesize:
			progress += len(buf)
			timenow = time()
			elapsed = (timenow - lasttime)
			if elapsed >= 1: # Average it over 1 second
				speed = ((progress - lastprogress_speed) / elapsed) * (1/elapsed)
				lasttime = timenow
				lastprogress_speed = progress

				eta = "%d secs" % ((filesize - progress) / speed)

			percent = int((float(progress) / filesize) * 100)

			if percent != lastpercent:
				bar = ""
				barlen = 50
				if percent == 100:
					bar = "=" * barlen
				else:
					scaled_percent = percent/(100/barlen)
					for i in range(barlen):
						if i < scaled_percent-1:
							bar += "="
						elif i < scaled_percent:
							bar += ">"
						else:
							bar += " "

				print "%d%% [%s] %s (%s/s) %s          \r" % (percent, bar, mksize(progress), mksize(speed) if speed else "-.-- MB", "eta " + eta if eta and percent < 100 else ""),
				sys.stdout.flush()

				lastpercent = percent
			lastprogress = progress
	print

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Copyright (C) 2017  Nathan Rennie-Waldock <nathan.renniewaldock@gmail.com>\n"
												 "This program comes with ABSOLUTELY NO WARRANTY;\n"
												 "This is free software, and you are welcome to redistribute it\n"
												 "under certain conditions.", formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument("-x", "--xml", type=is_file, default="rawprogram0.xml", help="XML file to parse for partitions (default: rawprogram0.xml)")
	group = parser.add_mutually_exclusive_group()
	group.add_argument("-p", "--partition", type=str, default="", help="Partition to assemble (default: all)")
	group.add_argument("-l", "--list", action="store_true", help="List found partitions")
	parser.add_argument("-o", "--output", metavar="DIRECTORY", default=".", help="Output directory (default: Current directory)")
	args = parser.parse_args()

	all_partitions = args.partition == "" or args.partition == "all"
	base = os.path.dirname(args.xml)
	output = args.output
	if not os.path.isdir(output):
		os.makedirs(output)
	xml = ET.parse(args.xml)
	
	partitions = {}
	for e in xml.findall("program"):
		attribs = e.attrib
		label = attribs["label"]
	
		if not attribs["filename"]:
			continue
	
		try:
			start_sector = long(attribs["start_sector"])
		except ValueError:
			continue
	
		if label not in partitions:
			partitions[label] = []
	
		partitions[label].append(
			{
				"filename": attribs["filename"],
				"sectors": attribs["num_partition_sectors"],
				"start_sector": start_sector,
				"sector_size": long(attribs["SECTOR_SIZE_IN_BYTES"])
			}
		)
	
	for k, v in partitions.items():
		partitions[k] = natsorted(v, key=lambda key: key["start_sector"])
	

	known_partitions = []
	for label, parts in partitions.items():
		if len(parts) > 1:
			known_partitions.append(label)

	if args.list:
		print "Known partitions: %s" % (" ".join(known_partitions))
		sys.exit()

	if not all_partitions and args.partition not in partitions:
		print "ERROR: Partition %s not found" % (args.partition)

		print "Known partitions: %s" % (" ".join(known_partitions))
		sys.exit(1)

	for label, parts in partitions.items():
		if not all_partitions and label != args.partition:
			continue
		if len(parts) > 1:
			with open(os.path.join(output, label + ".img"), "w+b") as f:
				partition_start = parts[0]["start_sector"]
				for part in parts:
					seek = part["sector_size"] * (part["start_sector"] - partition_start)
					f.seek(seek)
					copyfileobj(open(os.path.join(base, part["filename"]), "rb"), f, 16384, os.path.getsize(part["filename"]))

					print "%s: %s, start %d" % (label, part["filename"], (part["start_sector"] - partition_start))
	
