import os
import numpy as np
import joblib
import matplotlib.pyplot as plt
import librosa
import librosa.display
from keras.models import load_model
from keras.utils import load_img, img_to_array
import tensorflow as tf
import cv2
from PIL import Image
from rembg import remove
from joblib import load
from sklearn.preprocessing import LabelEncoder



class Utils:

    @staticmethod
    def predict_keras(keras_model, image_path, input_shape: tuple = (224, 224)) -> list[int]:
        image = load_img(image_path, target_size=input_shape)
        image_array = img_to_array(image) # Converts a PIL Image instance to a Numpy array | Shape: (224, 224, 3)
        image_array = np.expand_dims(image_array, axis=0)  # Expand the shape of an array. Insert a new axis that will appear at the 0 position in the expanded array shape. | Shape: (1, 224, 224, 3)
        image_array = image_array / 255.0  # Normalizing the pixels values to be between 0 and 1
        image_array_resized = tf.image.resize(image_array, input_shape)

        predictions = keras_model.predict(image_array_resized)
        predicted_labels = [1 if p > 0.1 else 0 for p in predictions[0]] # for multilabel
        return predicted_labels
    
    def predict_keras_sound(keras_model, image_path):
        img = load_img(image_path, target_size=(299, 299))
        img_array = img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0  # Rescale image

        # Predict the class
        predictions = keras_model.predict(img_array)
        predicted_class = np.argmax(predictions, axis=1)

        if predicted_class ==0:
            predicted_class="Affects Humans"
        elif predicted_class ==1:
            predicted_class="Affects plant"
        else:
            predicted_class="Eating plants"

        return predicted_class
    
    @staticmethod
    def generate_mel_spectrogram_image(sound_path) -> str:
        y, sr = librosa.load(sound_path, sr=None)

        S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
        S_dB = librosa.power_to_db(S, ref=np.max)

        fig, ax = plt.subplots()
        img = librosa.display.specshow(S_dB, sr=sr, x_axis='time', y_axis='mel', ax=ax)
        fig.colorbar(img, ax=ax, format='%+2.0f dB')

        output_path = os.path.splitext(sound_path)[0] + '.png' # save as image
        plt.savefig(output_path)
        plt.close(fig)

        return output_path
    
    @staticmethod
    def load_keras_model(model_path: str):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found at path: {model_path}")

        return load_model(model_path)
    
    @staticmethod
    def SVM_model_load_predict(model_path: str, scaler_path: str, label_encoder_path: str, n: float, p: float, k: float):
        clf = load(model_path)
        scaler = load(scaler_path)
        # Assuming you need to scale the input features
        #scaler = StandardScaler()  # Replace this with the scaler used during training
        label = joblib.load(label_encoder_path)

        sample = np.array([[n, p, k]])
        sample_scaled = scaler.transform(sample)
        prediction = clf.predict(sample_scaled)
        print(prediction)
        crop_name = label.inverse_transform(prediction)
        return crop_name
    
    def map_result_to_label(result, labels: dict[int, str]):
        # Ensure result is a list or an array
        if not isinstance(result, (list, tuple)):
            raise ValueError("Result should be a list or tuple")
        
        max_index = result.index(max(result))
        
        return labels.get(max_index, "Unknown")
    
    @staticmethod
    def detect_disease_with_background_removal_and_contrast_enhancement(image_path) -> float:
        image = Image.open(image_path)
        image_without_bg = remove(image)

        image_cv2 = cv2.cvtColor(np.array(image_without_bg), cv2.COLOR_RGBA2RGB)

        gray = cv2.cvtColor(image_cv2, cv2.COLOR_BGR2GRAY)

        equalized = cv2.equalizeHist(gray)

        _, thresh = cv2.threshold(equalized, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        disease_area = sum(cv2.contourArea(contour) for contour in contours)

        total_area = image_cv2.shape[0] * image_cv2.shape[1]

        percentage_disease = (disease_area / total_area) * 100

        return(percentage_disease)