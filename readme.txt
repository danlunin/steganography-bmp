# �������� Che.bmp, text.txt, new_text.txt � ���� Dog.bmp �� r:g:b=3:1:1 � ����� ���������� � output.bmp
$ python3 BMP.py -i Dog.bmp -o output_bmp.bmp -b 311 --files Che.bmp text.txt new_text.txt

# �������
$ python3 BMP.py -l output.bmp
file1.txt
file2.doc
file3.bmp

# ���������� ������ �� output.bmp �� ����� '*.txt' � ����� ������ � ������� data
$ python3 BMP.py -e -i output.bmp -f *.txt -force -o folder