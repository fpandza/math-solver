# Math solver

## Overview
This app uses a Convolutional Network trained from the following dataset:
https://www.kaggle.com/xainano/handwrittenmathsymbols

To recreate the training steps, run train.py

## Requirements
Python 3.8

## Usage
To run the server, please execute the following from the root directory:

```
pip3 install -r requirements.txt
```

and then run the following command with (optional) arguments:

Default image (2+2) loaded:
```
python3 app.py 
```

Custom image path:
```
python3 app.py --image_path <IMAGE_PATH>
```

Direct equation input (skips character detection and classification):
```
python3 app.py --direct_equation <EQUATION>
```

## Running with Docker

Coming soon