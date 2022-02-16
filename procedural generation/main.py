import noise
from PIL import Image

shape = (128, 128)

image_filepath = 'noise.png'
image = Image.new(mode='RGB', size=shape)

water = (66, 110, 225)
grass = (240, 210, 172)
beach = (36, 135, 32)
mountains = (140, 140, 140)
snow = (250, 250, 250)

scale = 25
octaves = 2
lacunarity = 3
persistence = 1.5
seed = 123

def set_color(x, y, image, value):
    if value < -0.07:
        image.putpixel((x, y), water)
    elif value < 0:
        image.putpixel((x, y), grass)
    elif value < 0.25:
        image.putpixel((x, y), beach)
    elif value < 0.50:
        image.putpixel((x, y), mountains)
    elif value < 1:
        image.putpixel((x, y), snow)

for x in range(shape[0]):
    for y in range(shape[1]):
        value = noise.pnoise2(  x / scale,
                                y / scale,
                                octaves=octaves,
                                lacunarity=lacunarity,
                                persistence=persistence,
                                repeatx=shape[0],
                                repeaty=shape[1],
                                base=0
                                )
        set_color(x, y, image, value)

image.save(image_filepath)
# image.show()