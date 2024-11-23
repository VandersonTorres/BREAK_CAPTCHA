import cv2
import os
import numpy as np
import pickle
from imutils import paths

from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from keras.api.models import Sequential
from keras.api.layers import Conv2D, MaxPooling2D
from keras.api.layers import Flatten, Dense

from utils.helpers import resize_to_fit


data = []
labels = []
base_imgs_dir = "captcha_processing/preprocessing/letters_base"

images = paths.list_images(base_imgs_dir)
for file in images:
    label = file.split(os.path.sep)[-2]
    image = cv2.imread(file)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # standardize image size to 20x20
    image = resize_to_fit(image, 20, 20)
    # adding a dimension for keras to read image
    image = np.expand_dims(image, axis=2)

    labels.append(label)
    data.append(image)

data = np.array(data, dtype="float") / 255
labels = np.array(labels)

# Separate in training data (75%) and test data (25%)
(X_train, X_test, Y_train, Y_test) = train_test_split(data, labels, test_size=0.25, random_state=0)

# Convert with one-hot encoding
lb = LabelBinarizer().fit(Y_train)
Y_train = lb.transform(Y_train)
Y_test = lb.transform(Y_test)

# Store the LabelBinarizer with pickle
with open("captcha_processing/trained_model/model_labels.dat", "wb") as pickle_file:
    pickle.dump(lb, pickle_file)

# CREATE AND TRAINING AI (DEEP LEARNING)
model = Sequential()

# Creating first layer of the Convolutional Neural Network
model.add(Conv2D(20, (5, 5), padding="same", input_shape=(20, 20, 1), activation="relu"))
model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

# Creating second layer
model.add(Conv2D(50, (5, 5), padding="same", activation="relu"))
model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

# Creating third layer
model.add(Flatten())
model.add(Dense(500, activation="relu"))

# Exit layer
model.add(Dense(36, activation="softmax"))

# Compile all layers
model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

# Train AI
model.fit(X_train, Y_train, validation_data=(X_test, Y_test), batch_size=36, epochs=20, verbose=1)

# Store model into a file
model.save("captcha_processing/trained_model/trained_model.hdf5")
