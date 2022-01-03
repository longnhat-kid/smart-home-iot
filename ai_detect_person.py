from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
import cv2
import globals as g

# Load the model
model = load_model('keras_model.h5')
cam = cv2.VideoCapture(0)

def detectPerson():
    ret, frame = cam.read()
    cv2.imwrite("img_detect.png", frame)
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    image = Image.open('img_detect.png')
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image_array
    # run the inference
    prediction = model.predict(data)
    if prediction[0][0] >= prediction[0][1]:
        print("AI: Nobody !!")
        g.buffer.append({"feed_id": "hall-infrared", "payload": "0", "numOfAttempt": 0})
    else:
        print("AI: Detect person !!")
        g.buffer.append({"feed_id": "hall-infrared", "payload": "1", "numOfAttempt": 0})

