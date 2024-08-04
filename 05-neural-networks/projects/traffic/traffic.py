import cv2
import numpy as np
import os
import sys
import tensorflow as tf

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    # Initialize variables that will be returned
    images, labels = [], []

    # Start Loading Data
    print(f"Started loading data from {data_dir}")

    # data_dir assumed to use correct os seperator
    for curr_num_category in range(NUM_CATEGORIES):
        curr_directory = os.path.join(data_dir, str(curr_num_category))

        print(f"Loading from: {curr_directory}")
        if os.path.isdir(curr_directory):
            # os.listdir(path) returns list containing name of the entries in the directory given by path
            for file_name in os.listdir(curr_directory):
                file_path = os.path.join(curr_directory, file_name)

                # OpenCV inherently represents images as NumPy arrays
                img = cv2.imread(file_path)
                img = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT))

                # appends NumPy array from currently processed file path and the current category number
                images.append(img)
                labels.append(curr_num_category)

    return images, labels


def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
    model = tf.keras.Sequential([])

    # Convolutional layer that learns 40 filters using 3x3 kernel
    model.add(tf.keras.layers.Conv2D(40, (3, 3), activation="relu",input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)))

    # Convolutional layer that learns 40 filters using 3x3 kernel
    model.add(tf.keras.layers.Conv2D(40, (3, 3), activation="relu",input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)))

    # Max-pooling layer, using 5x5 pool size
    model.add(tf.keras.layers.MaxPooling2D(pool_size=(5, 5)))

    # Flatten units
    model.add(tf.keras.layers.Flatten())

    # Add a dense hidden layer
    model.add(tf.keras.layers.Dense(150, activation="relu"))

    # Add a dense hidden layer with dropout
    model.add(tf.keras.layers.Dense(150, activation="relu"))
    model.add(tf.keras.layers.Dropout(0.3))

    # Add an output layer with output units for all 43 categories
    model.add(tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax"))

    # Provides a summary of the current model
    model.summary()

    model.compile(
        optimizer="adam", # Adam optimization is a stochastic gradient descent method that is based on adaptive estimation of first-order and second-order moments
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model


if __name__ == "__main__":
    main()
