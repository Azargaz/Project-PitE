### Training model

Training needs to be started from root project directory with command `python -m Drawuess.cnn.model`.

To train model put `.npy` files here (inside `cnn` folder) and run `model.py` using `python -m Drawuess.cnn.model`. 
Prompt will ask you if you want to train, answer `y` if you want to proceed.
All `.npy` files should be named the same as categories e.g. cat drawings should be named `cat.npy`.

Training will produce `model.json`, `model.h5` and `model_labels.json`. These files need to be put inside the main Drawuess folder, 
otherwise the model predictions run from inside Django's `views` will not work correctly.