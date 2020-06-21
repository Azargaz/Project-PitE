### Training model

Training needs to be run from inside project's root directory.

To train model put `.npy` files here (inside `cnn` folder) and run `model.py` using `python -m Drawuess.cnn.setup`. 
Prompt will ask you if you want to train, answer `y` if you want to proceed.
All `.npy` files should be named the same as categories e.g. cat drawings should be named `cat.npy`.

Training will produce `model.json`, `model.h5` and `model_labels.json`. These files need to be put inside the main Drawuess folder, 
otherwise the model predictions run from inside Django's `views` will not work correctly.

### Setting up database

In case there is a need to setup the database, please run `python -m Drawuess.cnn.setup` inside project's root directory. When prompted for training please answer `n`
and then when prompted to setup similar images and database answer `y`. This will save category names inside database, 
find all incorrectly labeled images and then save paths to them inside database.