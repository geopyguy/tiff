'''
Created April 4, 2013
@author: Richard Crissup
'''
import struct
from array import array
import numpy

class _Header(object):
    ''' '''
    version = '0.1'
    
    def __init__(self, f, *args, **kwargs):
        ''' '''
        self.f = f
        self.__curPostion = int()
        self.symbol = str()
        self.ifdOffset = int()
        
    def get(self):
        ''' '''
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

        self.f.seek(self.__curPostion)

class IFD(object):
    ''' '''
    version = '0.1'
    
    def __init__(self, f, offset=None, *args, **kwargs):
        ''' '''
        #Subclass header?
        self.f = f
        self.H = _Header(self.f)
        self.H.get()
        self.symbol = self.H.symbol
        
        self.imageWidth = tuple()
        self.imageLength = tuple()
        self.bitsperSample = tuple()
        self.security = tuple()
        self.resolutionUnit = tuple()
        self.Width = tuple()
        self.Length = tuple()
        self.tileOffsets = tuple()
        self.tileBytes = tuple()
        self.modelTiepoint = tuple()
        self.geoKey = tuple()
        self.header = tuple()
        
        self.tileWidth = int()
        self.tileLength = int()
        self.tilesAcross = int()
        self.tilesDown = int()
        self.tilesPerImage = int()
        
        self.pixelWidth = int()
            
    def get(self, f=None):
        '''  '''
        if f:
            self.f = f
 
        __cur = self.f.tell()
        self.f.seek(self.H.ifdOffset)
        self.numIfds = struct.unpack(self.H.symbol+'h',self.f.read(2))[0]
        print self.numIfds
        
        for entry in xrange(self.numIfds):
            data = struct.unpack(self.H.symbol+'HHLL',self.f.read(12))
            tag = data[0]
            
            if tag == 256: #Image Width
                self.imageWidth = data
            elif tag == 257: #Image Length
                self.imageLength = data
            elif tag == 258: #Bit per Sample
                self.bitsperSample = data
            elif tag == 270: #Security
                self.security = data
            elif tag == 296: #Resolution Unit
                self.resolutionUnit = data
            elif tag == 305: #Software
                pass
            elif tag == 322: #Tile Width
                self.Width = data
            elif tag == 323: #Tile Length
                self.Length = data
            elif tag == 324: #Tile Offsets
                self.tileOffsets = data
            elif tag == 325: #Tile Bytes
                self.tileBytes = data
            elif tag == 33922: #Model Tie Point
                self.modelTiepoint = data
            elif tag == 34735: #GEOKEY Header
                self.geoKey = data
            elif tag == 34737: #NGA Header
                self.header = data
        
        self.tilesAcross = (self.imageWidth[3] + self.Width[3] - 1) / self.Width[3]
        self.tilesDown = (self.imageLength[3] + self.Length[3] -1) / self.Length[3]
        self.tilesPerImage = self.tilesAcross * self.tilesDown
        self.tileWidth = self.Width[3]
        self.tileLength = self.Length[3]
        
        self.f.seek(__cur)
        
