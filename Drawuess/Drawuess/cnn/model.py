import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from tensorflow import keras
from keras.models import Sequential, model_from_json
from keras.layers import Dense, Dropout, Flatten
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.utils import np_utils
from keras import backend as K

from sklearn.model_selection import train_test_split

import os.path
import json
import tensorflow.compat.v1 as tf

import random

# FIX TO A BUG IN KERAS + TENSORFLOW >2.0 !!! #############################
# import keras.backend.tensorflow_backend as tfback
# import tensorflow as tf

# print("tf.__version__ is", tf.__version__)
# print("tf.keras.__version__ is:", tf.keras.__version__)

# def _get_available_gpus():
#     """Get a list of available gpu devices (formatted as strings).

#     # Returns
#         A list of available GPU devices.
#     """
#     #global _LOCAL_DEVICES
#     if tfback._LOCAL_DEVICES is None:
#         devices = tf.config.list_logical_devices()
#         tfback._LOCAL_DEVICES = [x.name for x in devices]
#     return [x for x in tfback._LOCAL_DEVICES if 'device:gpu' in x.lower()]

# tfback._get_available_gpus = _get_available_gpus
###########################################################################

K.common.set_image_dim_ordering('th')

MODEL_PATH = 'model.json'
MODEL_WEIGHTS_PATH = 'model.h5'
MODEL_LABELS = 'model_labels.json'

CATEGORIES = ['axe', 'angel', 'alarm clock', 'ant', 'apple', 'bat', 'bucket', 'cannon']
SAMPLES = 10000

def load_model():
    print(os.getcwd())

    json_file = open(MODEL_PATH, 'r')
    loaded_model_json = json_file.read()
    json_file.close()

    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights(MODEL_WEIGHTS_PATH)
    loaded_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    json_file = open(MODEL_LABELS, 'r')
    labels = json.load(json_file)
    json_file.close()
    return loaded_model, labels

def save_model(model, labels):
    model_json = model.to_json()
    with open(MODEL_PATH, "w") as json_file:
        json_file.write(model_json)
    model.save_weights(MODEL_WEIGHTS_PATH)
    with open(MODEL_LABELS, "w") as json_file:
        json.dump(labels, json_file)

def check_if_model_exists():
    return os.path.isfile(MODEL_PATH) and os.path.isfile(MODEL_WEIGHTS_PATH)

def setup_categories(categories, samples, verbose=False):
    label_dict = dict()

    for index, category in enumerate(categories):
        if verbose:
            print("Setting up '{}' category...".format(category))
        label_dict[index] = str(category)
        category = np.load('./{}.npy'.format(category))
        category = category[:samples, :]
        if verbose:
            print(category.shape)
        category = np.c_[category, index * np.ones(len(category))]
        categories[index] = category
    
    X = np.concatenate(([cat[:samples, :-1] for cat in categories]), axis=0).astype('float32')
    y = np.concatenate(([cat[:samples, -1] for cat in categories]), axis=0).astype('float32')
    X_train, X_test, y_train, y_test = train_test_split(X/255.,y, test_size=0.5, random_state=0)
    return X_train, X_test, y_train, y_test, label_dict

def cnn_model(num_classes):
    model = Sequential()
    model.add(Conv2D(30, (5, 5), input_shape=(1, 28, 28), activation='relu', data_format='channels_first'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(15, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.5))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dense(50, activation='relu'))
    model.add(Dense(num_classes, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    return model

def train():
    X_train, X_test, y_train, y_test, label_dict = setup_categories(CATEGORIES, SAMPLES, verbose=True)
    y_train_cnn = np_utils.to_categorical(y_train)
    y_test_cnn = np_utils.to_categorical(y_test)
    num_classes = y_test_cnn.shape[1]
    X_train_cnn = X_train.reshape(X_train.shape[0], 1, 28, 28).astype('float32')
    X_test_cnn = X_test.reshape(X_test.shape[0], 1, 28, 28).astype('float32')

    model = cnn_model(num_classes)
    model.fit(X_train_cnn, y_train_cnn, validation_data=(X_test_cnn, y_test_cnn), epochs=10, batch_size=200)
    scores = model.evaluate(X_test_cnn, y_test_cnn, verbose=0)
    save_model(model, label_dict)

def get_category_image_range_from_npy(category, a, b):    
    images = np.load('./{}.npy'.format(category))
    images = images[a:b, :]
    images = images[:, :784].reshape((images.shape[0], 1, 28, 28))
    images = images / 255.
    return images

# from PIL import Image

def find_similar_images():
    SIMILAR_SAMPLES = 10000
    if check_if_model_exists():
        model, labels = load_model()
        for category_index, category in enumerate(CATEGORIES):
            input_image = get_category_image_range_from_npy(CATEGORIES[category_index], SAMPLES, SAMPLES + SIMILAR_SAMPLES)
            result = model.predict(input_image, batch_size=32, verbose=0)
            for img_index, res in enumerate(result):
                similar_categories = []
                for i, r in enumerate(res):
                    if r >= 0.9 and i != category_index:
                        similar_categories.append('{}={:.3f}'.format(CATEGORIES[i], r))
                if len(similar_categories) > 0:
                    print('{}: [ {} ] [ {} ]'.format(img_index, similar_categories, category))
                    # Image.fromarray(get_category_image_range_from_npy(CATEGORIES[category_index], SAMPLES + img_index, SAMPLES + img_index+1)[0, 0, :, :] * 255).show()
    else:
        return 'Could not find model and/or weights files.'

def predict(input_image):
    if check_if_model_exists():
        model, labels = load_model()
        input_image = np.array([[input_image]])
        result = model.predict_classes(input_image, batch_size=32, verbose=0)
        return labels[str(result[0])]
    else:
        return 'Could not find model and/or weights files.'

if __name__ == '__main__':
    if input('Are you sure you want to re-initialize and re-train the model? (Y/n) ' ).lower() == 'y':
        train()
    else:
        find_similar_images()