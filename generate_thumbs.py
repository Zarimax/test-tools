import os, sys
from PIL import Image

basewidth = 130

for infile in filter(os.path.isfile, os.listdir( os.curdir ) ):
    outfile = os.path.splitext(infile)[0] + "_t.jpg"
    print infile+" --> "+outfile
    if infile != outfile:
        try:
            img = Image.open(infile)
            wpercent = (basewidth/float(img.size[0]))
            hsize = int((float(img.size[1])*float(wpercent)))
            img = img.resize((basewidth,hsize), Image.ANTIALIAS)
            img.save(outfile, "JPEG")
        except IOError:
            print "cannot create thumbnail for '%s'" % infile
