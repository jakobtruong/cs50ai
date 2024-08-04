# Traffic

An AI that uses Tensorflow to train a convolutional neural network to identify the type of traffic sign which appears in an image.

## Background

As research continues in the development of self-driving cars, one of the key challenges is computer vision, allowing these cars to develop an understanding of their environment from digital images. In particular, this involves the ability to recognize and distinguish road signs – stop signs, speed limit signs, yield signs, and more.

The dataset that will be used is the [German Traffic Sign Recognition Benchmark (GTSRB)](https://benchmark.ini.rub.de/?section=gtsrb&subsection=news) dataset, which contains thousands of images of 43 different kinds of road signs.

## Files

The datasets for this project are large so the links to the datasets are provided here:

- [Complete Dataset](https://cdn.cs50.net/ai/2020/x/projects/5/gtsrb.zip)
- [Small Dataset for Practice](https://cdn.cs50.net/ai/2020/x/projects/5/gtsrb-small.zip)

## How to Use

Install `Tensorflow`, `opencv-python` and `scikit-learn` if not already installed. If not, run the following command `pip install -r requirements.txt` while in the `traffic` directory to install required dependencies.

To run the program, run the command `python traffic.py data model_filename`

Example run command: `python3 traffic.py ./gtsrb/`

## Final Output (After Optimization)

```shell
$ python traffic.py ./gtsrb/
Epoch 1/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 7s 14ms/step - accuracy: 0.2680 - loss: 3.7624
Epoch 2/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 7s 14ms/step - accuracy: 0.8054 - loss: 0.6959
Epoch 3/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 7s 14ms/step - accuracy: 0.9147 - loss: 0.2858
Epoch 4/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 7s 14ms/step - accuracy: 0.9423 - loss: 0.1996
Epoch 5/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 7s 14ms/step - accuracy: 0.9635 - loss: 0.1353
Epoch 6/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 7s 14ms/step - accuracy: 0.9672 - loss: 0.1283
Epoch 7/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 7s 14ms/step - accuracy: 0.9744 - loss: 0.0992
Epoch 8/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 7s 14ms/step - accuracy: 0.9675 - loss: 0.1137
Epoch 9/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 7s 14ms/step - accuracy: 0.9769 - loss: 0.0888
Epoch 10/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 7s 14ms/step - accuracy: 0.9778 - loss: 0.0808
333/333 - 1s - 4ms/step - accuracy: 0.9747 - loss: 0.1100
```

## Test Results

Starting from the "base model" used in class, the following layers and hyper parameters were experimented with to maximize the accuracy of our model:

- Different numbers of convolutional and pooling layers
- Different numbers and sizes of filters for convolutional layers
- Different pool sizes for pooling layers
- Different numbers and sizes of hidden layers
- Dropout

Base model:
```python
    model = tf.keras.Sequential([])

    # Convolutional layer that learns 32 filters using 3x3 kernel
    model.add(tf.keras.layers.Conv2D(32, (3, 3), activation="relu",input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)))

    # Max-pooling layer, using 2x2 pool size
    model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))

    # Flatten units
    model.add(tf.keras.layers.Flatten())

    # # Add a dense hidden layer with dropout
    model.add(tf.keras.layers.Dense(128, activation="relu"))
    model.add(tf.keras.layers.Dropout(0.5))

    # Add an output layer with output units for all 43 categories
    model.add(tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax"))

    model.compile(
        optimizer="adam", # Adam optimization is a stochastic gradient descent method that is based on adaptive estimation of first-order and second-order moments
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )
```

Below are the list of optimizations starting with the base model:

| Model # |                              Optimization                              | Testing accuracy |
| :-----: | :------------------------------------------------------:               | :--------------: |
|  1      | In Class Model (Base)                                                  |     `0.0559`     |
|  2      | Modify pool size to 5x5                                                |     `0.3076`     |
|  3      | Added additional hidden layer                                          |     `0.8764`     |
|  4      | Additional convolutional layer (32 filters, 5x5 kernel)                |     `0.9706`     |
|  5      | Changed convolutional layers to learn 64 filters from 32               |     `0.9333`     |
|  6      | Switched second convolutional layer to use 3x3 kernel                  |     `0.9761`     |
|  7      | Lowered dropout from 0.5 to 0.3                                        |     `0.9720`     |
|  8      | Added dropout (.3) to hidden layer that was added at step 3            |     `0.9524`     |
|  9      | Increased number of learned filters of both convolutional layers to 40 |     `0.9747`     |

We started with the base model from class which had a poor accuracy of 5.59%. Looking at the model, I believe that this is due to a lack of layers to account for additional complexities that could be learned from the images. After adding an additional hidden dense layer in model 3, the accuracy shot up to a respectable 87.64%. The next major optimization was adding another convolutional layer before the pooling layer which the accuracy increase to 97.06%. Additional modifications were then experimented with such as kernel size and number of learned filters in the convolutional layers that got the model to its final 97.46% accuracy.

Final model after optimizations:
```python
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

    model.compile(
        optimizer="adam", # Adam optimization is a stochastic gradient descent method that is based on adaptive estimation of first-order and second-order moments
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )
```

