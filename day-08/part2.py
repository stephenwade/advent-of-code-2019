with open("input.txt") as f:
    data = f.read().rstrip()

image_width  = 25
image_height = 6

layer_length = image_width * image_height
if len(data) % layer_length != 0:
    raise ValueError('invalid image data')

layers = (data[i:i+layer_length] for i in range(0, len(data), layer_length))

pixels = zip(*layers)

def finalize_pixel(pixel):
    for layer in pixel:
        if layer != '2':
            return layer
    raise ValueError('invalid pixel data')

final_pixels = list(map(finalize_pixel, pixels))
final_image = (final_pixels[i:i+image_width] for i in range(0, len(final_pixels), image_width))

def display_pixel(pixel):
    if pixel == '0':
        return '  '
    if pixel == '1':
        return '##'
    raise ValueError('invalid pixel')

for row in final_image:
    print(''.join(map(display_pixel, row)))