class Tile(object):
    '''A image tile'''
    '''This could also be a generator for each scanline?'''
    __version = '1'
    def __init__(self, imagefile, length, width, offset, x, y):
        '''Tile(imagefile, tilelength, tilewidth, fileoffset, x, y)
        x, y = x,y coord of the upper left corner'''
        
        self.f = imagefile
        self.len = length
        self.wid = width
        self.off = offset
        self.x = x
        self.y = y
        
        self.xFactor = 1
        self.yFactor = 1
        
        self.data = []
        self.index = []
        self.cartCoords = []
        self.coords = []
        self.npData = None
        self.zeroLocations = []
        
        self._gettiledata()
        self.npData = numpy.array(self.data)
        
    def _gettiledata(self):
        '''
        get the tile data from the raster...
        called by __init__'''
        cur = self.f.tell()
        self.f.seek(self.off)
        scanline = 0
        
        while scanline < self.len:
            #data = array('h')
            data = array('l')
            data.read(self.f, self.wid)
            self.data.append(data)
            print self.data
            exit()
            scanline += 1
        self.f.seek(cur)
        
    def createZeroindex(self):
        '''read through scanlines finding zeros
        index array will be blank if no zeros are found
        index = (scanline, [zero positions])'''
        self.index = []
        scanline = 0
        while scanline < self.len:
            indexList = []
            zeroFlag = False
            for index, pixel in enumerate(self.data[scanline]):
                
                #find where values turn to zero
                if pixel == 0 and not zeroFlag:
                    zeroFlag = True
                    indexList.append(index)
                    
                #find where values turn from zero
                elif pixel != 0 and not zeroFlag:
                    indexList.append(index)
                
                else:
                    pass
                
                if pixel != 0:
                    zeroFlag = False
            self.index.append((scanline, indexList))
            scanline += 1
    
    def _createcartesiancoords(self):
        '''create cartesian coords for scanline'''
        self.cartCoords = []
        
        for scanline in self.index:
            y, index = scanline
            points = []
            for x in index:
                points.append((x, y))
            self.cartCoords.append(points)
            
    def _set_x_y_factor(self):
        '''set the x,y factor constants to 1 or -1 '''
        #Get these values from reading if the UL coords are - or +
        pass
    
    @staticmethod
    def xAdjust(xcoord, width, cellsize, column_number):
        '''adjust x coord, adding tile(s) width as needed'''
        x = (column_number * (width * cellsize)) + abs(xcoord)
        if xcoord < 0:
            x = x * -1
        return x
    
    @staticmethod
    def yAdjust(ycoord, length, cellsize, row_number):
        '''adjust the y coord, adding tile(s) length as needed'''
        y = (row_number * (length * cellsize)) + abs(ycoord)
        if ycoord < 0:
            y = y * -1
        return y
    
    def createcoords(self, pixelwidth = None):
        '''create coords for the tile'''
        self.coords = []
        
        self._createcartesiancoords()
        print 'cartCoords','len', len(self.cartCoords), self.cartCoords
        #NOTE need to get the UL coords here and pixel width
        
        #NOTE need to determine the negativeness values that control - or + for coord
        #determined from the UL coordinates

        #Note do i need this? need to actually use this function...
        self._set_x_y_factor()        
        self.xFactor = -1
        self.yFactor = 1
        
        for scanline in self.cartCoords:
            if scanline:
                for coord in scanline:
                    x, y = coord
                    
                    if self.xFactor < 0:
                        newX = (abs(self.x) - (x * pixelwidth)) * self.xFactor
                    else:
                        newX = (abs(self.x) + (x * pixelwidth)) * self.xFactor
                        
                    #This assumes the pixel is square...if not need to use pixel length value
                    if self.yFactor < 0:
                        newY = (abs(self.y) + (y * pixelwidth)) * self.yFactor
                    else:
                        newY = (abs(self.y) - (y * pixelwidth)) * self.yFactor
                        
                    self.coords.append((newX, newY))
                    
            else:
                print 'empty scanline add edge points?'
        #Add the origin point at the end to close the polygon? 
        #self.coords.append((self.x, self.y))
        

def gettileoffsets(f, obj):
    '''
    f = file
    obj = IFD.tileoffsers tuple
    returns array of tile offsets
    '''
    offsets = array('l')
    cur = f.tell()
    f.seek(obj[3])
    offsets.read(f, obj[2])
    f.seek(cur)
    return offsets.tolist()
    
# def gettile(f,tileLength, tileWidth, offset):
#     '''
#     returns a 2d array of int values representing a tile
#     '''
#     cur = f.tell()
#     f.seek(offset)
#     scanline = 0
#     tile = []
#     while scanline < tileLength:
#         data = array('h')
#         #read to the right
#         data.read(f, tileWidth)
#         tile.append(data)
#         scanline += 1
#     f.seek(cur)
#     return tile
# 
# def leftzeroindex(_list):
#     '''
#     find the leftmost position of valid pixels
#     returns None if all values in _list are 0
#     '''
#     index = 0
#     for pixel in _list:
#         if pixel != 0:
#             return index
#         else:
#             index += 1
# 
# def rightzeroindex(_list):
#     '''
#     finds the right most position of valid pixels
#     returns None if all values in _list are 0
#     '''
#     index = len(_list) - 1
#     while index > 0:
#         if _list[index] != 0:
#             return index
#         else:
#             index -= 1
# 
# def maketilearray(tilesPerImage,tilesDown,tilesAcross):
#     '''
#     create a 2d array representing the tiles
#     returns a numpy array
#     '''
#     return numpy.arange(tilesPerImage).reshape(tilesDown, tilesAcross)
#         
