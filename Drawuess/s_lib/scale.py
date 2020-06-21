from PIL import Image, ImageOps
from io import BytesIO
import base64
import numpy as np

def decode_img(string):
    return Image.open(BytesIO(base64.b64decode(string)))

def scale_and_prepare_image(img):
    img = img.convert('RGB')
    img = ImageOps.invert(img)
    img = img.convert('L')
    img = img.resize((28, 28), Image.BICUBIC)
    img = np.array(img)/255
    return img

def prepare_image(string):
    img = decode_img(string)
    img = scale_and_prepare_image(img)
    return img