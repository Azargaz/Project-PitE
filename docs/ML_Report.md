## Drawuess - Machine Learning report

Drawuess authors: Hubert Jakubek, Sebastian Sitko, Tomasz Piech

### Project idea - drawing and guessing

Main goal of the project was to use [Google's The Quick, Draw!](https://quickdraw.withgoogle.com/) dataset described [here](https://github.com/googlecreativelab/quickdraw-dataset).
The Quick, Draw! is website which allows to play a game of charade, but not versus human - instead versus AI. 
Google open-sourced the dataset collected using this website and it is one of the largest collections of hand-drawn doodles.

Our project is similar to the idea of 'The Quick, Draw!' but simplified and with added extension which allows to play a bit different game mode described later.



### The Neural Network model

Finding right model to use was the most difficult task of machine learning side of the project. We wanted to use model which was already prepared for and trained on the Quickdraw dataset
but unfortunately it was not so easy to find such a model. 

Below a short timeline of what our process of finding model looked like:
1. We tried looking for complete model ready-to-use but we failed to find one that we understood and could make it work.
2. We failed to find one because of problems like:
    - a lot of models needed difficult to setup libraries or even special environments (like Magenta) to use them,
    - often these libraries had a lot of dependencies which where not described properly,
    - because of that they had a lot of compatibility problems with newer versions of dependecy libraries, 
    - models we found for some reason did not have any requirements specified, so we could not use older, compatible versions of these dependency libraries.
3. After failing to find the model we tried looking for tutorials and guides on how to build model using libraries such as Keras and Tensorflow.
4. We found ["Classification of drawings made in the game 'Quick, draw!'"](https://github.com/kradolfer/quickdraw-image-recognition/blob/master/quickdraw_image_recognition.ipynb) - project describing and comparing use of different algorithms and techniques of classifying images.
5. From that project we chose the Convolutional Nerual Network approach and using Keras we built our model based on the project above with some changes (Droput changed from 0.2 to 0.5 and we remade whole training procedure to be more generic and to allow training on more than 2 categories of images).
6. We encoutered some challenges such as: 
    - problems with Tensorflow 2.0 and above - downgrading Tensorflow and some other libraries helped us solve this, 
    - understanding input of Keras models - our images are black and white, but Keras needs additional dimension to discribe color channels even if it's not really used for anything, 
    so everytime we need to pass images shaped like this: [number_of_images, channels(always 1, since we dont need more), width, height]
    - training and storing the model data (this was relatively easy task, after we knew how to input images into the model, 
    we just needed to prepare some images and fit the model, and then save the model data in .json files for later use).
7. Finally we had model ready and trained on 2 categories of images (later we retrained it on 8 categories).

To conclude, most of our problems with finding model came from incompatible libraries and lack of any type of `requirements.txt` files in projects or tutorials desciribing these models.
Another reason for problems was that we did not have any prior knowledge of machine learning, so the whole process was a learning experience.

#### Parameters of model and training

Model consists of 9 layers:
- Convolutional layer with 30 feature maps of size 5×5.
- Pooling layer taking the max over 2*2 patches.
- Convolutional layer with 15 feature maps of size 3×3.
- Pooling layer taking the max over 2*2 patches.
- Dropout layer with a probability of 50%.
- Flatten layer.
- Fully connected layer with 128 neurons and rectifier activation.
- Fully connected layer with 50 neurons and rectifier activation.
- Output layer.

Training was executed on 10,000 samples per category and 10 epochs. Half of all samples became the training set and the other half test set.



### Extended part of project

The extended part of our project is a game mode where user has to draw doodle based on multiple miscategorized images which all resemble one randomly chosen category.
E.g. user sees 4 images of what looks like a 'bucket' and tries to draw it, but the 'bucket' images from dataset are from any other category than 'bucket'.

Below is code for function which finds all miscategorized images of one category (miscategorized images are called 'similar' because they are similar to other category than they were supposed to be categorized).
```python
1. def find_similar_images(category_index, categories):
2.     model, labels = load_model()
3.     category = categories[category_index]
4.     input_images = get_image_range_from_npy(category, 0, SAMPLES)
5.     results = model.predict(input_images, batch_size=32, verbose=0)
6.     similar_images = []
7.     for img_index, result in enumerate(results):
8.         similar_category = ''
9.         save = False
10.        for index, value in enumerate(result):
11.            if index == category_index and value <= MAX_SIMILAR_CATEGORY_ACCURACY:
12.                save = True
13.            if value >= MIN_SIMILAR_CATEGORY_ACCURACY and index != category_index and similar_category == '':
14.                similar_category = '{}:{}:{}'.format(category, categories[index], img_index)
15.        if similar_category != '' and save == True:
16.            similar_images.append(similar_category)
17.    return similar_images
```

Explanation of code above:
- first get the category which will be searched for similar images (line 3.),
- then input all images from such category and predict their categories using the model (line 5.),
- loop through all predictions results with `enumerate` so that we have access to index of image (line 7.),
- loop through results of individual image also with `enumerate` (line 8.), 
individual results are shaped like this: [0.99, 0.55, 0.01, ...] where each value tells how much current image resembles each category,
- first `if` conditional checks (line 11.):
    - if the index of result (`index`) is the same as original category index (`category_index`),
    - and if the value of result (`value`) is smaller than chosen threshold (`MAX_SIMILAR_CATEGORY_ACCURACY`), which in our case was equal to `0.05`,
- second `if` conditional checks (line 12.):
    - if the `value` is bigger than chosen threshold (`MIN_SIMILAR_CATEGORY_ACCURACY`), which we chose to be `0.95`,
    - if index of this category is different than original category index, as we look only for miscategorized images,
    - and if we have already found similar category,
- the thresholds (`MAX_SIMILAR_CATEGORY_ACCURACY` and `MIN_SIMILAR_CATEGORY_ACCURACY`) tell prediction accuracy to look for,
the max one is about how unsimilar image is supposed to be to its' original category, and the min one is about how much image is similar to other category,
- function returns list of strings which are formatted like `original_category:similar_category:image_index`, this is returned inside other function which then saves this list inside database
to allow us to access miscategorized images.



### Sources

Final project sources:
- [Google The Quick, Draw!](https://quickdraw.withgoogle.com/)
- [Google Misfire!](http://misfire.io/)
- [Goodle The Quick, Draw! Dataset](https://github.com/googlecreativelab/quickdraw-dataset)
- [Google The Quick, Draw! simplified dataset in Numpy bitmap files](https://console.cloud.google.com/storage/browser/quickdraw_dataset/full/numpy_bitmap)
- [Classification of drawings made in the game 'Quick, draw!'](https://github.com/kradolfer/quickdraw-image-recognition/blob/master/quickdraw_image_recognition.ipynb)
- [The Sequential model in Keras - documentation](https://keras.io/guides/sequential_model/)
- ['Train a model in tf.keras with Colab, and run it in the browser with TensorFlow.js'](https://medium.com/tensorflow/train-on-google-colab-and-run-on-the-browser-a-case-study-8a45f9b1474e)

Some things we tried but decided to use something different or we could not make them work:
- [Magenta](https://magenta.tensorflow.org/get-started)
- [Sketch RNN (Magenta)](https://github.com/magenta/magenta/blob/master/magenta/models/sketch_rnn/README.md)
- [Quickdraw Simple Models (in Keras)](https://www.kaggle.com/kmader/quickdraw-simple-models)