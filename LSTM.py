from keras.models import Sequential
from keras.layers.convolutional import Conv3D
from keras.layers.convolutional_recurrent import ConvLSTM2D
from keras.layers.normalization import BatchNormalization
import numpy as np
import pylab as plt

seq = Sequential()
seq.add(ConvLSTM2D(filters=40, kernel_size=(3, 3),
input_shape=(None, 40, 40, 1),
padding='same', return_sequences=True))
seq.add(BatchNormalization())
seq.add(ConvLSTM2D(filters=40, kernel_size=(3, 3),
padding='same', return_sequences=True))
seq.add(BatchNormalization())
seq.add(ConvLSTM2D(filters=40, kernel_size=(3, 3),
padding='same', return_sequences=True))
seq.add(BatchNormalization())
seq.add(ConvLSTM2D(filters=40, kernel_size=(3, 3),
padding='same', return_sequences=True))
seq.add(BatchNormalization())
seq.add(Conv3D(filters=1, kernel_size=(3, 3, 3),
activation='sigmoid',
padding='same', data_format='channels_last'))
seq.compile(loss='binary_crossentropy', optimizer='adadelta')

# Artificial data generation:
# Generate movies with 3 to 7 moving squares inside.
# The squares are of shape 1x1 or 2x2 pixels,
# which move linearly over time.
# For convenience we first create movies with bigger width and height (80x80)
# and at the end we select a 40x40 window.
def generate_movies(n_samples=1200, n_frames=15):
    row = 80
    col = 80
    noisy_movies = np.zeros((n_samples, n_frames, row, col, 1), dtype=np.float)
    shifted_movies = np.zeros((n_samples, n_frames, row, col, 1),
    dtype=np.float)
    for i in range(n_samples):
        # Add 3 to 7 moving squares
        n = np.random.randint(3, 8)
    for j in range(n):
        # Initial position
        xstart = np.random.randint(20, 60)
        ystart = np.random.randint(20, 60)
        # Direction of motion
        directionx = np.random.randint(0, 3) - 1
        directiony = np.random.randint(0, 3) - 1
        # Size of the square
        w = np.random.randint(2, 4)
    for t in range(n_frames):
        x_shift = xstart + directionx * t
        y_shift = ystart + directiony * t
        noisy_movies[i, t, x_shift - w: x_shift + w,
        y_shift - w: y_shift + w, 0] += 1
        # Make it more robust by adding noise.
        # The idea is that if during inference,
        # the value of the pixel is not exactly one,
        # we need to train the network to be robust and still
        # consider it as a pixel belonging to a square.
    if np.random.randint(0, 2):
        noise_f = (-1)**np.random.randint(0, 2)
        noisy_movies[i, t,
        x_shift - w - 1: x_shift + w + 1,
        y_shift - w - 1: y_shift + w + 1,
        0] += noise_f * 0.1
    # Shift the ground truth by 1
    x_shift = xstart + directionx * (t + 1)
    y_shift = ystart + directiony * (t + 1)
    shifted_movies[i, t, x_shift - w: x_shift + w,
    y_shift - w: y_shift + w, 0] += 1
    # Cut to a 40x40 window
    noisy_movies = noisy_movies[::, ::, 20:60, 20:60, ::]
    shifted_movies = shifted_movies[::, ::, 20:60, 20:60, ::]
    noisy_movies[noisy_movies >= 1] = 1
    shifted_movies[shifted_movies >= 1] = 1
    return noisy_movies, shifted_movies