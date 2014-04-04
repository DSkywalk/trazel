#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
   Copyright (C) 2014 David Colmenero - D_Skywalk
    http://david.dantoine.org

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 3 of the License, or
   higher any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program; if not, write to the Free Software Foundation,
   Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA
"""

import sys, os
import re
from binascii import hexlify, unhexlify
from table import TABLE, SAFE, ENDVAL


"""
T2O. xE0200 a xE8129 (bytes 32554) (tope xE8200)
T2P. xE0200 a xE7D23 (bytes 31524) 
T2B. xE0200 a xE81FC (bytes 32765)
"""

HEXA = ['A', 'B', 'C', 'D', 'E', 'F', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9' ]
sTmpFile = "bin.tmp"

def sliceFile(sRomFile, sUserFile, iStart, iLength, iBufsize=1024):
    fp1 = open(sRomFile,'rb')
    fp1.seek(iStart)
    fp2 = open(sUserFile,'wb')
    init = 0
    while iLength:
        chunk = min(iBufsize,iLength)
        #print " c: %i | l: %i a: %s" % ( chunk, iLength , hex(init))
        data = fp1.read(chunk)
        fp2.write(data)
        iLength -= chunk
        init += chunk

    print "ended at " + hex(init)
    fp1.close()
    fp2.close()


def dumpText(sRomFile, sUserFile, iStart, iLength, iBufsize=1024):
    fp1 = open(sRomFile,'rb')
    fp1.seek(iStart)
    fp2 = open(sUserFile,'w')
    while iLength:
        data = fp1.read(1)
        key = hexlify(data).upper()
        value = TABLE.get(key, "{%s}" % key)
        fp2.write(value)
        iLength -= 1

    fp1.close()
    fp2.close()


"""
TODO: using buffer for big files
"""
def replaceText(sRomFile, sUserFile, iStart, iLength, iBufsize=1024):
    lTable = sorted(TABLE.items(), key=lambda x: -len(x[1])) # ordered from lenght (reversed)
    lnum = range(0, 256)
    with open(sUserFile, 'r') as content_file:
        content = content_file.read()
        ftmp = open(sTmpFile, "wb")
        
        # convert windows line-breaks to linux
        content = re.sub(r"\r\n","\n", content)
        
        # replace table values
        for (key, value) in lTable:
            if len(value) < 2 and value in HEXA: # first loop ignore hexa chars
                continue
            replace = "{%s}" % key
            #print "subs: %s to %s" % (value, replace)
            content = content.replace(value, replace)

        if not content[0] == "{":
            print "First char warning, check your dump and table again..."
            
        # replace HEXADECIMAL values using regex
        while len(HEXA):
            for char in HEXA:
                for (key, value) in lTable:
                    if value == char:
                        replace = "{%s}" % key
                        (content, match) = re.subn(r'(})([\w]*)('+ char +')', r'\g<1>\g<2>' + replace, content)
                        if not match:
                            HEXA.remove(char)


        # remove last \n insert by editors
        if content[-1] == '\n':
            content = re.sub(r"\n$","", content)

        # convert {xx} to binary
        for i in lnum:
            value = "{%s}" % hexlify(chr(i)).upper()
            key = chr(i)
            #print "subs: %s to %s" % (value, i)
            content = content.replace(value, key)

        iLeft = (iLength - len(content))
        print "Bytes left: %i (Filled with 0x%s)" % (iLeft, ENDVAL)
        while iLeft:
            content += unhexlify(ENDVAL)
            iLeft -= 1

        ftmp.write(content)
        ftmp.close()

def replaceBinary(sRomFile, sUserFile, iStart, iLength, iBufsize=1024):
    fp1 = open(sRomFile,'rb')
    fp1.seek(0, os.SEEK_END)
    iSize = fp1.tell() # get file size, os.stat is for lusers ¬_¬
    fp1.seek(0, os.SEEK_SET)
    fp2 = open(sUserFile,'wb')
    
    if (iStart + iLength) > iSize:
        print "Size Error, check your arguments..."
        return 0

    init = 0

    # first part...
    iCounter = iStart
    while iCounter:
        chunk = min(iBufsize,iCounter)
        data = fp1.read(chunk)
        fp2.write(data)
        iCounter -= chunk
        init += chunk

    fp1.close()
    print "1. ended at " + hex(init)

    # Second part...
    fp1 = open(sTmpFile,'rb')
    fp1.seek(0, os.SEEK_END)
    iTmpSize = fp1.tell()
    fp1.seek(0, os.SEEK_SET)

    while iTmpSize:
        chunk = min(iBufsize,iTmpSize)
        data = fp1.read(chunk)
        fp2.write(data)
        iTmpSize -= chunk
        init += chunk

    print "2. ended at " + hex(init)


    fp1.close()

    # Third part...
    fp1 = open(sRomFile,'rb')
    fp1.seek(init, os.SEEK_SET)
    iSize -= init
    while iSize:
        chunk = min(iBufsize,iSize)
        data = fp1.read(chunk)
        fp2.write(data)
        iSize -= chunk
        init += chunk

    print "3. ended at " + hex(init)

    fp1.close()
    fp2.close()


def usage():
    print "usage:"
    print " # slice binary - outputs a binary part"
    print sys.argv[0] + " <romfile> -s <start addr> <end addr> <outfile> "
    print " # convert a memory zone to text using table.py"
    print sys.argv[0] + " <romfile> -d <start addr> <end addr> <txtfile> "
    print " # replace a memory zone using text and table.py into a new rom file"
    print sys.argv[0] + " <romfile> -r <start addr> <end addr> <txtfile> <newrom>"
    print " D_Skywalk - GPLv3"

def genFile(args):
    firstPos = int(args[3], 16)
    lastPos =  int(args[4], 16)
    dumpSize = (lastPos - firstPos)

    if args[2] == "-s":
        sliceFile(args[1], args[5], firstPos, dumpSize )
        print "Slice: OK"
    elif args[2] == "-d":
        dumpText(args[1], args[5], firstPos, dumpSize )
        print "Dump: OK"
    elif args[2] == "-r" and len(args) == 7:
        replaceText(args[1], args[5], firstPos, dumpSize )
        replaceBinary(args[1], args[6], firstPos, dumpSize )
        print "Replace: OK"
    else:
        usage()

if __name__ == '__main__':
    if len(sys.argv) < 5:
        usage()
    else:
        genFile(sys.argv)

