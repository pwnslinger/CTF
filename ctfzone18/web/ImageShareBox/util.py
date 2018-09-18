#!/usr/bin/env python
from __future__ import print_function
from PIL.ExifTags import TAGS
from PIL import Image
import piexif
import dropbox

auth_token = 'your_token_here'
path = '/Apps/ImgShareBox/test.jpg'

def upload():
    dpx = dropbox.Dropbox(auth_token)
    try:
        with open('doh_des.jpg', 'rb') as f:
            dpx.files_upload(f.read(), path, mode=dropbox.files.WriteMode("overwrite"))
    except Exception as e:
        print(str(e))


def get_desc(img):
    return '%s = %s' % (TAGS[0x10e], str(img._getexif()[0x10e]))

def set_desc(img, text):
    try:
        exif_dict = piexif.load(img.info['exif'])
        exif_dict['0th'][270] = text
        exif_bytes = piexif.dump(exif_dict)
        img.save(img.filename, 'jpeg', exif=exif_bytes)
    except Exception as e:
        print('[-] Error: %s\n' % str(e))

def reload(img):
    try:
        filename = img.filename
        img.close()
    except Exception:
        pass
    return Image.open(filename)

def load(filename):
    return Image.open(filename)
