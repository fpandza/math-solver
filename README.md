# Math solver

## Overview

This app was created as a simple replica of PhotoMath.

It uses a Convolutional Network trained from the following dataset:
https://www.kaggle.com/xainano/handwrittenmathsymbols

To recreate the training steps, run train.py

## Requirements
Python 3.8

## Usage
To run the app locally, please execute the following from the root directory:

```
pip3 install -r requirements.txt
```

and then run the following command with (optional) arguments:

Default image loaded:
```
python3 app.py 
```

Custom image path:
```
python3 app.py --image_path <IMAGE_PATH>
```

Custom tensorflow model path:
```
python3 app.py --model_path <MODEL_PATH>
```

Direct equation input (skips character detection and classification):
```
python3 app.py --direct_equation <EQUATION>
```

## Running with Docker (Flask server)

Run the following commands inside repo folder:

```
docker build -t mini_photomath_app .
docker run --name mini_photomath -p 80:5000 mini_photomath_app
```

Flask app will become accessible through your browser on the server's IP address