from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
import os



config = {}

big = 12
small = 8

def init_font(size=12):
    if size not in config:
        config[size] = {}

    if 'font' not in config[size]:

        config[size]['font'] = ImageFont.truetype(os.path.dirname(os.path.realpath(__file__)) + "/Helvetica Bold.ttf", size)

    return config[size]['font']


def read_left_image(size):
    if size not in config:
        config[size] = {}
    if 'left' not in config[size]:
        config[size]["left"] = Image.open(os.path.dirname(os.path.realpath(__file__)) + "/imgs/left_%s.png" % size)

    return config[size]["left"]

def read_right_image(size):
    if size not in config:
        config[size] = {}
    if 'right ' not in config[size]:
        config[size]["right"] = Image.open(os.path.dirname(os.path.realpath(__file__)) + "/imgs/right_%s.png" % size)

    return config[size]["right"]


def draw_stars(stars, size=big, save=False):
    stars_text = to_text(stars)

    image_left = read_left_image(size)
    image_right = read_right_image(size)
    font = init_font(size)

    text_size = font.getsize(stars_text)

    size = (image_left.size[0] + text_size[0] + image_right.size[0], image_left.size[1])

    text_pos = (image_left.size[0], 7)
    text_rec = (image_left.size[0], 0, image_left.size[0] + text_size[0], size[1])
    line_top_rec = (image_left.size[0], 0, text_rec[2], 0)
    line_bot_rec = (image_left.size[0], size[1] - 1, text_rec[2], size[1])
    left_rec = (0,0,image_left.size[0], size[1])
    right_rec = (text_rec[2], 0, size[0], size[1])



    img = Image.new("RGBA", size, None)
    
    draw = ImageDraw.Draw(img)

    draw.rectangle(text_rec, fill=(255,255,255))
    
    draw.rectangle(line_top_rec, fill=(213,213,213))
    draw.rectangle(line_bot_rec, fill=(213,213,213))
    draw.text(text_pos, stars_text, (54,54,54), font=font)

    img.paste(image_left, left_rec)
    img.paste(image_right, right_rec)
    
    if save:
        img.save("out.png")

    imgout = BytesIO()
    img.save(imgout, "PNG")
    imgout.seek(0)

    return imgout




def to_text(stars):
    stars = str(stars)
    result = []
    while stars:
        result.append(stars[-3:])
        stars = stars[:-3]
    
    result.reverse()
    return ','.join(result)



if __name__ == '__main__':
    draw_stars(1234567890)