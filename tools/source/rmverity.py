#!/usr/bin/env python3
#
# remverity - by SuperR.
#
# Do not edit this file unless you know what you are doing

import os
import sys
import re
from shutil import copyfile

filename = None
vstatus = None

if len(sys.argv) > 1:
    filename = sys.argv[1]
if len(sys.argv) > 2:
    vstatus = sys.argv[2]

if not filename:
    print('Usage: rmverity.py boot.img [stats]')
    sys.exit()

def existf(filename):
	try:
		if os.path.isdir(filename):
			return 2
		if os.stat(filename).st_size > 0:
			return 0
		else:
			return 1
	except OSError:
		return 2

if existf(filename) != 0:
    print('No '+filename)
    sys.exit()

# if existf(filename+'.bak') != 0:
#     print('Backing up '+filename+' ...')
#     copyfile(filename, filename+'.bak')

wflag = None
with open(filename, 'rb') as f:
    data = f.read()

thechk = b'\x2c\x76\x65\x72\x69\x66\x79'
if re.search(thechk, data):
    if vstatus:
        print('yes')
        sys.exit()

    print('Removing dm-verity from '+filename+' ...')
    result = {}
    for i in re.finditer(thechk, data):
        begin = i.start()
        bnum = 7
        while True:
            if data[begin + bnum] == 0:
                result[data[begin:bnum + begin]] = b'\x00'*bnum
                break
            elif data[begin+bnum:begin+bnum+1] == b'\n':
                result[data[begin:bnum + begin]] = b''
                break
            else:
                bnum = bnum + 1
        
    for swap in list(result):
        data = data.replace(swap, result[swap])

    wflag = 1
else:
    if vstatus:
        print('no')
        sys.exit()
    
if wflag:
    with open(filename+'_new', 'wb') as o:
        devnull = o.write(data)
    os.replace(filename+'_new', filename)
    print('\n'+filename+' patched\n')
else:
    print('\nNo changes made to '+filename+'\n')