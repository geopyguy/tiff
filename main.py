import os
import tiff_tools
from tiff_tools import Header, IFD


image = '/media/rich/OS/workspace/tiff/UTM2GTIF.TIF'
print os.path.exists(image)
f = open(image,'rb')
H = Header()
H.get(f)
print H.__dict__

f.close()