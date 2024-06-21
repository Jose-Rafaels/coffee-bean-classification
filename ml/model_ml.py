from tensorflow.keras.models import load_model
import numpy as np
from tensorflow.keras.preprocessing.image import load_img

CLASSES = ['Dark', 'Green', 'Light', 'Medium']

def vgg16(img_path) : 
    model_vgg16  = load_model("ml/cofee_model_vgg16.h5")
    image = load_img(img_path, target_size=(224, 224))
    img_arr = np.array(image)
    img_vgg16 = img_arr / 255.0
    img_vgg16 = img_vgg16.reshape(1, 224, 224, 3)
    label_vgg16 = model_vgg16.predict(img_vgg16)
    predicted_class_vgg16 = CLASSES[np.argmax(label_vgg16)]
    percentage_vgg16 = np.max(label_vgg16) * 100
    return predicted_class_vgg16, percentage_vgg16

def inception(img_path) :
    model_inception  = load_model("ml/coffee_model_inceptionV3.h5")
    image = load_img(img_path, target_size=(299, 299))
    img_arr = np.array(image)
    img_inception = img_arr / 255.0
    img_inception = img_inception.reshape(1, 299, 299, 3)
    label_inception = model_inception.predict(img_inception)
    predicted_class_inception = CLASSES[np.argmax(label_inception)]
    percentage_inception = np.max(label_inception) * 100
    return predicted_class_inception, percentage_inception

