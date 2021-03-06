#!/usr/bin/env python3

import tensorflow as tf
from tensorflow import keras

import numpy as np
import argparse
import configparser


def create_model():
    model = keras.models.Sequential()
    model.add(keras.layers.Dense(18, input_shape=(11,), activation='relu'))
    for i in range(2):
        model.add(keras.layers.Dense(18, activation='relu'))
    model.add(keras.layers.Dense(2, activation='sigmoid'))
    return model


if __name__ == '__main__':

    config = configparser.ConfigParser()
    config.read('config')
    params = config['DEFAULT']

    parser = argparse.ArgumentParser(description='Train neural network for parameter estimation')

    parser.add_argument('-s',
                        required=True,
                        help='path to signals file')
    parser.add_argument('-p',
                        required=True,
                        help='path to parameters file')

    args = parser.parse_args()

    x = np.genfromtxt(args.s, delimiter=',')
    y = np.genfromtxt(args.p, delimiter=',')

    model = create_model()
    optimiser = tf.keras.optimizers.Adam()

    model.compile(optimiser, loss='mse')

    es = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=10, verbose=1)
    mc = tf.keras.callbacks.ModelCheckpoint('model.h5', monitor='val_loss', verbose=1)

    model.fit(x, y, epochs=500, callbacks=[es, mc], validation_split=0.2, batch_size=8)
