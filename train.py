# -*- coding: utf-8 -*-

import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator

train_path = "/dataset"

train_datagen = ImageDataGenerator(
    rescale=1./255,
    shear_range=0.2,
    zoom_range=0.2,
    validation_split=0.25
)
train_set = train_datagen.flow_from_directory(
    train_path,
    target_size=(45, 45),
    color_mode='grayscale',
    batch_size=64,
    class_mode='categorical',
    classes=['0', '1', '2', '3', '4', '5', '6', '7',
             '8', '9', '+', '-', ')', '(', 'times', 'div'],
    shuffle=True,
    subset='training',
    seed=123
)


test_set = train_datagen.flow_from_directory(
    train_path,
    target_size=(45, 45),
    color_mode='grayscale',
    batch_size=64,
    class_mode='categorical',
    classes=['0', '1', '2', '3', '4', '5', '6', '7',
             '8', '9', '+', '-', ')', '(', 'times', 'div'],
    shuffle=True,
    subset='validation',
    seed=123
)


def symbol(ind):
    symbols = ['0', '1', '2', '3', '4', '5', '6', '7',
               '8', '9', '+', '-', ')', '(', 'times', 'div']
    symb = symbols[ind.argmax()]
    return symb


model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu',
                           input_shape=(45, 45, 1)),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(16, activation='softmax')
])

model.summary()
model.compile(loss='categorical_crossentropy',
              optimizer='rmsprop', metrics=['accuracy'])
history = model.fit(train_set, epochs=1,
                    validation_data=test_set, verbose=1, validation_steps=3)


model.save("math_symbols.h5")
