with open("input.txt") as f:
    data = f.read().rstrip()

image_width  = 25
image_height = 6

layer_length = image_width * image_height
if len(data) % (image_width * image_height) != 0:
    raise ValueError('invalid image data')

layers = (data[i:i+layer_length] for i in range(0, len(data), layer_length))

layer_with_least_0s = min(layers, key=lambda layer: sum(1 for x in layer if x == '0'))

len_1 = sum(1 for x in layer_with_least_0s if x == '1')
len_2 = sum(1 for x in layer_with_least_0s if x == '2')
print(len_1 * len_2)
