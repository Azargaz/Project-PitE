import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC, LinearSVC
from sklearn.linear_model import SGDClassifier
from sklearn.neural_network import MLPClassifier

from sklearn.metrics import accuracy_score, confusion_matrix, roc_curve, roc_auc_score
from sklearn.model_selection import train_test_split, GridSearchCV

import keras
from keras.models import Sequential
from keras.models import model_from_json
from keras.layers import Dense, Dropout, Flatten
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.utils import np_utils
from keras import backend as K

import tensorflow as tf
import keras.backend.tensorflow_backend as tfback

# MOST IMPORTANT PART, FIX TO A BUG IN KERAS !!! ##########################
print("tf.__version__ is", tf.__version__)
print("tf.keras.__version__ is:", tf.keras.__version__)

def _get_available_gpus():
    """Get a list of available gpu devices (formatted as strings).

    # Returns
        A list of available GPU devices.
    """
    #global _LOCAL_DEVICES
    if tfback._LOCAL_DEVICES is None:
        devices = tf.config.list_logical_devices()
        tfback._LOCAL_DEVICES = [x.name for x in devices]
    return [x for x in tfback._LOCAL_DEVICES if 'device:gpu' in x.lower()]

tfback._get_available_gpus = _get_available_gpus
###########################################################################

K.common.set_image_dim_ordering('th')

import itertools

def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    if normalize:
        cm = np.round(cm.astype('float') / cm.sum(axis=1)[:, np.newaxis], 5)
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

axe = np.load('./axe.npy')
angel = np.load('./angel.npy')
axe = np.c_[axe, np.zeros(len(axe))]
angel = np.c_[angel, np.ones(len(angel))]

label_dict = {0:'axe', 1:'angel' }

# merge the axe and angel arrays, and split the features (X) and labels (y). Convert to float32 to save some memory.
X = np.concatenate((axe[:5000,:-1], angel[:5000,:-1]), axis=0).astype('float32')
y = np.concatenate((axe[:5000,-1], angel[:5000,-1]), axis=0).astype('float32')

X_train, X_test, y_train, y_test = train_test_split(X/255.,y,test_size=0.5,random_state=0)
y_train_cnn = np_utils.to_categorical(y_train)
y_test_cnn = np_utils.to_categorical(y_test)
num_classes = y_test_cnn.shape[1]
X_train_cnn = X_train.reshape(X_train.shape[0], 1, 28, 28).astype('float32')
X_test_cnn = X_test.reshape(X_test.shape[0], 1, 28, 28).astype('float32')

def cnn_model():
    model = Sequential()
    model.add(Conv2D(30, (5, 5), input_shape=(1, 28, 28), activation='relu', data_format='channels_first'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(15, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.2))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dense(50, activation='relu'))
    model.add(Dense(num_classes, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

def load_model():
    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()

    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights("model.h5")
    loaded_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    print("Loaded model from disk")
    return loaded_model

def save_model(model_cnn):
    model_json = model_cnn.to_json()
    with open("model.json", "w") as json_file:
        json_file.write(model_json)
    model_cnn.save_weights("model.h5")
    print("Saved model to disk")

from PIL import Image

if input('load model? y/n ') == 'y':
    model_cnn = load_model()
    
    pic = Image.open('./axe.png')
    pic = pic.convert('1')
    test_axe = np.array([[(np.array(pic))/255]])

    cnn_probab = model_cnn.predict(test_axe, batch_size=32, verbose=0)
    print(cnn_probab)

    # cnn_probab = model_cnn.predict(X_test_cnn, batch_size=32, verbose=0)

    # fig, ax = plt.subplots(figsize=(6,15))

    # for i in list(range(10)):

    #     # plot probabilities:
    #     ax = plt.subplot2grid((10, 5), (i, 0), colspan=4);
    #     plt.bar(np.arange(2), cnn_probab[i], 0.35, align='center');
    #     plt.xticks(np.arange(2), ['axe', 'angel'])
    #     plt.tick_params(axis='x', bottom='off', top='off')
    #     plt.ylabel('Probability')
    #     plt.ylim(0,1)
    #     plt.subplots_adjust(hspace = 0.5)

    #     # plot picture:
    #     ax = plt.subplot2grid((10, 5), (i, 4));
    #     plt.imshow(X_test_cnn[i].reshape((28,28)),cmap='gray_r', interpolation='nearest');
    #     plt.xlabel(label_dict[y_test[i]]); # get the label from the dict
    #     plt.xticks([])
    #     plt.yticks([])

    # plt.show()
else:
    model_cnn = cnn_model()
    model_cnn.fit(X_train_cnn, y_train_cnn, validation_data=(X_test_cnn, y_test_cnn), epochs=10, batch_size=200)
    scores = model_cnn.evaluate(X_test_cnn, y_test_cnn, verbose=0)
    save_model(model_cnn)
    print('Final CNN accuracy: ', scores[1])