### Training model

To train model put `.npy` files in this folder and run `model.py`. It will ask you if you want to train, answer `y` if you want to proceed.
All `.npy` files should be named the same as categories e.g. cat drawings should be named `cat.npy`. 
For now if you need to add more categories change the `CATEGORIES` list inside `model.py`.

Training will produce `model.json`, `model.h5` and `model_labels.json`. These files need to be put inside the main Drawuess folder, 
otherwise the model which is run inside `views.py` will not see these files.