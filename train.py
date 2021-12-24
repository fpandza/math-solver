# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from sklearn.metrics import classification_report
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator

train_path = "dataset/"

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
               '8', '9', '+', '-', ')', '(', 'x', '/']
    symb = symbols[ind.argmax()]
    return symb


model = tf.keras.models.Sequential([
    # Note the input shape is the desired size of the image 150x150 with 3 bytes color
    # This is the first convolution
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu',
                           input_shape=(45, 45, 1)),
    tf.keras.layers.MaxPooling2D(2, 2),
    # The second convolution
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    # The third convolution
    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    # Flatten the results to feed into a DNN
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dropout(0.5),
    # 512 neuron hidden layer
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(16, activation='softmax')
])

model.summary()
adam = tf.keras.optimizers.Adam(lr=8e-4)
model.compile(loss='categorical_crossentropy',
              optimizer=adam, metrics=['accuracy'])
history = model.fit(train_set, epochs=2,
                    validation_data=test_set, verbose=1, validation_steps=3)


model.save("math_symbol.h5")

argmx = []
labels_argmx = []

for i in range(100):
    imgs, lbls = next(test_set)
    # Labels
    lbls_argmax = [label.argmax() for label in lbls]
    labels_argmx.extend(lbls_argmax)
    # Predictions
    preds = model.predict(imgs)
    preds_argmax = [pred.argmax() for pred in preds]
    argmx.extend(preds_argmax)

y_true = labels_argmx
y_pred = argmx
target_names = ['0', '1', '2', '3', '4', '5', '6',
                '7', '8', '9', '+', '-', ')', '(', 'x', '/']
print(classification_report(y_true, y_pred, target_names=target_names))

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range(len(acc))

plt.plot(epochs, acc, 'r', label='Training accuracy')
plt.plot(epochs, val_acc, 'b', label='Validation accuracy')
plt.title('Training and validation accuracy')
plt.legend(loc=0)
plt.figure()

plt.show()
