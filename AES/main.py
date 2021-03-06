#!/usr/bin/python
#coding: UTF-8

import sys

# константы, определяющие размер ключа и блока данных
Nk = 4  # число 32-х битных слов, составляющих шифроключ
Nb = 4  # число столбцов(32-х битных слов), составляющих State
Nr = 10  # число раундов, которое является функцией Nk и Nb


# получение раундовых ключей
def KeyExpansion(key):
    Rcon = [
        [0x00, 0x00, 0x00, 0x00],
        [0x01, 0x00, 0x00, 0x00],
        [0x02, 0x00, 0x00, 0x00],
        [0x04, 0x00, 0x00, 0x00],
        [0x08, 0x00, 0x00, 0x00],
        [0x10, 0x00, 0x00, 0x00],
        [0x20, 0x00, 0x00, 0x00],
        [0x40, 0x00, 0x00, 0x00],
        [0x80, 0x00, 0x00, 0x00],
        [0x1b, 0x00, 0x00, 0x00],
        [0x36, 0x00, 0x00, 0x00]]

    w = [0] * (Nb * (Nr + 1))

    for i in range(Nk):
        w[i] = [key[4 * i], key[4 * i + 1], key[4 * i + 2], key[4 * i + 3]]

    for i in range(Nk, Nb * (Nr + 1)):
        temp = w[i - 1]
        if i % Nk == 0:
            temp = SubWord(RotWord(temp))
            temp2 = []
            for j in range(4):
                temp2.append(temp[j] ^ Rcon[i / Nk][j])
            temp = temp2
        w[i] = []
        for j in range(4):
            w[i].append(temp[j] ^ w[i - Nk][j])
    return w


def Sub1Byte(byte):
    Sbox = [0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
            0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
            0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
            0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
            0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
            0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
            0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
            0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
            0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
            0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
            0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
            0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
            0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
            0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
            0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
            0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]
    return Sbox[byte]


def InvSub1Byte(byte):
    Sbox = [0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb,
           0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb,
           0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e,
           0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25,
           0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92,
           0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84,
           0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06,
           0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b,
           0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,
           0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e,
           0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
           0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4,
           0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f,
           0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef,
           0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61,
           0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d]
    return Sbox[byte]


# трансформации при шифровании, которые обрабатывают State, используя
# нелинейную таблицу замещения байтов(S-box), применяя её независимо к каждому байту State
def SubBytes(state):
    for i in range(4):
        for j in range(Nb):
            state[i][j] = Sub1Byte(state[i][j])
    return state

def InvSubBytes(state):
    for i in range(4):
        for j in range(Nb):
            state[i][j] = InvSub1Byte(state[i][j])
    return state


# функция, использующаяся в процедуре Key Expansion, 
# которая берет 4-х байтное слово и производит над ним циклическую перестановку
def RotWord(word):
    return word[1:] + word[:1]


# функция, используемая в процедуре Key Expansion, которая берет на входе
# четырёхбайтное слово и, применяя S-box к каждому из четырёх байтов, выдаёт выходное слово
def SubWord(word):
    return [Sub1Byte(x) for x in word]


# трансформация при шифровании и обратном шифровании, при которой Round Key XOR’ится c State
def AddRoundKey(state, roundKey):
    for i in range(4):
        for j in range(Nb):
            state[i][j] ^= roundKey[i][j]
    return state


# трансформации при шифровании, которые обрабатывают State, циклически смещая последние три строки State на разные величины
def ShiftRows(state):
    for i in range(4):
        state[i] = state[i][i:] + state[i][0:i]
    return state


def InvShiftRows(state):
    for i in range(4):
        state[i] = state[i][-i:] + state[i][:-i]
    return state


# умножение двух чисел в поле Галуа
def gmul(a, b):
    p = 0
    for counter in range(8):
        if b & 1:
            p ^= a
        hi_bit_set = a & 0x80
        a <<= 1
        a &= 0xff
        if hi_bit_set:
            a ^= 0x1b
        b >>= 1
    return p


# В процедуре MixColumns четыре байта каждой колонки State смешиваются, используя для этого обратимую линейную
# трансформацию. MixColumns обрабатывает состояния по колонкам, трактуя каждую из них как полином четвёртой степени.
def MixColumns(state):
    for i in range(Nb):
        b = [0] * 4
        b[0] = gmul(state[i][0], 2) ^ gmul(state[i][1], 3) ^ gmul(state[i][2], 1) ^ gmul(state[i][3], 1)
        b[1] = gmul(state[i][0], 1) ^ gmul(state[i][1], 2) ^ gmul(state[i][2], 3) ^ gmul(state[i][3], 1)
        b[2] = gmul(state[i][0], 1) ^ gmul(state[i][1], 1) ^ gmul(state[i][2], 2) ^ gmul(state[i][3], 3)
        b[3] = gmul(state[i][0], 3) ^ gmul(state[i][1], 1) ^ gmul(state[i][2], 1) ^ gmul(state[i][3], 2)
        for j in range(4):
            state[i][j] = b[j]
    return state


