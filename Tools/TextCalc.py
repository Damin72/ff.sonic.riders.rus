import re
from binascii import unhexlify
import os

LEN_OF_HEXES_IN_FILE = 8

first_file = r"[Insert path to file with original text]\Orig.bin"

def work_with_textfile(file):
    len_of_file = os.stat(file).st_size

    text = bytes()

    with open(file, mode='rb') as wtf:
        for i in wtf:
            text += i

    text = text[16:]
    offsets = bytes()
    while text[3:4] == b'\x00':
        offsets += text[0:4]
        text = text[4:]

    list_of_hexes = list(map(hex, [m.start()+2+16+len(offsets) for m in re.finditer(b'\x00\x80', text)]))[:-1]

    for i in range(len(list_of_hexes)):
        list_of_hexes[i] = '0'*(LEN_OF_HEXES_IN_FILE-len(list_of_hexes[i])+2) + list_of_hexes[i][2:]

    print(list_of_hexes)

    list_of_hexes = list(map(unhexlify, list_of_hexes))

    for i in range(len(list_of_hexes)):
        list_of_hexes[i] = list_of_hexes[i][::-1]

    temp = r"[Insert path to output file]\complete.bin"

    with open(first_file, mode='rb') as first:
        with open(temp, mode='wb') as temp:
            first_string = first.read(16)
            writing_bytes = b''.join(list_of_hexes)
            pointer_position_change = len(list_of_hexes)*4
            first.seek(pointer_position_change, 1)
            other = first.read(len_of_file-pointer_position_change-16)
            temp.write(first_string+writing_bytes+other)
            print(len_of_file)


work_with_textfile(first_file)
