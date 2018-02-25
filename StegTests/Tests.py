#!/usr/bin/env python3
import sys
import os
import argparse
import unittest

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
from BmpSteg.Hasher import make_dic, get_hash
from BmpSteg.Injector import hide_in_image
from BmpSteg.Getter import get_from_image
from BMP import check_bits, make_file_copy
from BmpSteg.checker import check_exempt_files, check_free_space


class MyTestCase(unittest.TestCase):

    os.chdir('tests')

    def test_hide_in_image(self):
        secret_file = 'file1.txt'
        output_file = '1.bmp'
        rgb_tuple = (1, 1, 1)
        column = hide_in_image(output_file, secret_file, output_file,
                               rgb_tuple, -1)
        self.assertEqual(0, column)

    def test_hide_in_image1(self):
        secret_file = 'file1.txt'
        secret_file2 = 'file2.txt'
        output_file = 'DogTest2.bmp'
        rgb_tuple = (1, 1, 1)
        column = hide_in_image(output_file, secret_file, output_file,
                               rgb_tuple, -1)
        column = hide_in_image(output_file, secret_file2, output_file,
                               rgb_tuple, column)
        self.assertEqual(1, column)

    def test_get_image(self):
        secret_file = 'file1.txt'
        secret_file2 = 'file2.txt'
        output_file = 'DogTest2.bmp'
        file2 = 'new_text.txt'
        rgb_tuple = (1, 1, 1)
        column = hide_in_image(output_file, secret_file, output_file,
                               rgb_tuple, -1)
        hide_in_image(output_file, secret_file2, output_file, rgb_tuple,
                      column)
        column = -1
        get_from_image(output_file, file2, rgb_tuple, column, None)
        with open('new_text.txt', 'rb') as f1:
            data1 = f1.read()
        with open('file1.txt', 'rb') as f2:
            data2 = f2.read()
        self.assertEqual(data1, data2)

    def test_get_image2(self):
        output_file = 'DogTest2.bmp'
        secret_file = 'file1.txt'
        secret_file2 = 'file2.txt'
        file2 = 'new_text.txt'
        rgb_tuple = (1, 1, 1)
        column = hide_in_image(output_file, secret_file, output_file,
                               rgb_tuple, -1)
        hide_in_image(output_file, secret_file2, output_file, rgb_tuple,
                      column)
        column = 0
        get_from_image(output_file, file2, rgb_tuple, column, None)
        with open('new_text.txt', 'rb') as f1:
            data1 = f1.read()
        with open('file2.txt', 'rb') as f2:
            data2 = f2.read()
        self.assertEqual(data1, data2)

    def test_check_bits(self):
        tuple1 = (1, 2, 6)
        self.assertEqual(check_bits(tuple1), tuple1)

    def test_check_bits2(self):
        tuple1 = (1, 2, 9)
        exception = False
        try:
            check_bits(tuple1)
        except argparse.ArgumentTypeError:
            exception = True
        self.assertTrue(exception)

    def test_make_file_copy(self):
        input_file = 'DogTest.bmp'
        output_file = 'DogTest3.bmp'
        make_file_copy(input_file, output_file)
        with open(input_file, 'rb') as f1:
            a = f1.read()
        with open(output_file, 'rb') as f2:
            b = f2.read()
        self.assertEqual(a, b)

    def test_get_hash(self):
        file1 = 'file5.txt'
        file2 = 'file6.txt'
        hash1 = get_hash(file1, None)
        hash2 = get_hash(file2, None)
        self.assertEqual(hash1, hash2)

    def test_get_hash2(self):
        file1 = 'DogTest.bmp'
        file2 = 'file2.txt'
        hash1 = get_hash(file1, None)
        hash2 = get_hash(file2, None)
        self.assertNotEqual(hash1, hash2)

    def test_check_free_space(self):
        exception = False
        files = []
        maxtext = 2
        try:
            check_free_space(maxtext, files)
        except Exception:
            exception = True
        self.assertTrue(exception)

    def test_check_free_space(self):
        exception = False
        files = ['DogTest.bmp']
        maxtext = 20
        try:
            check_free_space(maxtext, files)
        except Exception:
            exception = True
        self.assertTrue(exception)

    def test_check_excempt_files(self):
        list_of_files = ['file1.txt', 'file5.txt', 'file4.txt']
        output_file = 'DogTest2.bmp'
        rgb_tuple = (1, 1, 1)
        hashes = []
        dict2 = make_dic(output_file, list_of_files, output_file, rgb_tuple,
                         -1)
        for file in list_of_files:
            new_file = 'new' + file
            get_from_image(output_file, new_file, rgb_tuple,
                           dict2[file][2], None)
            hashes.append(get_hash(new_file, None))
        self.assertTrue(check_exempt_files(dict2, hashes))

    def test_check_excempt_files2(self):
        list_of_files = ['file1.txt', 'file5.txt', 'file4.txt']
        output_file = 'DogTest2.bmp'
        rgb_tuple = (1, 1, 1)
        hashes = []
        dict2 = make_dic(output_file, list_of_files, output_file, rgb_tuple,
                         -1)
        dict2['file1.txt'] = 234, 3, 3
        for file in list_of_files:
            new_file = 'new' + file
            get_from_image(output_file, new_file, rgb_tuple,
                           dict2[file][2], None)
            hashes.append(get_hash(new_file, None))
        self.assertFalse(check_exempt_files(dict2, hashes))

    def test_make_dictionary(self):
        list_of_files = ['file1.txt', 'file5.txt', 'file4.txt']
        output_file = 'DogTest2.bmp'
        rgb_tuple = (1, 1, 1)
        dict1 = {'file1.txt': (0, get_hash('file1.txt', None), -1),
                 'file5.txt': (1, get_hash('file5.txt', None), 0),
                 'file4.txt': (2, get_hash('file4.txt', None), 1)}
        dict2 = make_dic(output_file, list_of_files, output_file, rgb_tuple,
                         -1)
        self.assertEqual(dict1, dict2)

if __name__ == '__main__':
    unittest.main()
