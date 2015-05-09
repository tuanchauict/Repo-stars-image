from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
import os


font_size = {
    'big': 12,
    'small': 10
}

text_margin = {
    'big': 7,
    'small': 6
}

img_margin = {
    'big': 20,
    'small': 10
}

config = {}


def init_font(size='small'):
    if 'font' not in config:
        config['font'] = {}

    if size not in config['font']:
        config['font'][size] = ImageFont.truetype(os.path.dirname(os.path.realpath(__file__)) + "/Helvetica Bold.ttf", font_size[size])

    return config['font'][size]


def read_image(_type, direction, size):
    if _type not in config:
        config[_type] = {}
    if direction not in config[_type]:
        config[_type][direction] = {}
    if size not in config[_type][direction]:
        config[_type][direction][size] = Image.open(os.path.dirname(os.path.realpath(__file__)) + "/imgs/%s_%s_%s.png" % (_type, direction, size))

    return config[_type][direction][size]


def draw_single_img(number, image_left, image_right, font, _size='small'):
    number = to_text(number)

    text_size = font.getsize(number)
    size = (image_left.size[0] + text_size[0] + image_right.size[0], image_left.size[1])

    text_pos = (image_left.size[0], text_margin[_size])
    text_rec = (image_left.size[0], 0, image_left.size[0] + text_size[0], size[1])
    line_top_rec = (image_left.size[0], 0, text_rec[2], 0)
    line_bot_rec = (image_left.size[0], size[1] - 1, text_rec[2], size[1])
    left_rec = (0,0,image_left.size[0], size[1])
    right_rec = (text_rec[2], 0, size[0], size[1])


    img = Image.new("RGBA", size, None)
    
    img.paste(image_left, left_rec)
    img.paste(image_right, right_rec)

    draw = ImageDraw.Draw(img)

    draw.rectangle(text_rec, fill=(250,250,250))
    
    draw.rectangle(line_top_rec, fill=(213,213,213))
    draw.rectangle(line_bot_rec, fill=(213,213,213))
    draw.text(text_pos, number, (54,54,54), font=font)

    return img


def draw_stars(stars, size='small', save=False):
    image_left = read_image('star', 'left', size)
    image_right = read_image('star', 'right', size)
    font = init_font(size)

    img = draw_single_img(stars, image_left, image_right, font, size)
    
    if save:
        img.save("stars.png")

    return img


def draw_folks(folks, size='small', save=False):
    image_left = read_image('folk', 'left', size)
    image_right = read_image('folk', 'right', size)
    font = init_font(size)

    img = draw_single_img(folks, image_left, image_right, font, size)
    
    if save:
        img.save("folks.png")

    return img


def draw_watches(watches, size='small', save=False):
    image_left = read_image('watch', 'left', size)
    image_right = read_image('watch', 'right', size)
    font = init_font(size)

    img = draw_single_img(watches, image_left, image_right, font, size)
    
    if save:
        img.save("watches.png")

    return img


def draw_image(watches=None, stars=None, folks=None, _size='small', save=False):
    imgs = []
    if watches != None:
        imgs.append(draw_watches(watches, _size, save))

    if stars != None:
        imgs.append(draw_stars(stars, _size, save))        

    if folks != None:
        imgs.append(draw_folks(folks, _size, save))


    if not imgs:
        return None 

    size = [0,0]

    for img in imgs:
        size[0] += img.size[0]
        size[1] = img.size[1]

    size[0] += (len(imgs) - 1) * img_margin[_size]
    size = (size[0], size[1])

    result_img = Image.new('RGBA', size, None)
    result_img.paste(imgs[0], (0,0) + imgs[0].size)

    left = imgs[0].size[0] + img_margin[_size]
    for img in imgs[1:]:
        result_img.paste(img, (left, 0, left + img.size[0], img.size[1]))
        left += img_margin[_size] + img.size[0]

    
    if save:
        result_img.save('out.png')

    out = BytesIO()
    result_img.save(out, 'PNG')

    out.seek(0)
    return out

def to_text(stars):
    stars = str(stars)
    result = []
    while stars:
        result.append(stars[-3:])
        stars = stars[:-3]
    
    result.reverse()
    return ','.join(result) + ' '



if __name__ == '__main__':
    draw_image(434545,2325,34325,save=True)