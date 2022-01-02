import cv2
import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from text_detection import get_boxes
from math_solver import solve
from character_classifier import Classifier
import argparse

parser = argparse.ArgumentParser(description='Second best math solver app')
parser.add_argument('--model_path', help='Path to trained model file',
                    default='math_symbols.h5')

args = parser.parse_args()

app = Flask(__name__)
app.secret_key = "secret key"

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
UPLOAD_FOLDER = 'static/uploads/'


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('upload.html')


@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join('static/uploads/', filename))
        photomath(os.path.join('static/uploads/', filename))

        return render_template('upload.html', filename=filename)
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)


def photomath(img):
    image = cv2.imread(img)
    orig = image.copy()

    char_crop_boxes = get_boxes(image)
    flash(f'Number of detected characters: {len(char_crop_boxes)}')

    img_list = []
    for box in char_crop_boxes:
        x_0 = box[0]
        x_1 = box[1]
        y_0 = box[2]
        y_1 = box[3]
        cropped_img = image[y_0:y_1, x_0:x_1]
        img_list.append(cropped_img)

    classifier = Classifier(args.model_path)
    img_list = classifier.prepare_images(img_list)

    flash(f'Number of characters after removing noise: {len(img_list)}')

    output_string = ''

    for img in img_list:
        new_char = classifier.classify(img)
        output_string = output_string + new_char

    flash(f"Detected equation: {output_string}")

    try:
        solved_equation = round(float(solve(output_string)), 3)
    except TypeError:
        solved_equation = 'INVALID INPUT, TRY AGAIN'

    flash('\n###### OUTPUT ######\n')
    flash(f'{output_string} = {solved_equation}')
    return solved_equation


@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


if __name__ == '__main__':
    app.run(host="0.0.0.0")  # host="0.0.0.0"
