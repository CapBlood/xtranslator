#from PIL import Image
import pytesseract
import cv2
import os

import numpy as np

def imageToText(image: list, preprocess: str = 'thresh'):
    # загрузить образ и преобразовать его в оттенки серого
    gray = cv2.cvtColor(np.array(image, dtype=np.float32), cv2.COLOR_BGR2GRAY)

    # проверьте, следует ли применять пороговое значение для предварительной обработки изображения
    #if preprocess == "thresh":
    #    gray = cv2.threshold(gray, 0, 255,
    #                        cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # если нужно медианное размытие, чтобы удалить шум
    #elif preprocess == "blur":
    #    gray = cv2.medianBlur(gray, 3)
    text = pytesseract.image_to_string(gray)
    return text