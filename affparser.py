#drop folder with .aff files on top, there may still be some bugs in this im not sure
import json
import sys
import os

blockLength = 44                                                        #the amount of bytes in one infoblock

def readInt(f, length):                                                 #read length bytes from file f and convert it to an integer
    return int.from_bytes(f.read(length), "little")

def readString(f, length):                                              #read length bytes from file f and convert it to a string
    return f.read(length).decode("utf-8")

def readOffset(f, offset, length):                                      #reads length bytes at specified offset from file f, and then puts cursor back at its old position
    curOffset = f.tell()
    f.seek(offset)
    thisString = f.read(length)
    f.seek(curOffset)
    return thisString
    

def readHeader(f):                                                      #
    game = f.read(4)                                                    #some kind of game identifier
    filetype = f.read(4)                                                #some kind of file type identifier
    f.read(4)                                                           #padding bytes
    f.read(4)                                                           #???
    hashid = readInt(f, 4)                                              #hashId, links to cousin files in meta/ folder
    f.read(124)                                                         #i dont know what this is and i dont intend to find out right now
    infoOffset = readInt(f,4)+16                                        #the offset infoblocks start at
    infoLength = readInt(f,4)                                           #how many bytes the info blocks take up (divide this number by blockLength to get amount of keys)
    f.read(104)                                                         #i dont know what this is and i dont intend to find out right now
    return [infoOffset, infoLength]
    
def readInfoBlock(f):                                                   #44 bytes
    startOffset = f.tell()
    #dont ask about this
    f.read(20)
    if (startOffset%8 == 0):
        f.read(4)

    keyOffset = readInt(f, 4)                                           #key name file offset
    keyLen = readInt(f, 4)                                              #key name length
    keyString = readOffset(f, keyOffset+16, keyLen).decode("utf-8")     #grab the key string

    #dont ask about this
    if (startOffset%8 == 4):
        f.read(4)
    return keyString

indir = sys.argv[1]
textmap = {}
for filename in os.listdir(indir):
    with open(os.path.join(indir, filename), 'rb+') as f:
        infoBlocks = readHeader(f)                                      #offset at array index 0, length at index 1
        keyValuePairs = int(infoBlocks[1]/blockLength)                  #how many keyvalue pairs the file contains
        thisTextmap = []                                                #we store the final parsed file in here
        f.seek(infoBlocks[0])                                           #info blocks start at the offset we got earlier
        for i in range (0, keyValuePairs):
            thisTextmap.append(readInfoBlock(f))
            print(thisTextmap)
        textmap[filename] = thisTextmap
        print(filename+" Parsed")
json_object = json.dumps(textmap, indent = 4, ensure_ascii=False).replace(r'\u0000', '')    #convert all the data to json object (and remove trash \u0000 from it)
with open('AffList.json', 'w', encoding="utf8") as f:
    f.write(json_object)
