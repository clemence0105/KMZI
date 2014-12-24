#!/usr/bin/env python
#coding: UTF-8

import sys
from PIL import Image


def lsb(num, bit):
	if bit == 0:
		num &= 0xFE
	else:
		num |= 0x01
	return num
    

def Hiding(data, imageName, resImageName):
    data = [ord(x) for x in data]
    img = Image.open(imageName)
    raw = [ord(x) for x in img.tostring()]
    i = 0

    size = len(data)
    if size * 8 + 24 > len(raw):
		raise Exception('Слишком много данных для этого изображения!')
        
    for j in range(24):
        raw[i] = lsb(raw[i], size & 1)
        size >>= 1
        i += 1

    for b in data:
        for j in range(8):
            raw[i] = lsb(raw[i], b & 1)
            b >>= 1
            i += 1

    raw = [chr(x) for x in raw]
    resImg = Image.fromstring(img.mode, img.size, ''.join(raw))
    resImg.save(resImageName, "BMP")


def parseArguments():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('image')
    parser.add_argument('-i', '--input', nargs='?', type=argparse.FileType(mode='rb'), default=sys.stdin)
    parser.add_argument('-o', '--res_image', nargs='?')
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parseArguments()

    if not arguments.res_image:
        arguments.res_image = "_" + arguments.image + ".bmp"

    data = arguments.input.read()
    try:
        Hiding(data, arguments.image, arguments.res_image)
    except Exception as err:
        print "Ошибка: {}".format(err)
        sys.exit(1)
