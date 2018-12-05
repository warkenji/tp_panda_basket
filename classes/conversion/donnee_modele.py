import tensorflow as tf
from numpy import loadtxt


def conversion(chemin_donnee='train_data.csv', chemin_modele='tf_model.h5'):
    data = loadtxt(chemin_donnee, delimiter=",", skiprows=1)

    train_x = data[:, 0] / 15
    train_y = data[:, 1] / 500

    model = tf.keras.Sequential([
        tf.keras.layers.Dense(units=1, input_shape=(1,), activation=tf.nn.relu),
        tf.keras.layers.Dense(units=64, activation=tf.nn.relu),
        tf.keras.layers.Dense(units=1)
    ])

    optimizer = tf.train.RMSPropOptimizer(0.001)

    model.compile(loss='mse', optimizer=optimizer, metrics=['mae'])

    model.fit(train_x, train_y, epochs=500, validation_split=0.2, verbose=1)

    model.save(chemin_modele)
