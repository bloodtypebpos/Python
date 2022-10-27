from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import io


def crop_img(img, background_color):
    pix = img.load()
    xxyy = [0, img.size[0] - 1, 0, img.size[1] - 1]
    adds = [1, -1, 1, -1]
    j_ends = [img.size[0] - 1, img.size[0] - 1, img.size[1] - 1, img.size[1] - 1]
    k_ends = [img.size[1] - 1, img.size[1] - 1, img.size[0] - 1, img.size[0] - 1]
    xy = []
    for i in range(0, len(xxyy)):
        val = xxyy[i]
        im_bool = True
        for j in range(0, j_ends[i]):
            num = val + j * adds[i]
            for k in range(0, k_ends[i]):
                if im_bool:
                    if i < 2:
                        pix_color = pix[num, k]
                    else:
                        pix_color = pix[k, num]
                    if pix_color != background_color:
                        if im_bool:
                            xy.append(num)
                            im_bool = False
                            break
                        else:
                            break
                else:
                    break
    return img.crop((xy[0], xy[2], xy[1], xy[3]))


def pad_img(img, padding, color):
    pad_img = Image.new("RGBA", (img.size[0] + 2 * padding, img.size[1] + 2 * padding), color=color)
    pad_img.paste(img, (padding, padding))
    return pad_img


def scale_img(img, scale):
    xy = (int(img.size[0] * scale), int(img.size[1] * scale))
    return img.resize(xy)


def filler_img(size, square_num):
    img = Image.new("RGBA", size, color="white")
    colors = ['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'purple', 'black', 'gray', 'white']
    drw = ImageDraw.Draw(img)
    num = 0
    for i in range(0, size[0]):
        if i % square_num == 0:
            drw.rectangle((i, 0, i+1, size[1]), fill=colors[num % len(colors)])
            num = num + 1
    num = 0
    for i in range(0, size[1]):
        if i % square_num == 0:
            drw.rectangle((0, i, size[0], i+1), fill=colors[num % len(colors)])
            num = num + 1
    return img



def image2file(image):
    """Return `image` as PNG file-like object."""
    image_file = io.BytesIO()
    image.save(image_file, format="PNG")
    return image_file


class PIL_project:
    def __init__(self, fname, **kwargs):
        self.original_img = Image.open(fname)
        self.original_size = self.original_img.size
        self.background_color = self.original_img.load()[0, 0]
        kwargs_list = [
            'cropping',
            'padding'
        ]
        for key in kwargs_list:
            setattr(self, key, kwargs.get(key, None))
        if 'cropping' in kwargs:
            if self.cropping == True:
                self.crop_it()
        if 'padding' in kwargs:
            try:
                print("LETS GO")
                self.pad_it(self.padding[0], self.padding[1])
            except:
                print("OOps.")
                pass

    def pad_it(self, padding, color):
        self.padded_img = pad_img(self.cropped_img, padding, color)

    def crop_it(self):
        self.cropped_img = crop_img(self.original_img, self.background_color)
