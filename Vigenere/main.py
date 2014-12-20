#!/usr/bin/env python
#coding: UTF-8

import sys

def vigenere(data, key, mode):
    data = data.upper().rstrip("\n")
    key = key.upper().rstrip("\n")
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "
    alphLen = len(alphabet)
    keyLen = len(key)
    res = ""
    if keyLen == 0:
        raise Exception("Ключ нулевой длинны!")
        
    for i, s in enumerate(data):
        k = key[i % keyLen]
        try:
            sIndex = alphabet.index(s)
        except ValueError:
            raise Exception ("Символа '{}' нет в словаре!".format(s))
        try:
            kIndex = alphabet.index(k)
        except ValueError:
            raise Exception ("Символа '{}' нет в словаре!".format(k))

        if mode == 'c': # шифрование
            r = sIndex + kIndex
        else: # дешифрование
            r = sIndex - kIndex

        res += alphabet[(r + alphLen) % alphLen]

    return res
        


def parseArguments():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', nargs='?', type=argparse.FileType(mode='r'), default=sys.stdin)
    parser.add_argument('-o', '--output', nargs='?', type=argparse.FileType(mode='w'), default=sys.stdout)
    parser.add_argument('-k', '--key', required=True, type=argparse.FileType(mode='r'))
    parser.add_argument('mode', choices=['c', 'd'], help="c - шифрование, d - дешифрование")
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parseArguments()
    try:
        data = arguments.input.read()
        key = arguments.key.read()
    except IOError:
        print "Не удаётся прочитать входные файлы"
        sys.exit()

    try:
        coded = vigenere(data, key, arguments.mode)
    except Exception as err:
        print "Ошибка: {}".format(err)
        sys.exit()
        
    arguments.output.write(coded)