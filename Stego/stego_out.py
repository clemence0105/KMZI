#!/usr/bin/env python
#coding: UTF-8

import sys
from PIL import Image

def Extracting(imageName):
    img = Image.open(imageName)
    raw = [ord(x) for x in img.tostring()]
    i = 0

    size = 0
    while i < 24:
        size |= (raw[i] & 1) << i
        i += 1

    res = ""
    for j in range(size):
        b = 0
        for k in range(8):
            b |= (raw[i] & 1) << k
            i += 1
        res += chr(b)

    return res

def parseArguments():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('image')
    parser.add_argument('-o', '--output', nargs='?', type=argparse.FileType(mode='wb'), default=sys.stdout)
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parseArguments()

    try:
        extracted = Extracting(arguments.image)
        arguments.output.write(extracted)
    except Exception as err:
        print "Ошибка: {}".format(err)
        sys.exit()
