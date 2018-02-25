import os
import logging


def check_exempt_files(dictionary, hashes):
    a = True
    for file in dictionary:
        if dictionary[file][1] in hashes:
            mes = 'OK ' + str(file)
            logging.debug(mes)
            mes = 'Your hash: ' + str(dictionary[file][1])
            logging.debug(mes)
        else:
            mes = 'No {0} with hash {1} in: {2}'.format(file,
                                                        dictionary[file][1],
                                                        hashes)
            logging.debug(mes)
            a = False
    return a


def check_free_space(max_text_size, files):
    size = 0
    for e in files:
        size += os.path.getsize(e)
    if size <= 0:
        raise Exception('Your file is empty')
    elif size > max_text_size:
        raise Exception('Your files are too big')
