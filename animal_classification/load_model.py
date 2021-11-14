from keras.models import load_model
import numpy as np
from PIL import Image
import cv2
import tensorflow as tf
from tensorflow.keras.utils import to_categorical

model = load_model("image_model.h5")

img_height = 180
img_width = 180

img = tf.keras.utils.load_img(
    "datasets/pet4.jpeg", target_size=(img_height, img_width)
)

img_array = tf.keras.utils.img_to_array(img)
img_array = tf.expand_dims(img_array, 0)

predictions = model.predict(img_array)
score = tf.nn.softmax(predictions[0])

class_names = ['cavallo', 'elefante', 'farfalla', 'gallina', 'scoiattolo']

print(
    "This image most likely belongs to {} with a {:.2f} percent confidence."
        .format(class_names[np.argmax(score)], 100 * np.max(score))
)
# print(model.summary())
