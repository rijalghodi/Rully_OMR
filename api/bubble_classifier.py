import numpy as np
import onnxruntime as ort


model_path = '../models/base_bubble_classification.onnx'

session = ort.InferenceSession(model_path)

input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name
input_shape = session.get_inputs()[0].shape

bubble_labels = ['crossed', 'default', 'filled', 'invalid']

def bubble_classifier(img):

    probability = session.run([output_name], {input_name: img})

    category = np.argmax(probability[0][0])

    label = bubble_labels[category]

    return {
        "category": str(category), 
        "label": label,
        "prob": probability[0][0].tolist()
    }
