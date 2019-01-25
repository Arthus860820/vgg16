import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPool2D
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import Adam
from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input


import keras
import cv2


train_path = './train'
valid_path = './valid'
test_path = './test'
train_batches = ImageDataGenerator().flow_from_directory(train_path, target_size=(224,224), classes=['white', 'red','green','whitewine'], batch_size=10)
valid_batches = ImageDataGenerator().flow_from_directory(valid_path, target_size=(224,224), classes=['white', 'red','green','whitewine'], batch_size=4)
test_batches = ImageDataGenerator().flow_from_directory(test_path, target_size=(224,224), classes=['white', 'red','green','whitewine'], batch_size=10)
img_h=224
print(train_batches.image_shape)
model_vgg16=keras.applications.vgg16.VGG16()
model=Sequential()

model.add(Conv2D(32, kernel_size=(3, 3),input_shape=(img_h,img_h,3),activation='relu',padding='same'))
model.add(Conv2D(32, kernel_size=(3, 3),input_shape=(img_h,img_h,3),activation='relu',padding='same'))
model.add(MaxPool2D())

model.add(Conv2D(64, kernel_size=(3, 3),input_shape=(img_h,img_h,3),activation='relu',padding='same'))
model.add(Conv2D(64, kernel_size=(3, 3),input_shape=(img_h,img_h,3),activation='relu',padding='same'))
model.add(MaxPool2D())

model.add(Conv2D(128, kernel_size=(3, 3),input_shape=(img_h,img_h,3),activation='relu',padding='same'))
model.add(Conv2D(128, kernel_size=(3, 3),input_shape=(img_h,img_h,3),activation='relu',padding='same'))
model.add(Conv2D(128, kernel_size=(3, 3),input_shape=(img_h,img_h,3),activation='relu',padding='same'))
model.add(MaxPool2D())


model.add(Conv2D(256, kernel_size=(3, 3),input_shape=(img_h,img_h,3),activation='relu',padding='same'))
model.add(Conv2D(256, kernel_size=(3, 3),input_shape=(img_h,img_h,3),activation='relu',padding='same'))
model.add(Conv2D(256, kernel_size=(3, 3),input_shape=(img_h,img_h,3),activation='relu',padding='same'))
model.add(MaxPool2D())

model.add(Conv2D(256, kernel_size=(3, 3),input_shape=(img_h,img_h,3),activation='relu',padding='same'))
model.add(Conv2D(256, kernel_size=(3, 3),input_shape=(img_h,img_h,3),activation='relu',padding='same'))
model.add(Conv2D(256, kernel_size=(3, 3),input_shape=(img_h,img_h,3),activation='relu',padding='same'))
model.add(MaxPool2D())

model.add(Flatten())
model.add(Dense(256,activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(256,activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(4,activation='softmax'))
model.summary()
sgd = Adam(lr=0.0002212)
model.compile(loss='categorical_crossentropy',optimizer=sgd, metrics=['accuracy'])
model.fit_generator(train_batches, steps_per_epoch=32, validation_data=valid_batches, validation_steps=5, epochs=100, verbose=2)
model.save("pasta.h5")
