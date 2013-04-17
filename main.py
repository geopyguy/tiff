import os
import struct
import tiff_tools
from tiff_tools import IFD


#image = '/media/rich/OS/workspace/tiff/UTM2GTIF.TIF'
#image = '/media/rich/OS/workspace/tiff/cea.tif'

image = r'/home/rich/Documents/tiff/test2.tif'

print os.path.exists(image)
f = open(image,'rb')

foo = IFD(f)
foo.get()

for key in foo.__dict__.iterkeys():
    print key, foo.__dict__[key]


print foo.tilesAcross
print foo.tilesDown
print foo.tilesPerImage

tileOffsets = tiff_tools.gettileoffsets(f, foo.tileOffsets)
print len(tileOffsets), tileOffsets

tileArray = tiff_tools.maketilearray(foo.tilesPerImage,foo.tilesDown, foo.tilesAcross)
print tileArray



row = 0
col = 0
while row < foo.tilesDown:
    tile = tileArray[row][col]
    data = tiff_tools.gettile(f, foo.tileLength[3], foo.tileWidth[3], tileOffsets[tile])
    scanlineCounter = 0
    for scanline in data:
        rightEdgeIndex = 0
        leftEdgeIndex = 0
        x = 0; y = 0; x_ = 0; y_ = 0
        print 'tile', tile, 'row', row, 'col', col
        print scanline
        
        #Decide which side of the scanline to read from...
        #scanline is all 0's
        if len(set(scanline)) == 1:
            pass
        
        #scanline has leftmost 0's
        elif scanline[0] == 0:
            leftEdgeIndex = tiff_tools.leftzeroindex(scanline)
            
            if leftEdgeIndex > 0:
                x = (foo.tileWidth[3] * col) + leftEdgeIndex
                y = (foo.tileLength[3] * row) + scanlineCounter
                print leftEdgeIndex, 'x,y',(x,y)
            elif leftEdgeIndex == 0:
                pass
            elif leftEdgeIndex == None:
                row -= 1 #need to keep reading on the same row
                col += 1
                break
            else:
                pass
        
        #scanline has rightmost 0's
        elif scanline[len(scanline) - 1] == 0:
            rightEdgeIndex = tiff_tools.rightzeroindex(scanline)
            
            if rightEdgeIndex > 0:
                x = (foo.tileWidth[3] * col) + rightEdgeIndex
                y = (foo.tileLength[3] + row) + scanlineCounter
                print rightEdgeIndex, 'x,y',(x,y)
            elif rightEdgeIndex == 0:
                pass
            elif rightEdgeIndex == None:
                row -= 1 #need to keep reading on the same row
                col += 1
                break
            else:
                pass
            
        #scanline has no 0's
        elif scanline.count('0') == 0:
            pass
        
        else: #scanline has 0's in the middle
            leftEdgeIndex = tiff_tools.leftzeroindex(scanline)
            x = (foo.tileWidth[3] * col) + leftEdgeIndex
            y = (foo.tileLength[3] * row) + scanlineCounter
            
            rightEdgeIndex = tiff_tools.rightzeroindex(scanline)
            x_ = (foo.tileWidth[3] * col) + rightEdgeIndex
            y_ = (foo.tileLength[3] * row) + scanlineCounter
            
            print 'x,y',(x,y),'x_,y_',(x_,y_)
        scanlineCounter += 1
    row += 1

f.read()
f.tell()
#print foo.__dict__

#print 'here'
#print foo.modelTiepoint
#f.seek(foo.modelTiepoint[3])
#
#print '@',f.tell()
#print struct.unpack(H.symbol+'d',f.read(8))
#
#print 'geokey'
#f.seek(foo.geoKey[3])
#print '@',f.tell()
#
#print 'header = ', struct.unpack(H.symbol+'LL',f.read(8))
#for i in xrange(14):
#    print struct.unpack(H.symbol+'hhhh',f.read(8))

f.close()