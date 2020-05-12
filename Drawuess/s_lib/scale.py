import cv2
import numpy as np
import pybase64





def scale_picture_arr(my_ndarray):
    my_ndarray += "=" * ((4 - len(my_ndarray) % 4) % 4)
    imgdata = pybase64.b64decode(my_ndarray)
    my_array = []
    for i in range(len(imgdata)):
        my_array.append(float(imgdata[i]))
    img = np.array(my_array)
    rescaled = cv2.resize(img, dsize=(28, 28), interpolation=cv2.INTER_CUBIC)
    print('przeskalowano na wymiar {} x {}'.format(28, 28))
    
    cv2.imshow("Resized image", rescaled)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    


    return rescaled

def scale_to_base64(rescaled_data):
    resc = pybase64.b64encode(rescaled_data)
    return resc

#scale_picture_arr('XDDDDDDDDDDDDD')
