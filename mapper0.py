#!/usr/bin/env python

import sys
import os
import re

for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    # split the line into words
    words = line.split()

    for word in words:
        string = re.sub(r"[\W_\d]", "",word)
        string = string.lower()
        if(string != ""):
            print '%s\t%s' % (string, 1)
