# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 19:54:59 2015

@author: List
"""
import pygame
import os
from PIL import Image
import subprocess

# load images properly
def load_image(name, colorkey=None):
    fullname = os.path.join('images', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

# convert image to desired image format    
def convert_image_to(image_file, im_format):
    if image_file[-4:] == "."+im_format:
        file_out = image_file
    else:
        print "converting", image_file, "..."
        img = Image.open(image_file)
        file_out = str(image_file[0:-4])+"."+im_format
        if len(img.split()) == 4:
            # prevent IOError: cannot write mode RGBA as BMP
            r, g, b, a = img.split()
            img = Image.merge("RGB", (r, g, b))
        img.save(file_out)
        os.remove(image_file)
    return file_out

def reverse_mp3(mp3_file):
    print mp3_file
    reverse = subprocess.Popen('sox -v 0.98 '+mp3_file+' '+mp3_file[:-3]+'wav reverse', shell=True)
    subprocess.Popen.wait(reverse)
    os.remove(mp3_file)
    
def mp3_to_wav(mp3_file):
    if mp3_file[-3:] == "wav":
        pass
    else:
        print mp3_file
        conversion = subprocess.Popen('sox -v 0.98 '+mp3_file+' '+mp3_file[:-3]+'wav', shell=True)
        subprocess.Popen.wait(conversion)
        os.remove(mp3_file)