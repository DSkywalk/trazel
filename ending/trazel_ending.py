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
from shutil import copyfile
import re
from binascii import hexlify, unhexlify
from table_end import TABLE, SAFE, ENDVAL, ORIGINAL_PTR, MAXSIZE


"""
T2O. xE0200 a xE8129 (bytes 32554) (tope xE8200)
T2P. xE0200 a xE7D23 (bytes 31524)
T2B. xE0200 a xE81FC (bytes 32765)
"""

"""
END. x73F4C a x742E1 (bytes 917)
"""

HEXA = ['A', 'B', 'C', 'D', 'E', 'F', '1', '2', '3', '4', '5', '6', '7', '8', '9' , '0']
sTxtTmpFile = "txt.tmp"
sBinTmpFile = "bin.tmp"


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


def getEnding(sRomFile, sUserFile, iStartPtr, iStartData, iBufsize=1024, iTexts=16):
    fp1 = open(sRomFile,'rb')
    fp1.seek(iStartPtr)
    pointers = []
    # first get pointers from ptr table
    for _i in range(iTexts + 1):
        data_h = fp1.read(1)
        data_l = fp1.read(1)
        key = hexlify(data_l + data_h).upper()
        # print key, int(key, 16), iStartData + int(key, 16)
        pointers.append( int(key, 16) )
    fp1.close()

    return pointers, iTexts

def dumpEndingPhrase(sRomFile, sUserFile, iStart, iLength, iBufsize=1024):
    print iStart, iLength
    fp1 = open(sRomFile,'rb')
    fp1.seek(iStart)
    fp2 = open(sUserFile,'a')
    line_end = 0
    while iLength > 0:
        for __i in range(4):
            data = fp1.read(1)
            key = hexlify(data).upper()
            fp2.write("{%s}" % key)
            if __i == 3:
                line_end = (int(key, 16) + 1) / 2
                print "end:", line_end
        for c in range(line_end):
            data = fp1.read(1)
            key = hexlify(data).upper()
            value = TABLE.get(key, "{%s}" % key)
            fp2.write(value)
        fp2.write("\n")
        iLength -= line_end + 4
    fp2.write("\n")
    fp2.write("\n")
    fp1.close()
    fp2.close()


def replaceText(sUserFile, iStart, iLength, iBufsize=1024):
    lTable = sorted(TABLE.items(), key=lambda x: -len(x[1])) # ordered from lenght (reversed)
    lnum = range(0, 256)
    with open(sUserFile, 'r') as content_file:
        content = content_file.read()
        ftmp = open(sTxtTmpFile, "wb")
        
        # convert windows line-breaks to linux
        content = re.sub(r"\r\n","\n", content)
        
        # replace table values
        for (key, value) in lTable:
            if len(value) < 2 and value in HEXA: # first loop ignore hexa chars
                continue
            replace = "{%s}" % key
            # print "subs: %s to %s" % (value, replace)
            content = content.replace(value, replace)

        if not content[0] == "{":
            print "First char warning, check your dump and table again..."
            

        # replace HEXADECIMAL values using regex
        while len(HEXA):
            for char in HEXA:
                bFound = False
                for (key, value) in lTable:
                    if value == char:
                        bFound = True
                        replace = "{%s}" % key
                        (content, match) = re.subn(r'(})([\w]*)('+ char +')', r'\g<1>\g<2>' + replace, content)
                        if not match:
                            HEXA.remove(char)
                if not bFound:
                    HEXA.remove(char)

        ftmp.write(content)
        ftmp.close()


def getTextData():
    with open(sTxtTmpFile, "r") as fptxt:
        iText = 1
        iLine = 0
        ending = False
        oData = {}
        lData = []
        for line in fptxt:
            iLine += 1
            # prepare content
            content = line[:-1]
            for i in range(0, 256):
                value = "{%s}" % hexlify(chr(i)).upper()
                key = chr(i)
                #print "subs: %s to %s" % (value, i)
                content = content.replace(value, key)

            # check custom ending value
            if content[-1] == '\xff':
                content = content[:-1]
                ending = True

            # ((len - header_size) * data_size) -1
            iTotalSize = len(content)
            iPhraseSize = ((iTotalSize - 4) * 2) -1
            print iLine, "size:", iTotalSize, "[", hex(iPhraseSize), "]"
            
            # save new length
            tmpList = list(content)
            tmpList[3] = chr(iPhraseSize)
            #content = ''.join(tmpList)
            
            lData.extend(tmpList)
            
            if ending:
                # print lData, len(lData), hex(len(lData))
                oData[iText] = lData
                iText += 1
                ending = False
                lData = []
        return oData
            

