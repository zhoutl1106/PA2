#!/usr/bin/env python

import sys
import os
import re

lineNum = 1

filestop = open('stops.txt','rt')
stopList = filestop.readline().strip().split()

for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    # split the line into words
    words = line.split()
    # increase counters
    offset = 1;
    for word in words:
        # write the results to STDOUT (standard output);
        # what we output here will be the input for the
        # Reduce step, i.e. the input for reducer.py
        #
        # tab-delimited; the trivial word count is 1
        filename = os.environ['mapreduce_map_input_file']
        filestart = os.environ['mapreduce_map_input_start']
        string = re.sub(r"[\W_\d]", "",word)
        string = string.lower()
        #filelen = os.environ['mapreduce_map_input_length']
        if(string != "" and string not in stopList):
            print '%s\t%s\t%s\t%s\t%s' % (string, filename, filestart, lineNum, offset)
        offset = offset + 1
    lineNum = lineNum + 1
