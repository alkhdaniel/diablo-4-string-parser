import json

def readHeader(f):                                      #48 bytes
    bundle = f.read(8)                                  #not sure but some file type identifier
    f.read(4)                                           #padding bytes
    f.read(4)                                           #some type of file id identifier
    f.read(1)                                           #no clue
    fileid = f.read(2)                                  #this ID links to cousin files in meta/ folder
    f.read(1)                                           #padding
    f.read(12)                                          #padding bytes
    f.read(4)                                           #dont know, seems to always be 32, some kind of block size or something?
    infoLength = int.from_bytes(f.read(4), "little")    #infoblock byte length, divide by 40 to get total keyvalue pairs
    f.read(8)                                           #padding bytes
    return infoLength
    
def readInfoBlock(f):                               #40 bytes
    f.read(8)                                       #padding bytes
    unknown1 = f.read(4)                            #dont know
    keyLen = int.from_bytes(f.read(4), "little")    #key name length
    f.read(8)                                       #padding bytes
    unknown2 = f.read(4)                            #dont know
    valLen = int.from_bytes(f.read(4), "little")    #value string length
    f.read(8)                                       #padding bytes
    return [keyLen, valLen]

def readKeyValue(f, keyLen, valLen):
    key=f.read(keyLen-1)                                #read the key name
    f.read((8-(f.tell()%8))%8)                          #padding bytes (pads until the next 8th position)
    val=f.read(valLen-1)                                #read the value
    f.read((8-(f.tell()%8))%8)                          #padding bytes (pads until the next 8th position)
    return [key.decode("utf8"), val.decode("utf8")]
    

with open('enUS_Text/meta/StringList/Power_Sorcerer_Hydra.stl', 'rb+') as f:
    infoLength = readHeader(f)                                      #for now readHeader only returns the length of infoblocks
    keyValuePairs = int(infoLength/40)                              #how many keyvalue pairs the file contains
    keyValueLens = []                                               #we store the keyvalue lengths here
    for i in range (0, keyValuePairs):
        keyValueLens.append(readInfoBlock(f))                       #get key and value length info for all pairs and store it
    textmap = {}                                                    #we store the final parsed file in here
    for i in range (0, keyValuePairs):                              #loop all keyvalue pairs
        keyvalue = readKeyValue(f, keyValueLens[i][0], keyValueLens[i][1])  #grab the keyvalue pair text
        textmap[keyvalue[0]] = keyvalue[1]                                  #insert current pair into the textmap
    json_object = json.dumps(textmap, indent = 4)                   #convert all the data to json object
    print(json_object)                                              #print it out to console for now
