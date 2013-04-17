import os
import struct
import tiff_tools
from tiff_tools import IFD


#image = '/media/rich/OS/workspace/tiff/UTM2GTIF.TIF'
#image = '/media/rich/OS/workspace/tiff/cea.tif'
image = r'C:\workspace\tiff\test.tif'
print os.path.exists(image)
f = open(image,'rb')

foo = IFD(f)
foo.get()





for key in foo.__dict__.iterkeys():
    print key, foo.__dict__[key]


print foo.tilesAcross
print foo.tilesDown
print foo.tilesPerImage


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