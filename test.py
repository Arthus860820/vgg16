from keras.models import load_model
import numpy as np
from keras.preprocessing.image import ImageDataGenerator
import cv2
from keras.applications.resnet50 import preprocess_input
from keras.preprocessing import image

test_path = './test'
    # load the trained convolutional neural network
test_batches = ImageDataGenerator().flow_from_directory(test_path, target_size=(224,224), classes=['white', 'red','green','whitewine'], batch_size=10)
print("[INFO] loading network...")
model = load_model('pasta.h5')
for i in range(1,28):
    imag = cv2.imread(test_path+'/'+str(i)+'.jpg')
    img=cv2.resize(imag,(224,224))
    img_array  = image.img_to_array(img)
    x = np.expand_dims(img_array , axis=0)
    x = preprocess_input(x)
    features = model.predict_classes(x,verbose=0)
    print('Predicted:'+test_path+'/'+str(i)+'.jpg'+':::', features[0])
