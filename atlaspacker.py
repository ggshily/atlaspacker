#!/usr/bin/env python
import sys, os, argparse
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="The file(s) or folder you want to convert into a TextureAtlas", type=str)
parser.add_argument("-o", "--output", help="The filename to use in the resulting TextureAtlas files", type=str)
parser.add_argument("-f", "--filter", help="What kind of texture filter to use in the configuration file. (default: Nearest)", type=str, choices=["linear", "nearest"])
args = parser.parse_args()
if os.path.isdir(args.input):
	print os.path.abspath(args.input)
