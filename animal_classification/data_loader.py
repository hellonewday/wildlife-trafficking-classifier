from PIL import Image
import numpy as np
import os
import cv2
import random
from imgaug import augmenters as iaa

data = []
labels = []

file_list = os.listdir("dataset")


def brightness(img, low, high):
    value = random.uniform(low, high)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv = np.array(hsv, dtype=np.float64)
    hsv[:, :, 1] = hsv[:, :, 1] * value
    hsv[:, :, 1][hsv[:, :, 1] > 255] = 255
    hsv[:, :, 2] = hsv[:, :, 2] * value
    hsv[:, :, 2][hsv[:, :, 2] > 255] = 255
    hsv = np.array(hsv, dtype=np.uint8)
    img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return img


for i in range(0, len(file_list)):
    print(i, file_list[i])

    images = os.listdir(f"dataset/{file_list[i]}")
    print("Load file: ", file_list[i], " with label: ", i)
    for image in images:
        imag = cv2.imread(f"dataset/{file_list[i]}/{image}", cv2.IMREAD_COLOR)
        if imag is not None:
            img_from_ar = Image.fromarray(imag, 'RGB')
            resized_image = img_from_ar.resize((50, 50))
            data.append(np.array(resized_image))
            labels.append(i)

            imag = cv2.flip(imag, 0)
            img_from_ar = Image.fromarray(imag, 'RGB')
            resized_image = img_from_ar.resize((50, 50))
            data.append(np.array(resized_image))
            labels.append(i)

            imag = cv2.flip(imag, 1)
            img_from_ar = Image.fromarray(imag, 'RGB')
            resized_image = img_from_ar.resize((50, 50))
            data.append(np.array(resized_image))
            labels.append(i)

            imag = cv2.flip(imag, -1)
            img_from_ar = Image.fromarray(imag, 'RGB')
            resized_image = img_from_ar.resize((50, 50))
            data.append(np.array(resized_image))
            labels.append(i)

            imag = cv2.blur(imag, (20, 20))
            img_from_ar = Image.fromarray(imag, 'RGB')
            resized_image = img_from_ar.resize((50, 50))
            data.append(np.array(resized_image))
            labels.append(i)

            imag = brightness(imag, 0.5, 3)
            img_from_ar = Image.fromarray(imag, 'RGB')
            resized_image = img_from_ar.resize((50, 50))
            data.append(np.array(resized_image))
            labels.append(i)

            rotate = iaa.Affine(rotate=(-25, 25))
            imag = rotate(image=imag)
            img_from_ar = Image.fromarray(imag, 'RGB')
            resized_image = img_from_ar.resize((50, 50))
            data.append(np.array(resized_image))
            labels.append(i)

            seq1 = iaa.Sequential([
                iaa.Affine(rotate=(-25, 25)),
                iaa.AdditiveGaussianNoise(scale=(30, 90)),
                iaa.Crop(percent=(0, 0.4))
            ], random_order=True)
            imag = seq1(image=imag)
            img_from_ar = Image.fromarray(imag, 'RGB')
            resized_image = img_from_ar.resize((50, 50))
            data.append(np.array(resized_image))
            labels.append(i)

            seq2 = iaa.Sequential([
                iaa.CropAndPad(percent=(-0.2, 0.2), pad_mode="edge"),  # crop and pad images
                iaa.AddToHueAndSaturation((-60, 60)),  # change their color
                iaa.ElasticTransformation(alpha=90, sigma=9)  # water-like effect
            ], random_order=True)
            imag = seq2(image=imag)
            img_from_ar = Image.fromarray(imag, 'RGB')
            resized_image = img_from_ar.resize((50, 50))
            data.append(np.array(resized_image))
            labels.append(i)

print('Number of images: ', len(labels))

animals = np.array(data)
labels = np.array(labels)
np.save("animals", animals)
np.save("labels", labels)
