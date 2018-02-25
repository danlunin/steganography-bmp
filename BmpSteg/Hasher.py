import hashlib
import os
from BmpSteg.Injector import hide_in_image


def make_dic(input_file, list_of_files, output_file, rgb_tuple, k):
    dic = {}
    for file in list_of_files:
        dic[file] = hide_in_image(input_file, file, output_file, rgb_tuple,
                                  k), get_hash(file, None), k
        k = dic[file][0]
    return dic


def get_hash(filename, directory):
    if directory is not None:
        current = os.getcwd()
        os.chdir(directory)
    BLOCKSIZE = 65536
    hasher = hashlib.sha1()
    with open(filename, 'rb') as afile:
        buf = afile.read(BLOCKSIZE)
        while buf:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)
    if directory is not None:
        os.chdir(current)
    return hasher.hexdigest()
