'''
Created April 4, 2013
@author: Richard Crissup
'''
import sys
import binascii
import struct
from array import array

class Header(object):
    ''' '''
    version = '0.1'
    
    def __init__(self, f=None, *args, **kwargs):
        ''' '''
        if f:
            self.f = f
        self.__curPostion = int()
        self.symbol = str()
        self.ifdOffset = int()
        
    def get(self,f=None):
        ''' '''
        if f:
            self.f = f
        
        self.__curPostion = self.f.tell()
        
        self.f.seek(0)
        __endian = self.f.read(2).upper()
        if __endian == 'II':
            self.symbol = '<'
        elif __endian == 'MM':
            self.symbol = '>'
        
        if struct.unpack(self.symbol+'h', self.f.read(2))[0] != 42:
            raise Exception('Not a valid tiff file - failed 42 test')
        
        self.ifdOffset = struct.unpack(self.symbol+'l',self.f.read(4))[0]
        
        self.f.seek(self.ifdOffset)
        #self.numIfds = struct.unpack(self.symbol+'h',self.f.read(2))[0]
        
        self.f.seek(self.__curPostion)

class IFD(object):
    ''' '''
    version = '0.1'
    
    def __init__(self, f=None, offset=None, *args, **kwargs):
        ''' '''
        #Subclass header?
        
        if f:
            self.f = f
            self.H = Header()
        self.H.get(self.f)
        
        self.imageWidth = tuple()
        self.imageLength = tuple()
        self.bitsperSample = tuple()
        self.security = tuple()
        self.tileWidth = tuple()
        self.tileLength = tuple()
        self.tileOffsets = tuple()
        self.tileBytes = tuple()
        self.geoKey = tuple()
        self.header = tuple()
        
    
    def get(self, f=None):
        '''  '''
        if f:
            self.f = f
 
        __cur = self.f.tell()
        self.f.seek(self.H.ifdOffset)
        self.numIfds = struct.unpack(self.H.symbol+'h',self.f.read(2))[0]
        print self.f.tell()

        for entry in xrange(self.numIfds):
            data = struct.unpack(self.H.symbol+'HHLL',self.f.read(12))
            tag = data[0]
            #data = _tag, _type, _count, _offset
            print data
            
            if tag == 256: #Image Width
                self.imageWidth = data
            elif tag == 257: #Image Length
                self.imageLength = data
            elif tag == 258: #Bit per Sample
                self.bitsperSample = data
            elif tag == 270: #Security
                self.security = data
            elif tag == 305: #Software
                pass
            elif tag == 322: #Tile Width
                self.tileWidth = data
            elif tag == 323: #Tile Length
                self.tileLength = data
            elif tag == 324: #Tile Offsets
                self.tileOffsets = data
            elif tag == 325: #Tile Bytes
                self.tileBytes = data
            elif tag == 34735: #GEOKEY Header
                self.geoKey = data
            elif tag == 34737: #NGA Header
                self.header = data
        
        self.f.seek(__cur)
    
def gettile(f,length,width,offset):
    '''
    returns a 2d array of int values representing a tile
    '''
    cur = f.tell()
    f.seek(offset)
    scanline = 0
    tile = []
    while scanline < length:
        data = array('h')
        #read to the right
        data.read(f, width)
        tile.append(data)
        scanline += 1
    f.seek(cur)
    return tile

        