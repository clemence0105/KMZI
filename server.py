#!/usr/bin/env python
#coding: UTF-8
import socket
import sys
from Vigenere.main import vigenere
from AES.main import DecryptString
from Stego.stego_out import Extracting


def recieve_data(keyVigenere, keyAES):
    sock = socket.socket()
    sock.bind(('', 7777))

    sock.listen(100)
    conn, addr = sock.accept()
    image_data = ""
    while True:
        new_data = conn.recv(1000000)
        if not new_data:
            break
        image_data += new_data
    conn.close()
    
    imgfile = open("_.bmp", 'wb')
    imgfile.write(image_data)
    imgfile.close()

    data = Extracting("_.bmp")
    data = DecryptString(data, keyAES)
    data = vigenere(data, keyVigenere, 'd')
    return data


def parseArguments():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('vigenere_key', type=argparse.FileType(mode='r'))
    parser.add_argument('aes_key', type=argparse.FileType(mode='r'))
    parser.add_argument('-o', '--output', nargs='?', type=argparse.FileType(mode='wb'), default=sys.stdout)
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parseArguments()
    try:
        keyVigenere = arguments.vigenere_key.read()
        keyAES = arguments.aes_key.read()
    except IOError:
        print "Не удаётся прочитать входные файлы"
        sys.exit()

    try:
        data = recieve_data(keyVigenere, keyAES)
    except Exception as err:
        print "Ошибка: {}".format(err)
        sys.exit()
    arguments.output.write(data)

    print "Сообщение принято"
