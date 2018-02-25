from PIL import Image, ImageDraw

DETECT_BIT = {0: (0b11111111, 0b00000000),
              1: (0b11111110, 0b00000001),
              2: (0b11111101, 0b00000010),
              3: (0b11111011, 0b00000100),
              4: (0b11110111, 0b00001000),
              5: (0b11101111, 0b00010000),
              6: (0b11011111, 0b00100000),
              7: (0b10111111, 0b01000000)}


def get_data(file_for_injection, tempfile=None):
    if tempfile is None:
        with open(file_for_injection, 'rb') as ft:
            tbyte = ft.read()
            file_for_injection_len = len(tbyte) - 1
            tbyte =\
                file_for_injection_len.to_bytes(3, byteorder='little') + tbyte
    else:
        tbyte = file_for_injection.read()
        file_for_injection_len = len(tbyte) - 1
        tbyte =\
            file_for_injection_len.to_bytes(3, byteorder='little') + tbyte
    return iter(tbyte)


def hide_in_image(input_file, file_for_injection, output_file, rgb_tuple,
                  column, tempfile=None):
    mode = 0
    with open(output_file, 'rb') as imgfile:
        image = Image.open(imgfile)
        draw = ImageDraw.Draw(image)
        width = image.size[0]
        height = image.size[1]
        pix = image.load()
        byteText = get_data(file_for_injection, tempfile)
    amount_of_bits = 0
    byte = next(byteText)
    for i in range(column + 1, width):
        for j in range(height):
            pixels = [pix[i, j][0], pix[i, j][1], pix[i, j][2]]
            for k in range(3):
                for l in range(rgb_tuple[k]):
                    if amount_of_bits < 8:
                        amount_of_bits += 1
                    else:
                        try:
                            byte = next(byteText)
                            amount_of_bits = 1
                        except StopIteration:
                            draw.point((i, j), (pixels[0], pixels[1],
                                                pixels[2]))
                            image.save(output_file, "BMP")
                            return i
                    lsb = byte & 0b00000001
                    if lsb == 0:
                        pixels[k] = pixels[k] & DETECT_BIT[rgb_tuple[k] - l][0]
                    else:
                        pixels[k] = pixels[k] | DETECT_BIT[rgb_tuple[k] - l][1]
                    byte = byte >> 1
                draw.point((i, j), (pixels[0], pixels[1], pixels[2]))
    image.save(output_file, "BMP")
    return i
