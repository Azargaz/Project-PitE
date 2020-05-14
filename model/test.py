import model
import numpy as np
from PIL import Image

pic = Image.open('./axe.png')
pic = pic.convert('1')
test_axe = (np.array(pic))/255

print(model.predict(test_axe))