def InvMixColumns(state):
    for i in range(Nb):
        b = [0] * 4
        b[0] = gmul(state[i][0], 14) ^ gmul(state[i][1], 11) ^ gmul(state[i][2], 13) ^ gmul(state[i][3], 9)
        b[1] = gmul(state[i][0], 9)  ^ gmul(state[i][1], 14) ^ gmul(state[i][2], 11) ^ gmul(state[i][3], 13)
        b[2] = gmul(state[i][0], 13) ^ gmul(state[i][1], 9)  ^ gmul(state[i][2], 14) ^ gmul(state[i][3], 11)
        b[3] = gmul(state[i][0], 11) ^ gmul(state[i][1], 13) ^ gmul(state[i][2], 9)  ^ gmul(state[i][3], 14)
        for j in range(4):
            state[i][j] = b[j]
    return state



# функция шифрования блока данных
def encrypt(data, key):
    if len(key) != 16:
        raise Exception('Ключ должен быть 16-байтным!')
    w = KeyExpansion(key)
    
    state = []
    # сначала данные разбиваются на таблицу из 4-х строк и Nb столбцов
    # причем заполнение идёт по столбцам
    for i in range(4):
        state.append(data[i::Nb])

    state = AddRoundKey(state, w[0:Nb])
    for round in range(1, Nr):
        state = SubBytes(state)
        state = ShiftRows(state)
        state = MixColumns(state)
        state = AddRoundKey(state, w[round*Nb:Nb * (round + 1)])

    state = SubBytes(state)
    state = ShiftRows(state)
    state = AddRoundKey(state, w[Nr*Nb:(Nr + 1) * Nb])

    result = []
    for i in range(Nb):
        for j in range(4):
            result.append(state[j][i])
    return result


def decrypt(data, key):
    if len(key) != 16:
        raise Exception('Ключ должен быть 16-байтным!')
    w = KeyExpansion(key)
    
    state = []
    for i in range(4):
        state.append(data[i::Nb])

    state = AddRoundKey(state, w[Nr * Nb:(Nr + 1) * Nb])
    for round in range(Nr - 1, 0, -1):
        state = InvShiftRows(state)
        state = InvSubBytes(state)
        state = AddRoundKey(state, w[Nb * round:Nb * (round + 1)])
        state = InvMixColumns(state)

    state = InvShiftRows(state)
    state = InvSubBytes(state)
    state = AddRoundKey(state, w[0: Nb])

    result = []
    for i in range(Nb):
        for j in range(4):
            result.append(state[j][i])
    return result


def EncryptString(data, key):
    # переведём символы в int
    data = [ord(x) for x in data]
    key = [ord(x) for x in key]

    # выравнивание длины
    lastLen = len(data) % 16
    nZeroes = 16 - lastLen - 1
    data = [nZeroes] + data + [0] * nZeroes

    result = []
    for i in range(len(data) / 16):
        result += encrypt(data[i * 16: (i + 1) * 16], key)

    # переводим числа обратно в символы
    result = [chr(x) for x in result]
    return ''.join(result) # возвращаем в виде строки


def DecryptString(data, key):
    data = [ord(x) for x in data]
    key = [ord(x) for x in key]
    result = []
    for i in range(len(data) / 16):
        result += decrypt(data[i * 16: (i + 1) * 16], key)

    nZeroes = result[0]
    # избавимся от фиктивных нулей в конце
    if nZeroes != 0:
        result = result[1:-nZeroes]
    else:
        result = result[1:]
    result = [chr(x) for x in result]
    return ''.join(result)



def parseArguments():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', nargs='?', type=argparse.FileType(mode='rb'), default=sys.stdin)
    parser.add_argument('-o', '--output', nargs='?', type=argparse.FileType(mode='wb'), default=sys.stdout)
    parser.add_argument('-k', '--key', required=True, type=argparse.FileType(mode='rb'))
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
        if arguments.mode == 'c':
            coded = EncryptString(data, key)
        else:
            coded = DecryptString(data, key)
    except Exception as err:
        print "Ошибка: {}".format(err)
        sys.exit()
        
    arguments.output.write(coded)