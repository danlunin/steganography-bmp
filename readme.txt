# вшивание Che.bmp, text.txt, new_text.txt в файл Dog.bmp по r:g:b=3:1:1 и вывод результата в output.bmp
$ python3 BMP.py -i Dog.bmp -o output_bmp.bmp -b 311 --files Che.bmp text.txt new_text.txt

# листинг
$ python3 BMP.py -l output.bmp
file1.txt
file2.doc
file3.bmp

# распаковка данных из output.bmp по маске '*.txt' и вывод файлов в каталог data
$ python3 BMP.py -e -i output.bmp -f *.txt -force -o folder