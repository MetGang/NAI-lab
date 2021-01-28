import scipy.io as sio
import numpy as np
import json
from PIL import Image

WIDTH = 64
HEIGHT = 64

def get_image_as_array(path):
    with Image.open(path) as img:
        if img.mode == 'RGB':
            return np.array(img.resize((WIDTH, HEIGHT), Image.NEAREST)).tolist()
        else:
            return np.array(img.convert('RGB').resize((WIDTH, HEIGHT), Image.NEAREST)).tolist()

annos = sio.loadmat('cars_annos.mat')

X_train = []
X_test = []

print('X')
for i, record in enumerate(annos['annotations'][0]):
    if record[-1][0][0] == 0:
        X_train.append(get_image_as_array(record[0][0]))
    else:
        X_test.append(get_image_as_array(record[0][0]))

y_train = []
y_test = []

print('y')
for record in annos['annotations'][0]:
    if record[-1][0][0] == 0:
        y_train.append(int(record[-2][0][0] - 1))
    else:
        y_test.append(int(record[-2][0][0] - 1))

print('classes')
classes = [ record[0] for record in annos['class_names'][0] ]

data = {
    'X_train': X_train,
    'X_test': X_test,
    'y_train': y_train,
    'y_test': y_test,
    'classes': classes
}

print('json')
with open('cars_dataset.json', 'w') as file:
    json.dump(data, file)
