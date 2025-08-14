# MNIST CNN with Image Augmentation
# pip install tensorflow matplotlib

import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
import matplotlib.pyplot as plt

# 1) Load data
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

# 2) Normalize and add channel dimension
x_train = (x_train / 255.0).astype("float32")[..., np.newaxis]  # (N,28,28,1)
x_test  = (x_test  / 255.0).astype("float32")[..., np.newaxis]

# 3) Augmentation pipeline (works on 4D data)
datagen = ImageDataGenerator(
    rotation_range=10,
    zoom_range=0.1,
    width_shift_range=0.1,
    height_shift_range=0.1
)
datagen.fit(x_train)

# 4) Build a small CNN
model = models.Sequential([
    layers.Conv2D(32, 3, activation='relu', input_shape=(28, 28, 1)),
    layers.Conv2D(32, 3, activation='relu'),
    layers.MaxPooling2D(),
    layers.Dropout(0.25),

    layers.Conv2D(64, 3, activation='relu'),
    layers.MaxPooling2D(),
    layers.Dropout(0.25),

    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(10, activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# 5) Train with augmentation
batch_size = 64
epochs = 6
model.fit(datagen.flow(x_train, y_train, batch_size=batch_size),
          epochs=epochs,
          validation_data=(x_test, y_test),
          verbose=2)

# 6) Evaluate
test_loss, test_acc = model.evaluate(x_test, y_test, verbose=0)
print(f"Test accuracy: {test_acc:.4f}")

# 7) Predictions and quick grid
pred = model.predict(x_test[:25], verbose=0)

plt.figure(figsize=(10, 10))
for i in range(25):
    plt.subplot(5, 5, i + 1)
    plt.xticks([]); plt.yticks([]); plt.grid(False)
    plt.imshow(x_test[i].squeeze(), cmap=plt.cm.binary)
    p = pred[i].argmax()
    t = y_test[i]
    color = 'blue' if p == t else 'red'
    plt.xlabel(f"Pred: {p}\nTrue: {t}", color=color)
plt.tight_layout()
plt.show()
