import os
import struct
import tiff_tools
from tiff_tools import Header, IFD


image = '/media/rich/OS/workspace/tiff/UTM2GTIF.TIF'
image = '/media/rich/OS/workspace/tiff/cea.tif'
print os.path.exists(image)
f = open(image,'rb')
H = Header()
H.get(f)
print H.__dict__

foo = IFD(f)
foo.get()


print foo.__dict__

print 'here'
print foo.modelTiepoint
f.seek(foo.modelTiepoint[3])

print '@',f.tell()
print struct.unpack(H.symbol+'d',f.read(8))

f.close()