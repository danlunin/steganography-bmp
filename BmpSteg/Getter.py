from PIL import Image
from BmpSteg.Injector import DETECT_BIT
import os
import tempfile


DICTIONARY_GET_RAMAINING = {0: (0b11111111, 0b00000000),
                            1: (0b11111110, 0b00000001),
                            2: (0b11111100, 0b00000011),
                            3: (0b11111000, 0b00000111),
                            4: (0b11110000, 0b00001111),
                            5: (0b11100000, 0b00011111),
                            6: (0b11000000, 0b00111111),
                            7: (0b10000000, 0b01111111)}


def get_information(width, height, pix, size, rgb_tuple, column):
    list_of_bytes = []
    length = 0
    bits = []
    for i in range(column + 1, width):
        for j in range(height):
            for k in range(3):
                pix_num = pix[i, j][k]
                if length > size + 3:
                    return list_of_bytes
                lsb = pix_num & DICTIONARY_GET_RAMAINING[rgb_tuple[k]][1]
                for l in range(rgb_tuple[k]):
                    if len(bits) == 8:
                        length += 1
                        bits.reverse()
                        list_of_bytes.append(bytes([int(''.join(bits), 2)]))
                        bits = []
                    if lsb & DETECT_BIT[rgb_tuple[k] - l][1] == 0:
                        bits.append('0')
                    else:
                        bits.append('1')


def get_from_image(output_file, new_file, rgb_tuple, column, folder,
                   unnnecessary=None):
    current = os.getcwd()
    new = None
    with open(output_file, 'rb') as imgfile:
        image = Image.open(imgfile)
        width = image.size[0]
        height = image.size[1]
        pix = image.load()
        size_array = get_information(width, height, pix, 3, rgb_tuple, column)
        size = (int.from_bytes((size_array[0] + size_array[1]),
                               byteorder='little'))
        if folder is not None:
            os.chdir(folder)
            new = 1
        information_array = get_information(width, height, pix, size,
                                            rgb_tuple, column)[3:]
        if unnnecessary is None:
            with open(new_file, 'wb') as fi2:
                for i in range(len(information_array)):
                    fi2.write(information_array[i])
            imgfile.close()
        else:
            temp = tempfile.TemporaryFile(mode='w+b')
            for i in range(len(information_array)):
                temp.write(information_array[i])
            temp.seek(0)
            return temp
        if new:
            os.chdir(current)
