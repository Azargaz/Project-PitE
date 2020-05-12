import numpy as np

import matplotlib.pyplot as plt
from PIL import Image

def plot_sample(input_array, index, title=''):
    '''
    Function to plot 28x28 pixel drawings that are stored in a numpy array.
    Specify how many rows and cols of pictures to display (default 4x5).  
    If the array contains less images than subplots selected, surplus subplots remain empty.
    '''
    
    imgplot = plt.imshow(input_array[index,:784].reshape((28,28)), cmap='gray_r', interpolation='nearest')
    plt.xticks([])
    plt.yticks([])

    plt.show()

pic = Image.open('./axe.png')
axe = np.array(pic)/255
print(axe)
# axe = np.load('./axe.npy')
# plot_sample(axe, 3, title="blaaa")