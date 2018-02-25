#!/usr/bin/env python3
import argparse
import re
import os
import sys
import shutil
import tempfile
import json
import logging
from PIL import Image

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
from BmpSteg.Getter import get_from_image
from BmpSteg.Hasher import get_hash, make_dic
from BmpSteg.checker import check_exempt_files, check_free_space
from BmpSteg.Injector import hide_in_image
from io import StringIO


def check_bits(rgb_tuple):
    for color in rgb_tuple:
        if not (0 <= int(color) <= 8):
            msg = "%r is not in [0, 8]" % color
            raise argparse.ArgumentTypeError(msg)
    return rgb_tuple


def make_file_copy(input_file, output_file):
    with open(input_file, 'rb') as imgfile:
        information = imgfile.read()
        with open (output_file, 'wb') as img2:
            img2.write(information)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', help='file for injection', metavar='input_file',
                        action='store', type=str)
    parser.add_argument('-b', type=check_bits, metavar='rgb', action='store',
                        help='Amount of bits to store in each color byte',
                        default=(1, 1, 1))
    parser.add_argument('-fi', '--files', nargs='+', default=[])
    parser.add_argument('-force', action='store_true', help='Check integrity',
                        default=False)
    parser.add_argument('-o', metavar='ouput_file',
                        action='store', type=str,
                        help='given_output_file')
    parser.add_argument('-f',  metavar='file',
                        action='store', type=str,
                        help='regular expression of files')
    parser.add_argument('-l', metavar='file_with_secret_files',
                        help='listing on', action='store', type=str)
    parser.add_argument('-e', help='extracting mode', action='store_true')
    args = parser.parse_args()
    hashes = []
    logging.basicConfig(level=logging.DEBUG)
    if args.l or args.e:
        if args.i:
            output_file = args.i
        else:
            output_file = args.l
        temp = get_from_image(output_file, 'tuple.txt', (1, 1, 1), -1, None,
                              unnnecessary=1)
        tuple_string = str(temp.read())
        rgb_tuple = (int(tuple_string[2]), int(tuple_string[3]),
                     int(tuple_string[4]))
        temp.close()
        temp = get_from_image(output_file, 'dictionary.pickle', rgb_tuple, 0,
                              None, unnnecessary=1)
        dictionary_of_files = json.loads(temp.read().decode("utf-8"))
        temp.close()
    if args.l:
        for e in dictionary_of_files:
            print(e)
    elif args.e:
        list_of_needed_files = []
        wildcart = '.' + args.f
        logging.debug(str(dictionary_of_files))
        for e in dictionary_of_files.keys():
            if re.fullmatch(wildcart, e):
                list_of_needed_files.append(e)
        print(list_of_needed_files)
        try:
            os.mkdir(args.o)
        except OSError:
            pass
        for file in list_of_needed_files:
            new_file = file
            get_from_image(output_file, new_file, rgb_tuple,
                           dictionary_of_files[file][2], args.o)
            mes = 'getting hash from' + str(new_file)
            logging.debug(mes)
            hashes.append(get_hash(new_file, args.o))
        if args.force:
            check_exempt_files(dictionary_of_files, hashes)
    else:
        rgb_tuple = args.b
        rgb_tuple = int(rgb_tuple[0]), int(rgb_tuple[1]), int(rgb_tuple[2])
        image = Image.open(args.i)
        height = image.size[1]
        width = image.size[0]
        needed_space = 1000*8
        k = needed_space//(height*(rgb_tuple[0] + rgb_tuple[1] + rgb_tuple[2]))
        k += 2
        amount_of_bits_pixel = (rgb_tuple[0] + rgb_tuple[1] + rgb_tuple[2])
        max_text_size = height * width * amount_of_bits_pixel
        check_free_space(max_text_size, args.files)
        if args.i:
            input_file = args.i
        else:
            complete_stdin = sys.stdin.read()
            input_file = StringIO(complete_stdin)
        if args.o:
            output_file = args.o
        else:
            output_file = 'None'
        make_file_copy(input_file, output_file)
        temp = tempfile.TemporaryFile(mode='w+b')
        temp.write(bytes(str(rgb_tuple[0]) + str(rgb_tuple[1]) +
                         str(rgb_tuple[2]), 'UTF-8'))
        temp.seek(0)
        hide_in_image(output_file, temp, output_file, (1, 1, 1), -1, 1)
        dictionary_of_files = make_dic(output_file, args.files,
                                       output_file, rgb_tuple, k)

        if not args.o:
            with open(output_file, "r") as f:
                shutil.copyfileobj(f, sys.stdout)
        logging.debug(str(dictionary_of_files))
        a = json.dumps(dictionary_of_files)
        temp = tempfile.TemporaryFile(mode='w+b')
        temp.write(bytes(a, 'UTF-8'))
        temp.seek(0)
        hide_in_image(output_file, temp, output_file, rgb_tuple, 0, 1)


if __name__ == '__main__':
    main()