def dumpToBinary(sUserFile, oData, iStart, iBufsize=1024):
    with open(sUserFile, "rb+") as f:
        f.seek(iStart)
        f.write(oData)


def fillBinary(sUserFile, iLeft, iPos, iValue):
    content = ""
    print "Bytes at %x left: %i (Filled with 0x%s)" % (iPos, iLeft, ENDVAL)

    while iLeft:
        content += unhexlify(ENDVAL)
        iLeft -= 1
    dumpToBinary(sUserFile, content, iPos)
    

def convertLittle(iValue):
    sValue = '%04x' % iValue
    lValue = [ chr(int(x, 16)) for x in [sValue[2:], sValue[:-2]] ]
    return ''.join(lValue)


def replaceBinary(sUserFile, iStartPtr, iStartData, iBufsize=1024):
    iValue = iStartData - ORIGINAL_PTR
    iMaxPos = iValue + MAXSIZE

    iPosPtr = iStartPtr # 0x742E1
    iPosData = iStartData # 0x73F4C

    # get text data
    oData = getTextData()
    
    print "0", hex(iValue), hex(iPosPtr)
    dumpToBinary(sUserFile, convertLittle(iValue), iPosPtr)

    for idx, data in oData.iteritems():
        iPosPtr += 2
        iValue += len(data)
        if iValue > iMaxPos:
            print " OVERFLOW IGN:", iValue, hex(iValue)
            continue

        print idx, hex(iValue), hex(iPosPtr), hex(iPosData)

        # write new ptr
        dumpToBinary(sUserFile, convertLittle(iValue), iPosPtr)
        # write new content
        dumpToBinary(sUserFile, ''.join(data), iPosData)

        iPosData += len(data)
    
    iLeft = iMaxPos - iValue
    if iLeft > 0:
        content = ""
        print "Bytes left: %i (Filled with 0x%s)" % (iLeft, ENDVAL)

        while iLeft:
            content += unhexlify(ENDVAL)
            iLeft -= 1
        dumpToBinary(sUserFile, content, iPosData)

    elif iLeft < 0:
        print "WARNING OVERWRITEN BYTES:", abs(iLeft)


def usage():
    print "usage:"
    print " # slice binary - outputs a binary part"
    print sys.argv[0] + " <romfile> -s <start addr> <end addr> <outfile> "
    print " # convert a memory zone to text using table.py"
    print sys.argv[0] + " <romfile> -d <ptr addr> <data addr> <txtfile> "
    print " # replace a memory zone using text and table.py into a new rom file"
    print sys.argv[0] + " <romfile> -r <ptr addr> <data addr> <txtfile> <newrom>"
    print " D_Skywalk - GPLv3"

def genFile(args):
    firstAddr = int(args[3], 16)
    lastAddr =  int(args[4], 16)
    dumpSize = (lastAddr - firstAddr)

    if args[2] == "-s":
        sliceFile(args[1], args[5], firstAddr, dumpSize )
        print "Slice: OK"
    elif args[2] == "-d":
        # clean new file
        fp2 = open(args[5],'w')
        fp2.close()
        # get rom data
        ptrs, iTexts = getEnding(args[1], args[5], firstAddr, lastAddr )
        # loop over data
        for i in range(iTexts):
            dataSize = (ptrs[i + 1] - ptrs[i])
            dumpEndingPhrase(args[1], args[5], lastAddr + ptrs[i], dataSize)
        print "Dump: OK"
    elif args[2] == "-r" and len(args) == 7:
        ptrs, iTexts = getEnding(args[1], args[5], firstAddr, lastAddr )
        textAddr = lastAddr + ptrs[0]
        dumpSize = ptrs[-1] - ptrs[0]
        print "init:", textAddr, " size:", dumpSize
        copyfile(args[1], args[6])
        replaceText(args[5], textAddr, dumpSize)
        # getTextData(0)
        replaceBinary(args[6], firstAddr, lastAddr)
        # print "Replace: OK"
    else:
        usage()

if __name__ == '__main__':
    if len(sys.argv) < 5:
        usage()
    else:
        genFile(sys.argv)

