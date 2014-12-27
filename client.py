#!/usr/bin/env python
#coding: UTF-8
import socket
import sys
from Vigenere.main import vigenere
from AES.main import EncryptString
from Stego.stego_in import Hiding


def send_data(data, keyVigenere, keyAES, imageName, server):
    res_image = "_" + imageName + ".bmp"
    data = vigenere(data, keyVigenere, 'c')
    data = EncryptString(data, keyAES)
    Hiding(data, imageName, res_image)
    data = open(res_image, 'rb').read()

    sock = socket.socket()
    sock.connect((server, 7777))
    sock.send(data)
    sock.close()


def parseArguments():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('vigenere_key', type=argparse.FileType(mode='r'))
    parser.add_argument('aes_key', type=argparse.FileType(mode='r'))
    parser.add_argument('image')
    parser.add_argument('server_address')
    parser.add_argument('-i', '--input', nargs='?', type=argparse.FileType(mode='r'), default=sys.stdin)
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parseArguments()
    try:
        data = arguments.input.read()
        keyVigenere = arguments.vigenere_key.read()
        keyAES = arguments.aes_key.read()
    except IOError:
        print "Не удаётся прочитать входные файлы"
        sys.exit()

    try:
        send_data(data, keyVigenere, keyAES, arguments.image, arguments.server_address)
    except Exception as err:
        print "Ошибка: {}".format(err)
        sys.exit()

    print "Сообщение успешно отправлено"