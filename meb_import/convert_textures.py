import os

from functools import partial
from genericpath import exists

from numpy import numarray


from .binary_stream import BinaryStream
from math import radians


class attr:
    def __init__(self, ID, type, val, num_values, nextArr):
        self.ID = ID
        self.type = type
        self.val = val
        self.num_values = num_values
        self.nextArr = nextArr


STRSoffset = 0
ATTRarr = []
NUMBarr = []
filesize = 0


def readBLMY(filename):
    ATTRarr = []
    NUMBarr = []

    num_attr = 0
    num_numb = 0

    f = filename
    # print(f.tell())
    stream = BinaryStream(f)

    f.seek(4, 1)
    numChunks = stream.readULong()
    filesize = stream.readULong()
    f.seek(4, 1)

    for i in range(0, numChunks):
        CHname = ""
        for w in range(0, 4):
            CHname += chr(int.from_bytes(stream.readByte(), 'big'))
        CHsize = stream.readULong()
        CHoffset = stream.readULong()
        f.seek(4, 1)

        currentOffset = f.tell()
        f.seek(CHoffset, 1)

        if CHname == 'HEAD':
            num_elmt = stream.readULong()
            num_attr = stream.readULong()
            num_coll = stream.readULong()
            num_numb = stream.readULong()
            num_strs = stream.readULong()
            unknown1 = stream.readULong()
            unknown2 = stream.readULong()
        elif CHname == 'ATTR':
            for i in range(0, num_attr):
                ID = stream.readULong()
                type = stream.readULong()
                val = stream.readULong()
                num_values = stream.readULong()
                nextAttr = stream.readULong()
                ATTRarr.append(attr(ID, type, val, num_values, nextAttr))
        elif CHname == 'NUMB':
            for i in range(0, num_numb):
                NUMBarr.append(stream.readFloat())
        elif CHname == 'STRS':
            STRSoffset = CHoffset
        f.seek(currentOffset, 1)


def renfiles(dir):
    realname = ''

    for file in os.listdir(dir):
        if file.lower().endswith(".bmt"):
            f = open(file, "rb")
            readBLMY(f)
            
            stream = BinaryStream(f)
            for i in range(0, len(ATTRarr)):
                if ATTRarr[i].id == -974381262:
                    if ATTRarr[i+1] is not None:
                        f.seek(ATTRarr[i+1].val + STRSoffset, 1)
                        realname = stream.readStr()
            f.close()
            



OBJpos = [0, 0, 0]
OBJscale = 1.0
OBJorient = {'x': 0, 'y': 0, 'z': 0, 'w': 1}

def readCarBML(filename):
    f = filename

    stream = BinaryStream(f)    
    readBLMY(filename)
    
    OBJpos = [0, 0, 0]
    
    for i in range(0, len(ATTRarr)):
        OBJscale = 1.0
        if   ATTRarr[i].id == 773578924:
            OBJpos = [NUMBarr[(ATTRarr[i].val+1)], NUMBarr[(ATTRarr[i].val+2)], NUMBarr[(ATTRarr[i].val+3)]]
        
        elif ATTRarr[i].id == -351767367:
            OBJorient = quat NUMBarr[(ATTRarr[i].val+1)] NUMBarr[(ATTRarr[i].val+2)] NUMBarr[(ATTRarr[i].val+3)] NUMBarr[(ATTRarr[i].val+4)]
            
        elif ATTRarr[i].id == 1933617737: 
            OBJscale = NUMBarr[(ATTRarr[i].val+1)]
        
        elif ATTRarr[i].id ==  1259803821:
            fseek f (ATTRarr[i].val + STRSoffset) #seek_set
            mebname = filenameFromPath (readstring f)
            if (LODtest mebname) == true do importPart (modelPath + mebname) OBJpos OBJorient OBJscale

        elif ATTRarr[i].id == -263649155:
            fseek f (ATTRarr[i-1].val + STRSoffset) #seek_set
            modelName = readstring f


        selective_import.importprogress.value = 95.*i/ATTRarr.count + 5
    )
    fclose f
    if selective_import.ren.checked do
    (
        renameFile filename (modelPath + modelName + ".vhf.BML")
        vhfFiles = getfiles (modelPath + "*.vhf")
        if vhfFiles.count == 1 do
        (
            renameFile vhfFiles[1] (modelPath + modelName + ".vhf")
        )
    )