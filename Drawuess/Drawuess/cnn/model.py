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

from .database import create_connection, clear_similar, insert_similar, get_category_names

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
DB_PATH = './db.sqlite3'
SAMPLES = 10000

MAX_SIMILAR_CATEGORY_ACCURACY = 0.05
MIN_SIMILAR_CATEGORY_ACCURACY = 0.95

def load_model():
    conn = create_connection(DB_PATH)
    with conn:
        json_file = open(MODEL_PATH, 'r')
        loaded_model_json = json_file.read()
        json_file.close()

        loaded_model = model_from_json(loaded_model_json)
        loaded_model.load_weights(MODEL_WEIGHTS_PATH)
        loaded_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

        labels = get_category_names(conn)
        return loaded_model, labels

def save_model(model):
    model_json = model.to_json()
    with open(MODEL_PATH, "w") as json_file:
        json_file.write(model_json)
    model.save_weights(MODEL_WEIGHTS_PATH)

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
    conn = create_connection(DB_PATH)
    with conn:
        categories = get_category_names(conn)
        X_train, X_test, y_train, y_test, label_dict = setup_categories(categories, SAMPLES, verbose=True)
        y_train_cnn = np_utils.to_categorical(y_train)
        y_test_cnn = np_utils.to_categorical(y_test)
        num_classes = y_test_cnn.shape[1]
        X_train_cnn = X_train.reshape(X_train.shape[0], 1, 28, 28).astype('float32')
        X_test_cnn = X_test.reshape(X_test.shape[0], 1, 28, 28).astype('float32')

        model = cnn_model(num_classes)
        model.fit(X_train_cnn, y_train_cnn, validation_data=(X_test_cnn, y_test_cnn), epochs=10, batch_size=200)
        scores = model.evaluate(X_test_cnn, y_test_cnn, verbose=0)
        save_model(model)

def get_image_range_from_npy(category, a, b):    
    images = np.load('./Drawuess/cnn/{}.npy'.format(category))
    images = images[a:b, :]
    images = images[:, :784].reshape((images.shape[0], 1, 28, 28))
    images = images / 255.
    return images

def get_single_image_from_npy(category, index):
    return get_image_range_from_npy(category, index, index+1)

def find_similar_images(category_index, categories):
    model, labels = load_model()
    category = categories[category_index]
    input_images = get_image_range_from_npy(category, 0, SAMPLES)
    results = model.predict(input_images, batch_size=32, verbose=0)
    similar_images = []
    for img_index, result in enumerate(results):
        similar_category = ''
        save = False
        for index, value in enumerate(result):
            if index == category_index and value <= MAX_SIMILAR_CATEGORY_ACCURACY:
                save = True
            if value >= MIN_SIMILAR_CATEGORY_ACCURACY and index != category_index and similar_category == '':
                similar_category = '{}:{}:{}'.format(category, categories[index], img_index)
        if similar_category != '' and save == True:
            similar_images.append(similar_category)
    return similar_images

def sort_similar_images(similars):
    sorted_images = dict()
    for similar in similars:
        for image in similar:
            image = image.split(':')
            if image[0] not in sorted_images:
                sorted_images[image[0]] = []
            sorted_images[image[0]].append('{}:{}'.format(image[1], image[2]))
    return sorted_images

def find_all_similar_images():
    try:
        conn = create_connection(DB_PATH)
        with conn:
            similars = []
            categories = get_category_names(conn)
            for category_index, category in enumerate(categories):
                print('Finding similar images in category {}...'.format(category))
                similars.append(find_similar_images(category_index, categories))
            similars = sort_similar_images(similars)
            clear_similar(conn)
            for category in similars:
                for similar in similars[category]:
                    similar = similar.split(':')
                    insert_similar(conn, [category, similar[0], similar[1]])
    except Exception as e:
        print('Error while finding similar images: {}'.format(e))

def predict(input_image):
    try:
        model, labels = load_model()
        input_image = np.array([[input_image]])
        result = model.predict_classes(input_image, batch_size=32, verbose=0)
        return labels[int(result[0])]
    except Exception as e:
        print('Error while predicting: {}'.format(e))

if __name__ == '__main__':
    if input('Are you sure you want to re-initialize and re-train the model? (Y/n) ' ).lower() == 'y':
        train()
    elif input('Do you want to setup similar images? (Y/n) ' ).lower() == 'y':
        find_all_similar_images()