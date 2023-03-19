import json

def readHeader(f):                                      #48 bytes
    game = f.read(4)                                    #some kind of game identifier
    filetype = f.read(4)                                #some kind of file type identifier
    f.read(4)                                           #padding bytes
    f.read(4)                                           #???
    hashid = f.read(4)                                  #hashId, links to cousin files in meta/ folder
    f.read(12)                                          #padding bytes
    f.read(4)                                           #dont know, seems to always be 32, some kind of block size or something?
    infoLength = int.from_bytes(f.read(4), "little")    #infoblock byte length, divide by 40 to get total keyvalue pairs
    f.read(8)                                           #padding bytes
    return infoLength


def readOffset(f, offset, length):
    curOffset = f.tell()
    f.seek(offset)
    thisString = f.read(length)
    f.seek(curOffset)
    return thisString.decode("utf-8")
    
def readInfoBlock(f):                               #40 bytes
    f.read(8)                                       #padding bytes
    keyOffset = int.from_bytes(f.read(4), "little") #key name file offset
    keyLen = int.from_bytes(f.read(4), "little")    #key name length
    keyString = readOffset(f, keyOffset+16, keyLen) #grab the key string
    f.read(8)                                       #padding bytes
    valOffset = int.from_bytes(f.read(4), "little") #value string file offset
    valLen = int.from_bytes(f.read(4), "little")    #value string length
    valString = readOffset(f, valOffset+16, valLen) #grab the value string
    f.read(8)                                       #padding bytes
    return [keyString, valString]

with open('enUS_Text/meta/StringList/AchievementsUI.stl', 'rb+') as f:
    infoLength = readHeader(f)                                      #for now readHeader only returns the length of infoblocks
    keyValuePairs = int(infoLength/40)                              #how many keyvalue pairs the file contains
    textmap = {}                                                    #we store the final parsed file in here
    for i in range (0, keyValuePairs):
        keyValuePair = readInfoBlock(f)                             #grab the keyvalue pair text
        textmap[keyValuePair[0]] = keyValuePair[1]                  #insert current pair into the textmap
    json_object = json.dumps(textmap, indent = 4)                   #convert all the data to json object
    print(json_object)                                              #print it out to console for now
