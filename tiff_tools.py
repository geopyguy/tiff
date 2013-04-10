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
        self.numIfds = int()
        
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
        self.numIfds = struct.unpack(self.symbol+'h',self.f.read(2))[0]
        
        self.f.seek(self.__curPostion)

class IFD(object):
    ''' '''
    version = '0.1'
    
    def __init__(self, f=None, *args, **kwargs):
        ''' '''
        #Subclass header?
        
    def get(self, f=None):
        ''' '''
        pass
    
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

        