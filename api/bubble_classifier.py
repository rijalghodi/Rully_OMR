import numpy as np
from utils import preprocess_bubble
import onnxruntime as ort


model_path = '../models/bubble_classification.onnx'
session = ort.InferenceSession(model_path)

input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name
input_shape = session.get_inputs()[0].shape

bubble_labels = ['crossed', 'default', 'filled', 'invalid']

def bubble_classifier(img, need_preprocess=True, need_img_2_tensor=True):
    if need_preprocess:
        img = preprocess_bubble(img)
    
    if need_img_2_tensor:
        img = img.astype(np.float32) 
        img = np.expand_dims(img, axis=0)
    
    probability = session.run([output_name], {input_name: img})

    category = np.argmax(probability[0][0])

    label = bubble_labels[category]

    return {
        "category": str(category), 
        "label": label,
        "prob": probability[0][0].tolist()
    }
