# steganography-bmp
Utility for steganography in BMP format.
#Examples:
# Injection 
Inject files Che.bmp, text.txt, new_text.txt into file Dog.bmp by r:g:b=3:1:1 and result(image with secret information) in output.bmp
$ python3 BMP.py -i Dog.bmp -o output_bmp.bmp -b 311 --files Che.bmp text.txt new_text.txt

# Listing (to get names of all files injected in the image)
$ python3 BMP.py -l output.bmp
file1.txt
file2.doc
file3.bmp

# Unpacking data
Unpacking from output.bmp by mask '*.txt' and resultedfiles into directory "data" data
$ python3 BMP.py -e -i output.bmp -f *.txt -force -o folder
