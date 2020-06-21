### Downloading images, training model, setting up database

This is the instruction on how to setup the project and how to get all necessary files (assuming all libraries from `requirements.txt` have been installed).
Please go to project's root directory and run setup using `python -m Drawuess.cnn.setup` command.
After running the `setup` you will see this prompt:

    What would you like to setup?
        1. Download images.
        2. Re-initialize and re-train the model.
        3. Clear and setup the database.
    (type 1/2/3 to choose option or any other key to do nothing)

Description for each option:
1. (this option is necessary before running the application if there are no `.npy` files inside `/Drawuess/cnn/` directory) Download images - downloads all images needed to run the application (the `.npy` files).
2. (this option is not necessary unless there are no `model.*` files in root directory) Re-initialize and re-train the model - creates from scratch the model files and then trains model using downloaded images.
3. (this option is not necessary unless there is no `db.sqlite3` file in root directory) Clear and setup the database - setups the database from scratch.

<b>TL;DR:</b> by default there is no need to run setup options 2. and 3. as all model and database files are inside `git` repository, 
but the images needed to run the application are not included inside repository, therefore it is necessary to download them using `setup` script (recommended)
or manually from [Quickdraw's Dataset Google Cloud](https://console.cloud.google.com/storage/browser/quickdraw_dataset/full/numpy_bitmap) (not recommended).
